from __future__ import annotations
from pathlib import Path
import sys

BLOCK_ROOT = Path(__file__).resolve().parents[1]
if str(BLOCK_ROOT) not in sys.path:
    sys.path.insert(0, str(BLOCK_ROOT))
from run_block_demo import main as run_main

if __name__ == "__main__":
    args = ["extract_nonblock_entities_from_block", *sys.argv[1:]]
    run_main(args)
