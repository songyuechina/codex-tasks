from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

import pythoncom
import psutil
import win32com.client
import win32process


def find_codex_tasks_root(p: Path) -> Path:
    cur = p.resolve()
    if cur.is_file():
        cur = cur.parent
    while True:
        if cur.name.lower() == "codex-tasks":
            return cur
        if cur.parent == cur:
            raise RuntimeError("找不到根目录 codex-tasks")
        cur = cur.parent


ROOT = find_codex_tasks_root(Path(__file__))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "cad") not in sys.path:
    sys.path.insert(0, str(ROOT / "cad"))

from system.common_logger import set_debug_mode, sys_logger
from system.licad import C


Point3D = Tuple[float, float, float]


def load_cad_geometry_draw_module():
    module_path = ROOT / "cad" / "library" / "cad_geometry_draw.py"
    spec = importlib.util.spec_from_file_location("scheme_cad_geometry_draw", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载模块: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CAD_GEOMETRY_DRAW = load_cad_geometry_draw_module()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="根据坐标数据绘制建筑物外轮廓并保存为 DWG。")
    parser.add_argument("--source", required=True, help="坐标来源文件，支持 json/csv/txt/png/jpg/jpeg/bmp。")
    parser.add_argument(
        "--output",
        default=None,
        help="输出 DWG 路径；未提供时默认保存到输入文件所在目录下的 总图定位.dwg。",
    )
    parser.add_argument("--layer", default="建筑外轮廓", help="目标图层名。")
    parser.add_argument("--color", type=int, default=None, help="CAD 颜色号；默认不强制设置。")
    parser.add_argument("--label-layer", default="坐标标注", help="坐标标注所在图层。")
    parser.add_argument("--label-color", type=int, default=None, help="坐标标注颜色；默认不强制设置。")
    parser.add_argument("--text-height", type=float, default=0.45, help="坐标文字高度，单位为模型空间 1:1 单位。")
    parser.add_argument("--leader-rise", type=float, default=1.20, help="引线竖向抬升量，单位为模型空间 1:1 单位。")
    parser.add_argument("--leader-landing", type=float, default=0.60, help="引线首段水平投影，单位为模型空间 1:1 单位。")
    parser.add_argument("--leader-shoulder", type=float, default=2.40, help="引线水平肩长最小值，单位为模型空间 1:1 单位。")
    parser.add_argument("--label-gap", type=float, default=0.18, help="文字与引线之间的竖向间距，单位为模型空间 1:1 单位。")
    parser.add_argument("--ordered", action="store_true", help="声明输入点已按轮廓顺序排列。")
    parser.add_argument("--close-after-save", action="store_true", help="保存成功后关闭新建图纸。")
    parser.add_argument("--overwrite", action="store_true", help="输出已存在时允许覆盖。")
    parser.add_argument("--ocr-text", help="图片 OCR 文本文件；提供后优先使用该文本解析坐标。")
    parser.add_argument("--no-labels", action="store_true", help="只绘制外轮廓，不生成坐标标注。")
    parser.add_argument("--no-shutdown-cad", action="store_true", help="保存后不关闭整个天正/AutoCAD 进程。")
    parser.add_argument("--debug", action="store_true", help="打开 INFO 级日志。")
    return parser.parse_args()


def _point_from_any(value) -> Point3D:
    if isinstance(value, dict):
        x = value.get("x")
        y = value.get("y")
        z = value.get("z", 0.0)
        label = value.get("label")
        if x is None or y is None:
            raise ValueError(f"点对象缺少 x/y: {value!r}")
        if label:
            sys_logger.debug(f"读取点 {label}: ({x}, {y}, {z})")
        return (float(x), float(y), float(z))
    if isinstance(value, (list, tuple)):
        if len(value) < 2:
            raise ValueError(f"点坐标长度不足: {value!r}")
        z = value[2] if len(value) >= 3 else 0.0
        return (float(value[0]), float(value[1]), float(z))
    raise TypeError(f"无法识别的点格式: {value!r}")


