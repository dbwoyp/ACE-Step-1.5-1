"""Wiring helpers for Gradio event registration.

This package exposes typed context builders eagerly and resolves handler
registration callables lazily to avoid importing optional UI dependencies
during lightweight test collection.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

from .context import (
    GenerationWiringContext,
    TrainingWiringContext,
    build_auto_checkbox_inputs,
    build_auto_checkbox_outputs,
    build_mode_ui_outputs,
)

_LAZY_EXPORTS: dict[str, tuple[str, str]] = {
    "register_generation_metadata_handlers": (
        ".generation_metadata_wiring",
        "register_generation_metadata_handlers",
    ),
    "register_generation_metadata_file_handlers": (
        ".generation_metadata_file_wiring",
        "register_generation_metadata_file_handlers",
    ),
    "register_generation_batch_navigation_handlers": (
        ".generation_batch_navigation_wiring",
        "register_generation_batch_navigation_handlers",
    ),
    "register_generation_mode_handlers": (".generation_mode_wiring", "register_generation_mode_handlers"),
    "register_generation_run_handlers": (".generation_run_wiring", "register_generation_run_handlers"),
    "register_results_aux_handlers": (".results_aux_wiring", "register_results_aux_handlers"),
    "register_results_restore_and_lrc_handlers": (
        ".results_display_wiring",
        "register_results_restore_and_lrc_handlers",
    ),
    "register_results_save_button_handlers": (".results_display_wiring", "register_results_save_button_handlers"),
    "register_generation_service_handlers": (".generation_service_wiring", "register_generation_service_handlers"),
    "register_training_dataset_builder_handlers": (
        ".training_dataset_builder_wiring",
        "register_training_dataset_builder_handlers",
    ),
    "register_training_dataset_load_handler": (
        ".training_dataset_preprocess_wiring",
        "register_training_dataset_load_handler",
    ),
    "register_training_preprocess_handler": (
        ".training_dataset_preprocess_wiring",
        "register_training_preprocess_handler",
    ),
    "register_training_run_handlers": (".training_run_wiring", "register_training_run_handlers"),
}


def _resolve_lazy_export(name: str) -> Any:
    """Return a lazily-imported wiring symbol and cache it on this module.

    Args:
        name: Public symbol requested from this module.

    Returns:
        Any: The resolved attribute from the target wiring submodule.

    Raises:
        AttributeError: If ``name`` is not a supported public export.
    """
    module_and_symbol = _LAZY_EXPORTS.get(name)
    if module_and_symbol is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module_name, symbol_name = module_and_symbol
    module = import_module(module_name, __name__)
    resolved = getattr(module, symbol_name)
    globals()[name] = resolved
    return resolved


def __getattr__(name: str) -> Any:
    """Resolve known handler exports lazily on first attribute access."""
    return _resolve_lazy_export(name)


def __dir__() -> list[str]:
    """Return module attributes including lazy exports for introspection."""
    return sorted(set(globals()) | set(_LAZY_EXPORTS))


__all__ = [
    "GenerationWiringContext",
    "TrainingWiringContext",
    "build_auto_checkbox_inputs",
    "build_auto_checkbox_outputs",
    "build_mode_ui_outputs",
    *_LAZY_EXPORTS.keys(),
]
