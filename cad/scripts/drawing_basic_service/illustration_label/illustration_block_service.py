from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

import pythoncom
import win32com.client

from library.cad_blocks import attsync_block_instance
from system.CAD_com_utils import retry_if_busy
from system.CAD_coordination import wait_command_done, wait_quiescent
from system.CAD_core import launch_cad_guardians, litz, open_file
from system.common_logger import sys_logger
from system.licad import C
from system.runtime_guard_bridge import (
    RuntimeGuardTriggered,
    assert_runtime_guard_ok,
    render_guard_error,
)


DEFAULT_BLOCK_NAMES = ("A0", "A1", "A2", "A3")
_BLOCK_REF_CAST_MAP = {
    "AcDbBlockReference": "IAcadBlockReference",
    "AcDbMInsertBlock": "IAcadMInsertBlock",
}


@dataclass
class BlockReplaceResult:
    block_name: str
    source_entity_count: int
    reassigned_reference_count: int
    backup_block_name: str | None
    backup_deleted: bool
    attribute_sync_triggered: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _guard_checkpoint(checkpoint: str) -> None:
    try:
        decision = assert_runtime_guard_ok(checkpoint)
    except RuntimeGuardTriggered as exc:
        payload = render_guard_error(exc)
        sys_logger.error("[runtime_guard] %s", payload)
        raise RuntimeError(f"runtime guard blocked at {checkpoint}: {payload}") from exc

    sys_logger.info(
        "[runtime_guard] checkpoint=%s status=%s action=%s",
        checkpoint,
        decision.status,
        decision.recommended_action,
    )


def _point_variant(point: Iterable[float]) -> Any:
    return win32com.client.VARIANT(
        pythoncom.VT_ARRAY | pythoncom.VT_R8,
        tuple(float(v) for v in point),
    )


def _dispatch_variant(objects: Sequence[Any]) -> Any:
    return win32com.client.VARIANT(
        pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH,
        tuple(objects),
    )


def _block_exists(doc: Any, block_name: str) -> bool:
    try:
        _blocks_item(doc.Blocks, block_name)
        return True
    except Exception:
        return False


def _activate_document(doc: Any) -> None:
    try:
        doc.Activate()
    except Exception:
        pass


def _collect_block_entities(block_def: Any) -> list[Any]:
    count = _collection_count(block_def)
    return [_collection_item(block_def, i) for i in range(count)]


def _iter_block_containers(doc: Any) -> Iterable[Any]:
    total = _collection_count(doc.Blocks)
    for idx in range(total):
        yield _collection_item(doc.Blocks, idx)


def _as_block_reference(entity: Any) -> Any | None:
    try:
        obj_name = str(getattr(entity, "ObjectName", "") or "")
    except Exception:
        return None
    iface = _BLOCK_REF_CAST_MAP.get(obj_name)
    if not iface:
        return None
    try:
        return win32com.client.CastTo(entity, iface)
    except Exception:
        return None


def _get_reference_name(block_ref: Any) -> str:
    try:
        return str(getattr(block_ref, "Name", "") or "")
    except Exception:
        return ""


def _unique_backup_name(doc: Any, block_name: str) -> str:
    stem = f"{block_name}__OLD"
    if not _block_exists(doc, stem):
        return stem

    index = 1
    while True:
        candidate = f"{stem}_{index}"
        if not _block_exists(doc, candidate):
            return candidate
        index += 1


@retry_if_busy(max_retries=8, delay=0.6)
def _rename_block_definition(block_def: Any, new_name: str) -> str:
    block_def.Name = new_name
    return new_name


@retry_if_busy(max_retries=8, delay=0.6)
def _create_block_definition(doc: Any, base_point: Sequence[float], block_name: str) -> Any:
    return doc.Blocks.Add(_point_variant(base_point), block_name)


@retry_if_busy(max_retries=8, delay=0.6)
def _copy_entities_to_owner(source_doc: Any, entities: Sequence[Any], owner: Any) -> Any:
    return source_doc.CopyObjects(_dispatch_variant(entities), owner)


@retry_if_busy(max_retries=8, delay=0.6)
def _set_block_reference_name(block_ref: Any, new_name: str) -> bool:
    block_ref.Name = new_name
    return True


@retry_if_busy(max_retries=8, delay=0.6)
def _delete_block_definition(block_def: Any) -> bool:
    block_def.Delete()
    return True


@retry_if_busy(max_retries=8, delay=0.6)
def _save_document(doc: Any) -> bool:
    doc.Save()
    return True


@retry_if_busy(max_retries=8, delay=0.6)
def _collection_count(collection: Any) -> int:
    return int(getattr(collection, "Count", 0) or 0)


@retry_if_busy(max_retries=8, delay=0.6)
def _collection_item(collection: Any, index: int) -> Any:
    return collection.Item(index)


@retry_if_busy(max_retries=8, delay=0.6)
def _blocks_item(blocks: Any, key: Any) -> Any:
    return blocks.Item(key)


def _reassign_block_references(doc: Any, old_name: str, new_name: str) -> list[Any]:
    changed_refs: list[Any] = []

    for container in _iter_block_containers(doc):
        entity_count = _collection_count(container)
        for idx in range(entity_count):
            entity = _collection_item(container, idx)
            block_ref = _as_block_reference(entity)
            if block_ref is None:
                continue

            current_name = _get_reference_name(block_ref)
            if current_name != old_name:
                continue

            _set_block_reference_name(block_ref, new_name)
            try:
                block_ref.Update()
            except Exception:
                pass
            changed_refs.append(block_ref)

    return changed_refs


