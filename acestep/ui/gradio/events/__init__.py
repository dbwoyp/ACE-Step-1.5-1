"""Gradio UI event-handlers facade.

This module wires generation, results, and training callbacks while avoiding
import-time loading of optional heavy UI dependencies.
"""

from __future__ import annotations

from . import wiring


def setup_event_handlers(demo, dit_handler, llm_handler, dataset_handler, dataset_section, generation_section, results_section):
    """Setup generation/results event wiring for the Gradio UI.

    Args:
        demo (Any): Root Gradio demo/container used to register events.
        dit_handler (Any): Inference service used by generation/results callbacks.
        llm_handler (Any): LLM service used by metadata/text callbacks.
        dataset_handler (Any): Dataset service used by generation wiring.
        dataset_section (dict[str, Any]): Dataset UI component map.
        generation_section (dict[str, Any]): Generation UI component map.
        results_section (dict[str, Any]): Results UI component map.

    Returns:
        None: Registers event handlers in-place on the supplied components.
    """
    wiring_context = wiring.GenerationWiringContext(
        demo=demo,
        dit_handler=dit_handler,
        llm_handler=llm_handler,
        dataset_handler=dataset_handler,
        dataset_section=dataset_section,
        generation_section=generation_section,
        results_section=results_section,
    )

    auto_checkbox_inputs, auto_checkbox_outputs = wiring.register_generation_service_handlers(
        wiring_context
    )
    mode_ui_outputs = wiring.build_mode_ui_outputs(wiring_context)
    wiring.register_generation_metadata_handlers(
        wiring_context,
        auto_checkbox_inputs=auto_checkbox_inputs,
        auto_checkbox_outputs=auto_checkbox_outputs,
    )

    wiring.register_generation_mode_handlers(
        wiring_context,
        mode_ui_outputs=mode_ui_outputs,
        auto_checkbox_inputs=auto_checkbox_inputs,
        auto_checkbox_outputs=auto_checkbox_outputs,
    )

    wiring.register_generation_metadata_file_handlers(
        wiring_context,
        auto_checkbox_inputs=auto_checkbox_inputs,
        auto_checkbox_outputs=auto_checkbox_outputs,
    )
    wiring.register_results_save_button_handlers(wiring_context)
    wiring.register_results_aux_handlers(
        wiring_context,
        mode_ui_outputs=mode_ui_outputs,
    )
    wiring.register_generation_run_handlers(wiring_context)
    wiring.register_generation_batch_navigation_handlers(wiring_context)
    wiring.register_results_restore_and_lrc_handlers(wiring_context)


def setup_training_event_handlers(demo, dit_handler, llm_handler, training_section):
    """Setup event handlers for the training tab (dataset builder and LoRA training)."""
    training_context = wiring.TrainingWiringContext(
        demo=demo,
        dit_handler=dit_handler,
        llm_handler=llm_handler,
        training_section=training_section,
    )

    wiring.register_training_dataset_load_handler(
        training_context,
        button_key="load_json_btn",
        path_key="load_json_path",
        status_key="load_json_status",
    )
    wiring.register_training_dataset_builder_handlers(training_context)

    wiring.register_training_dataset_load_handler(
        training_context,
        button_key="load_existing_dataset_btn",
        path_key="load_existing_dataset_path",
        status_key="load_existing_status",
    )

    wiring.register_training_preprocess_handler(training_context)
    wiring.register_training_run_handlers(training_context)
