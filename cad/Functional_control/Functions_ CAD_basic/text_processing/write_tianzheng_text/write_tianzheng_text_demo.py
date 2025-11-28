from __future__ import annotations
from pathlib import Path
import sys

TEXT_ROOT = Path(__file__).resolve().parents[1]
runner = TEXT_ROOT / "run_text_demo.py"
if str(TEXT_ROOT) not in sys.path:
    sys.path.insert(0, str(TEXT_ROOT))
from run_text_demo import main as run_main

if __name__ == "__main__":
    args = ["write_tianzheng_text", *sys.argv[1:]]
    run_main(args)