def _count_block_references(doc: Any, block_name: str) -> int:
    count = 0
    for container in _iter_block_containers(doc):
        entity_count = _collection_count(container)
        for idx in range(entity_count):
            entity = _collection_item(container, idx)
            block_ref = _as_block_reference(entity)
            if block_ref is None:
                continue
            if _get_reference_name(block_ref) == block_name:
                count += 1
    return count


def _require_block_definition(doc: Any, block_name: str, *, role: str) -> Any:
    try:
        return _blocks_item(doc.Blocks, block_name)
    except Exception as exc:
        raise RuntimeError(f"{role} 中找不到块定义: {block_name}") from exc


def _open_document(path: Path) -> Any:
    if not open_file(str(path)):
        raise RuntimeError(f"打开 DWG 失败: {path}")
    wait_quiescent(min_quiet=0.8, timeout=30.0)
    return C.raw_doc


def prepare_cad_runtime(*, ensure_guard: bool = True) -> None:
    if ensure_guard:
        launch_cad_guardians()
    _guard_checkpoint("before_litz")
    if not litz():
        raise RuntimeError("CAD 受控入口初始化失败")
    wait_quiescent(min_quiet=1.0, timeout=60.0)
    _guard_checkpoint("after_litz")


def replace_single_block_definition(
    source_doc: Any,
    target_doc: Any,
    block_name: str,
    *,
    run_attsync: bool = True,
) -> BlockReplaceResult:
    _activate_document(target_doc)
    wait_quiescent(min_quiet=0.5, timeout=20.0)
    _guard_checkpoint(f"before_replace_{block_name}")

    source_block = _require_block_definition(source_doc, block_name, role="源文件")
    target_block = _require_block_definition(target_doc, block_name, role="目标文件")

    source_entities = _collect_block_entities(source_block)
    if not source_entities:
        raise RuntimeError(f"源块定义为空，无法替换: {block_name}")

    backup_name = _unique_backup_name(target_doc, block_name)
    source_origin = tuple(float(v) for v in getattr(source_block, "Origin", (0.0, 0.0, 0.0)))

    sys_logger.info(
        "[replace_block] block=%s source_entities=%s backup=%s",
        block_name,
        len(source_entities),
        backup_name,
    )

    _rename_block_definition(target_block, backup_name)
    wait_quiescent(min_quiet=0.3, timeout=15.0)

    new_block = _create_block_definition(target_doc, source_origin, block_name)
    _copy_entities_to_owner(source_doc, source_entities, new_block)
    wait_quiescent(min_quiet=0.5, timeout=20.0)

    changed_refs = _reassign_block_references(target_doc, backup_name, block_name)
    wait_quiescent(min_quiet=0.5, timeout=20.0)

    try:
        target_doc.Regen(1)
    except Exception:
        pass

    attribute_sync_triggered = False
    if run_attsync and changed_refs:
        try:
            attribute_sync_triggered = bool(attsync_block_instance(changed_refs[0]))
            wait_command_done(timeout=60.0, quiet_time=0.5)
        except Exception as exc:
            sys_logger.warning("[replace_block] ATTSYNC 失败 block=%s error=%s", block_name, exc)

    remaining = _count_block_references(target_doc, backup_name)
    if remaining:
        raise RuntimeError(
            f"仍有 {remaining} 个块实例指向旧定义 {backup_name}，替换未完成: {block_name}"
        )

    backup_deleted = False
    try:
        _delete_block_definition(_blocks_item(target_doc.Blocks, backup_name))
        backup_deleted = True
    except Exception as exc:
        sys_logger.warning(
            "[replace_block] 旧块定义删除失败 block=%s backup=%s error=%s",
            block_name,
            backup_name,
            exc,
        )

    _guard_checkpoint(f"after_replace_{block_name}")
    return BlockReplaceResult(
        block_name=block_name,
        source_entity_count=len(source_entities),
        reassigned_reference_count=len(changed_refs),
        backup_block_name=backup_name,
        backup_deleted=backup_deleted,
        attribute_sync_triggered=attribute_sync_triggered,
    )


def replace_defined_blocks(
    *,
    target_file: str | Path,
    source_file: str | Path,
    block_names: Sequence[str] = DEFAULT_BLOCK_NAMES,
    ensure_guard: bool = True,
    run_attsync: bool = False,
) -> dict[str, Any]:
    target_path = Path(target_file).resolve()
    source_path = Path(source_file).resolve()

    if not target_path.exists():
        raise FileNotFoundError(f"目标文件不存在: {target_path}")
    if not source_path.exists():
        raise FileNotFoundError(f"源文件不存在: {source_path}")
    if target_path == source_path:
        raise ValueError("目标文件和源文件不能相同")

    prepare_cad_runtime(ensure_guard=ensure_guard)

    source_doc = _open_document(source_path)
    source_name = str(getattr(source_doc, "FullName", source_path))
    target_doc = _open_document(target_path)
    target_name = str(getattr(target_doc, "FullName", target_path))

    sys_logger.info("[replace_defined_blocks] source=%s target=%s", source_name, target_name)
    _guard_checkpoint("after_open_source_and_target")

    results = [
        replace_single_block_definition(
            source_doc,
            target_doc,
            block_name,
            run_attsync=run_attsync,
        ).to_dict()
        for block_name in block_names
    ]

    _activate_document(target_doc)
    _save_document(target_doc)
    wait_quiescent(min_quiet=0.8, timeout=30.0)
    _guard_checkpoint("after_target_save")

    return {
        "ok": True,
        "target_file": str(target_path),
        "source_file": str(source_path),
        "block_names": list(block_names),
        "results": results,
    }
