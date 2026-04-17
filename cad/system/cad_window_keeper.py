#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sys
import time
from pathlib import Path

current = Path(__file__).resolve()
while current.name != "cad":
    if current.parent == current:
        raise RuntimeError("找不到 cad 根目录")
    current = current.parent
if str(current) not in sys.path:
    sys.path.insert(0, str(current))

from system.CAD_core import _resize_windows_for_background_use  # noqa: E402


LOG_FILE = Path(__file__).parent / "cad_window_keeper.log"
LOCK_FILE = Path(__file__).parent / "cad_window_keeper.lock"
CHECK_INTERVAL_SEC = 1.0
CAD_PROCESS_NAMES = ("acad.exe",)
WPS_PROCESS_NAMES = ("wps.exe", "wpspdf.exe", "ksolaunch.exe")
WPS_TITLE_KEYWORDS = ("wps office", "wps pdf", "kingsoft")


logger = logging.getLogger("cad_window_keeper")
logger.setLevel(logging.INFO)
logger.handlers = []
file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-5s %(message)s"))
logger.addHandler(file_handler)


def acquire_single_instance() -> None:
    if LOCK_FILE.exists():
        try:
            existing_pid = int(LOCK_FILE.read_text(encoding="utf-8").strip() or "0")
        except Exception:
            existing_pid = 0
        if existing_pid > 0:
            try:
                os.kill(existing_pid, 0)
                raise SystemExit(0)
            except OSError:
                pass
    LOCK_FILE.write_text(str(os.getpid()), encoding="utf-8")


def release_single_instance() -> None:
    try:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()
    except Exception:
        pass


def main() -> int:
    acquire_single_instance()
    logger.info("cad_window_keeper started pid=%s", os.getpid())
    try:
        while True:
            try:
                cad_result = _resize_windows_for_background_use(
                    process_names=CAD_PROCESS_NAMES,
                    corner="top-right",
                )
                wps_result = _resize_windows_for_background_use(
                    process_names=WPS_PROCESS_NAMES,
                    title_keywords=WPS_TITLE_KEYWORDS,
                    corner="bottom-right",
                )
                if cad_result.get("moved") or wps_result.get("moved"):
                    logger.info(
                        "window_layout enforced cad=%s/%s wps=%s/%s",
                        cad_result.get("moved"),
                        cad_result.get("observed"),
                        wps_result.get("moved"),
                        wps_result.get("observed"),
                    )
            except Exception as exc:
                logger.warning("window_layout loop failed: %s", exc)
            time.sleep(CHECK_INTERVAL_SEC)
    finally:
        release_single_instance()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