def _dedupe_adjacent(points: Sequence[Point3D], tol: float = 1e-6) -> List[Point3D]:
    cleaned: List[Point3D] = []
    for point in points:
        if not cleaned:
            cleaned.append(point)
            continue
        last = cleaned[-1]
        if abs(point[0] - last[0]) <= tol and abs(point[1] - last[1]) <= tol and abs(point[2] - last[2]) <= tol:
            continue
        cleaned.append(point)
    if len(cleaned) > 1:
        first = cleaned[0]
        last = cleaned[-1]
        if abs(first[0] - last[0]) <= tol and abs(first[1] - last[1]) <= tol and abs(first[2] - last[2]) <= tol:
            cleaned.pop()
    return cleaned


def _polygon_area(points: Sequence[Point3D]) -> float:
    area = 0.0
    for idx, point in enumerate(points):
        nxt = points[(idx + 1) % len(points)]
        area += point[0] * nxt[1] - nxt[0] * point[1]
    return area / 2.0


def _sort_points_clockwise(points: Sequence[Point3D]) -> List[Point3D]:
    cx = sum(point[0] for point in points) / len(points)
    cy = sum(point[1] for point in points) / len(points)
    ordered = sorted(points, key=lambda point: math.atan2(point[1] - cy, point[0] - cx), reverse=True)
    if _polygon_area(ordered) > 0:
        ordered.reverse()
    return ordered


def _normalize_points(points: Iterable[Point3D], preserve_order: bool) -> List[Point3D]:
    prepared = _dedupe_adjacent([_point_from_any(point) for point in points])
    if len(prepared) < 3:
        raise ValueError("至少需要 3 个点才能绘制闭合轮廓。")
    if preserve_order:
        if _polygon_area(prepared) > 0:
            prepared.reverse()
        return prepared
    return _sort_points_clockwise(prepared)


def _variant_point(point: Point3D):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [point[0], point[1], point[2]])


def _to_model_point(geo_point: Point3D) -> Point3D:
    # 大地坐标按 (X, Y) 提供，但写入 CAD 模型空间时需要映射成 (x, y) = (Y, X)。
    return (geo_point[1], geo_point[0], geo_point[2])


def _to_model_points(geo_points: Sequence[Point3D]) -> List[Point3D]:
    return [_to_model_point(point) for point in geo_points]


def _bbox(points: Sequence[Point3D]) -> tuple[float, float, float, float]:
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return min(xs), min(ys), max(xs), max(ys)


def _ensure_layer(layer_name: str) -> None:
    if not layer_name:
        return
    doc = C.raw_doc
    for idx in range(6):
        try:
            doc.Layers.Item(layer_name)
            return
        except Exception:
            try:
                doc.Layers.Add(layer_name)
                return
            except Exception:
                if idx == 5:
                    raise
                time.sleep(0.6)


def _run_with_retries(action, *, retries: int = 8, delay: float = 0.8, action_name: str = "cad_action"):
    last_error = None
    for _ in range(retries):
        try:
            return action()
        except Exception as exc:
            last_error = exc
            time.sleep(delay)
    raise RuntimeError(f"{action_name} 多次重试后仍失败: {last_error}")


def _draw_text_line(text: str, insert_point: Point3D, height: float, layer: str | None, color: int | None):
    text_obj = _run_with_retries(
        lambda: C.raw_doc.ModelSpace.AddText(str(text), _variant_point(insert_point), float(height)),
        action_name="add_text",
    )
    if layer:
        try:
            text_obj.Layer = layer
        except Exception:
            pass
    if color is not None:
        try:
            text_obj.Color = int(color)
        except Exception:
            pass
    return text_obj


def _build_coordinate_label(point: Point3D) -> tuple[str, str]:
    return (f"X {point[0]:.3f}", f"Y {point[1]:.3f}")


