#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Public TArch operation API.

This module is the stable external entry for high-level TArch functions under
`cad/library/tarch_operation`. Concrete implementations can stay split across
multiple files, but callers should prefer importing from this module.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from .drawing_name import write_tarch_drawing_name as _write_tarch_drawing_name
from .single_line_text import write_tarch_single_line_text as _write_tarch_single_line_text

MODULE_ROOT = Path(__file__).resolve().parent

__all__ = [
    "MODULE_ROOT",
    "list_public_functions",
    "write_tarch_drawing_name",
    "write_tarch_single_line_text",
    "write_tarch_title_mark",
    "write_tarch_text",
]


def list_public_functions() -> list[str]:
    """Return the current stable public TArch API names."""
    return [
        "write_tarch_drawing_name",
        "write_tarch_single_line_text",
        "write_tarch_title_mark",
        "write_tarch_text",
    ]


def write_tarch_drawing_name(
    drawing_name_text: str,
    target_point: Sequence[float] = (0.0, 0.0, 0.0),
    *,
    target_dwg_path: str | Path | None = None,
    plot_scale: float | int | str = 100,
    scale_text: str | None = None,
    drawing_name_height: float | None = None,
    scale_height: float | None = None,
    spacing_factor: float | None = None,
    annotation_style: str | None = None,
    text_style: str = "TARCH_CN_STANDARD",
    show_scale: bool | str = True,
    rotation_degrees: float = 0.0,
    prefix_text: str | None = None,
    layer: str | None = None,
    alignment: str = "左下",
    template_path: str | Path | None = None,
    save: bool = False,
) -> dict:
    """Write one TArch drawing-name mark."""
    return _write_tarch_drawing_name(
        drawing_name_text=drawing_name_text,
        target_point=target_point,
        target_dwg_path=target_dwg_path,
        plot_scale=plot_scale,
        scale_text=scale_text,
        drawing_name_height=drawing_name_height,
        scale_height=scale_height,
        spacing_factor=spacing_factor,
        annotation_style=annotation_style,
        text_style=text_style,
        show_scale=show_scale,
        rotation_degrees=rotation_degrees,
        prefix_text=prefix_text,
        layer=layer,
        alignment=alignment,
        template_path=template_path,
        save=save,
    )


def write_tarch_single_line_text(
    text: str,
    target_point: Sequence[float] = (0.0, 0.0, 0.0),
    *,
    target_dwg_path: str | Path | None = None,
    height: float = 3.5,
    width_factor: float = 1.0,
    rotation_degrees: float = 0.0,
    oblique_degrees: float = 0.0,
    style: str = "TARCH_CN_STANDARD",
    alignment: str = "左下",
    layer: str | None = None,
    plot_scale: float | int | str = 100,
    template_path: str | Path | None = None,
    save: bool = False,
) -> dict:
    """
    Write one TArch single-line text entity.

    This is the first stable function in the public `tarch_operation` API.
    """
    return _write_tarch_single_line_text(
        text=text,
        target_point=target_point,
        target_dwg_path=target_dwg_path,
        height=height,
        width_factor=width_factor,
        rotation_degrees=rotation_degrees,
        oblique_degrees=oblique_degrees,
        style=style,
        alignment=alignment,
        layer=layer,
        plot_scale=plot_scale,
        template_path=template_path,
        save=save,
    )


def write_tarch_text(*args, **kwargs) -> dict:
    """
    Compatibility alias for future text-family expansion.

    For now it maps directly to TArch single-line text writing.
    """
    return write_tarch_single_line_text(*args, **kwargs)


def write_tarch_title_mark(*args, **kwargs) -> dict:
    """Compatibility alias for TArch drawing-name writing."""
    return write_tarch_drawing_name(*args, **kwargs)
