#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CAD library package entry.

Keep the package root lightweight. Submodules are loaded lazily so callers can
import `library.<module>` without paying the cost of eagerly importing every
business module up front.
"""

from importlib import import_module

_SUBMODULES = {
    "cad_annotation",
    "cad_blocks",
    "cad_control",
    "cad_geometry_draw",
    "cad_geometry_polyline",
    "cad_geometry_segment",
    "cad_objects",
    "Databaseoperation",
    "tarch_building",
    "tarch_operation",
}

__all__ = sorted(_SUBMODULES)


def __getattr__(name):
    if name not in _SUBMODULES:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(f".{name}", __name__)
    globals()[name] = module
    return module


def __dir__():
    return sorted(set(globals()) | _SUBMODULES)