def _make_label_spec(
    point: Point3D,
    centroid: Point3D,
    text_height: float,
    leader_rise: float,
    leader_landing: float,
    leader_shoulder: float,
    label_gap: float,
) -> dict:
    text_x, text_y = _build_coordinate_label(point)
    text_width_est = max(len(text_x), len(text_y)) * text_height * 0.62
    shoulder = max(float(leader_shoulder), text_width_est + text_height * 0.9)

    dir_x = 1.0 if point[0] >= centroid[0] else -1.0
    dir_y = 1.0 if point[1] >= centroid[1] else -1.0

    knee = (
        point[0] + dir_x * float(leader_landing),
        point[1] + dir_y * float(leader_rise),
        point[2],
    )
    tail = (
        knee[0] + dir_x * shoulder,
        knee[1],
        knee[2],
    )
    text_origin = (
        min(knee[0], tail[0]),
        knee[1] + float(label_gap),
        point[2],
    )
    second_line = (
        text_origin[0],
        text_origin[1] + text_height * 1.35,
        point[2],
    )
    return {
        "leader_points": [point, knee, tail],
        "text_origin_lower": text_origin,
        "text_origin_upper": second_line,
        "text_x": text_x,
        "text_y": text_y,
    }


def _extract_xy_pairs(text: str) -> List[Point3D]:
    normalized = text.replace("\r", "\n")
    pairs = re.findall(
        r"[Xx]\s*[:=]?\s*(-?\d+(?:\.\d+)?)\s*[\n ,;，；]*[Yy]\s*[:=]?\s*(-?\d+(?:\.\d+)?)",
        normalized,
        flags=re.MULTILINE,
    )
    if pairs:
        return [(float(x), float(y), 0.0) for x, y in pairs]

    loose_pairs = re.findall(r"(-?\d+(?:\.\d+)?)\s*[, ]+\s*(-?\d+(?:\.\d+)?)", normalized)
    if loose_pairs:
        return [(float(x), float(y), 0.0) for x, y in loose_pairs]

    return []


def _load_json_points(path: Path) -> tuple[List[Point3D], bool]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return [_point_from_any(item) for item in payload], False
    if not isinstance(payload, dict):
        raise ValueError("JSON 顶层必须是对象或数组。")

    for key in ("points", "vertices", "coordinates", "outline"):
        if key in payload:
            ordered = bool(payload.get("ordered", False))
            return [_point_from_any(item) for item in payload[key]], ordered
    raise ValueError("JSON 中未找到 points/vertices/coordinates/outline 字段。")


def _load_csv_points(path: Path) -> tuple[List[Point3D], bool]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(2048)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample)
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(handle, dialect=dialect)
        if reader.fieldnames:
            rows = []
            for row in reader:
                x = row.get("x") or row.get("X")
                y = row.get("y") or row.get("Y")
                z = row.get("z") or row.get("Z") or 0.0
                if x is None or y is None:
                    continue
                seq = row.get("seq") or row.get("order") or row.get("index")
                rows.append((int(seq) if seq not in (None, "") else 10**9, (float(x), float(y), float(z))))
            rows.sort(key=lambda item: item[0])
            return [item[1] for item in rows], True

        handle.seek(0)
        plain_reader = csv.reader(handle, dialect=dialect)
        points: List[Point3D] = []
        for row in plain_reader:
            if len(row) < 2:
                continue
            z = float(row[2]) if len(row) >= 3 and row[2] not in ("", None) else 0.0
            points.append((float(row[0]), float(row[1]), z))
        return points, True


