#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.runtime import main_for_role


if __name__ == "__main__":
    main_for_role(Path(__file__).with_name("role.toml"))
