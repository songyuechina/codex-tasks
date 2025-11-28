from __future__ import annotations
from pathlib import Path
import sys

TARCH_ROOT = Path(__file__).resolve().parents[1]
if str(TARCH_ROOT) not in sys.path:
    sys.path.insert(0, str(TARCH_ROOT))
from run_tarch_demo import main as run_main

if __name__ == "__main__":
    args = ["draw_tarch_wall", *sys.argv[1:]]
    run_main(args)