def _ocr_image_to_text(image_path: Path) -> str:
    try:
        import pytesseract
        from PIL import Image

        return pytesseract.image_to_string(Image.open(image_path), lang="eng", config="--psm 6")
    except Exception:
        pass

    try:
        result = subprocess.run(
            ["tesseract", str(image_path), "stdout", "-l", "eng", "--psm", "6"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except Exception as exc:
        raise RuntimeError(
            "无法自动 OCR 图片，请提供 --ocr-text 文本文件，或安装 pytesseract/tesseract。"
        ) from exc


def _load_text_like_points(path: Path) -> tuple[List[Point3D], bool]:
    text = path.read_text(encoding="utf-8")
    points = _extract_xy_pairs(text)
    if not points:
        raise ValueError(f"未能从文本中识别坐标: {path}")
    return points, False


def _load_image_points(path: Path, ocr_text: str | None) -> tuple[List[Point3D], bool]:
    if ocr_text:
        text = Path(ocr_text).read_text(encoding="utf-8")
    else:
        sidecars = [
            path.with_suffix(".txt"),
            path.with_name(path.stem + ".ocr.txt"),
            path.with_name(path.stem + ".json"),
            path.with_name(path.stem + ".csv"),
        ]
        for sidecar in sidecars:
            if not sidecar.exists():
                continue
            if sidecar.suffix.lower() == ".json":
                return _load_json_points(sidecar)
            if sidecar.suffix.lower() == ".csv":
                return _load_csv_points(sidecar)
            text = sidecar.read_text(encoding="utf-8")
            points = _extract_xy_pairs(text)
            if points:
                return points, False
        text = _ocr_image_to_text(path)

    points = _extract_xy_pairs(text)
    if not points:
        raise ValueError(f"未能从图片 OCR 文本中提取坐标: {path}")
    return points, False


def load_points_from_source(source: Path, ocr_text: str | None) -> tuple[List[Point3D], bool]:
    suffix = source.suffix.lower()
    if suffix == ".json":
        return _load_json_points(source)
    if suffix == ".csv":
        return _load_csv_points(source)
    if suffix in {".txt", ".dat"}:
        return _load_text_like_points(source)
    if suffix in {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}:
        return _load_image_points(source, ocr_text)
    raise ValueError(f"暂不支持的输入格式: {source.suffix}")


def ensure_output_ready(output_path: Path, overwrite: bool) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not output_path.exists():
        return
    if not overwrite:
        raise FileExistsError(f"输出文件已存在，请增加 --overwrite: {output_path}")
    try:
        output_path.unlink()
    except PermissionError as exc:
        raise PermissionError(f"无法覆盖现有文件，可能正被 CAD 占用: {output_path}") from exc


def resolve_output_path(source: Path, explicit_output: str | None) -> Path:
    if explicit_output:
        return Path(explicit_output).resolve()
    return (source.parent / "总图定位.dwg").resolve()


def create_fresh_document() -> str:
    C.li()
    acad = C.acad
    current_name = C.raw_doc.Name
    new_doc = acad.Documents.Add()
    last_error = None
    for _ in range(8):
        try:
            new_doc.Activate()
            break
        except Exception as exc:
            last_error = exc
            time.sleep(0.6)
    else:
        raise RuntimeError(f"新图纸激活失败: {last_error}")
    time.sleep(0.6)
    if not C.li():
        raise RuntimeError("新建图纸后无法刷新 CAD 连接。")
    sys_logger.info(f"已从 {current_name} 切换到新图纸 {C.raw_doc.Name}")
    return C.raw_doc.Name


def draw_outline(points: Sequence[Point3D], layer: str, color: int):
    model_points = _to_model_points(points)

    def _draw():
        poly = CAD_GEOMETRY_DRAW.draw_lwpolyline_wcs(
            model_points,
            closed=True,
            layer=layer,
            color=color,
            target_space="ModelSpace",
        )
        if poly is None:
            raise RuntimeError("LWPolyline 返回 None")
        return poly

    polyline = _run_with_retries(
        _draw,
        action_name="draw_outline",
    )
    try:
        C.raw_doc.Regen(1)
    except Exception:
        pass
    return polyline


def annotate_points(
    points: Sequence[Point3D],
    label_layer: str,
    label_color: int | None,
    text_height: float,
    leader_rise: float,
    leader_landing: float,
    leader_shoulder: float,
    label_gap: float,
) -> None:
    if not points:
        return

    _ensure_layer(label_layer)
    model_points = _to_model_points(points)
    x1, y1, x2, y2 = _bbox(model_points)
    centroid = ((x1 + x2) / 2.0, (y1 + y2) / 2.0, 0.0)

    for geo_point, model_point in zip(points, model_points):
        spec = _make_label_spec(
            model_point,
            centroid,
            text_height=text_height,
            leader_rise=leader_rise,
            leader_landing=leader_landing,
            leader_shoulder=leader_shoulder,
            label_gap=label_gap,
        )
        def _draw_leader():
            poly = CAD_GEOMETRY_DRAW.draw_lwpolyline_wcs(
                spec["leader_points"],
                closed=False,
                layer=label_layer,
                color=label_color,
                target_space="ModelSpace",
            )
            if poly is None:
                raise RuntimeError("leader 返回 None")
            return poly
        leader = _run_with_retries(
            _draw_leader,
            action_name="draw_leader",
        )
        _draw_text_line(
            _build_coordinate_label(geo_point)[0],
            spec["text_origin_upper"],
            height=text_height,
            layer=label_layer,
            color=label_color,
        )
        _draw_text_line(
            _build_coordinate_label(geo_point)[1],
            spec["text_origin_lower"],
            height=text_height,
            layer=label_layer,
            color=label_color,
        )

    try:
        C.raw_doc.Regen(1)
    except Exception:
        pass


def save_document(output_path: Path, close_after_save: bool) -> None:
    if not C.save_file_as(str(output_path)):
        raise RuntimeError(f"DWG 保存失败: {output_path}")
    if close_after_save:
        time.sleep(0.6)
        if not C.close_dwg_by_name(output_path.name):
            if not C.close_file("no_save"):
                raise RuntimeError("保存后关闭图纸失败。")
        try:
            C.li()
        except Exception:
            pass


def shutdown_cad_application(force: bool = True) -> None:
    acad = C.acad
    hwnd = None
    pid = None
    try:
        hwnd = acad.HWND
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
    except Exception:
        pass

    try:
        docs = acad.Documents
        for _ in range(10):
            if docs.Count <= 0:
                break
            doc = docs.Item(docs.Count - 1)
            try:
                doc.Close(False)
            except Exception:
                time.sleep(0.6)
    except Exception:
        pass

    try:
        acad.Quit()
    except Exception:
        pass

    if pid:
        deadline = time.time() + 6.0
        while time.time() < deadline:
            if not psutil.pid_exists(pid):
                return
            time.sleep(0.5)

    if force and pid:
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        deadline = time.time() + 8.0
        while time.time() < deadline:
            if not psutil.pid_exists(pid):
                return
            time.sleep(0.5)
        raise RuntimeError(f"CAD 进程 {pid} 在 taskkill 后仍未退出。")

    raise RuntimeError("无法确认 CAD 已完全退出。")


def main() -> int:
    args = parse_args()
    set_debug_mode(mode=1 if args.debug else 0, who="AI", wait_time=0)

    source = Path(args.source).resolve()
    if not source.exists():
        raise FileNotFoundError(f"输入文件不存在: {source}")
    output_path = resolve_output_path(source, args.output)

    raw_points, source_ordered = load_points_from_source(source, args.ocr_text)
    preserve_order = args.ordered or source_ordered
    points = _normalize_points(raw_points, preserve_order=preserve_order)

    sys_logger.info(f"读取到 {len(points)} 个轮廓点，preserve_order={preserve_order}")
    ensure_output_ready(output_path, overwrite=args.overwrite)
    create_fresh_document()
    draw_outline(points, layer=args.layer, color=args.color)
    if not args.no_labels:
        annotate_points(
            points,
            label_layer=args.label_layer,
            label_color=args.label_color,
            text_height=float(args.text_height),
            leader_rise=float(args.leader_rise),
            leader_landing=float(args.leader_landing),
            leader_shoulder=float(args.leader_shoulder),
            label_gap=float(args.label_gap),
        )
    save_document(output_path, close_after_save=args.close_after_save)
    if not args.no_shutdown_cad:
        shutdown_cad_application(force=True)

    sys_logger.info(f"建筑外轮廓已保存: {output_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        sys_logger.error(f"绘制失败: {exc}")
        raise
