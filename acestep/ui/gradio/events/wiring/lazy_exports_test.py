"""Tests for lazy export mechanics in the wiring facade module."""

import importlib
import unittest


class WiringLazyExportsTests(unittest.TestCase):
    """Validate lazy-export bookkeeping that avoids eager heavy imports."""

    def setUp(self):
        """Load module under test fresh for deterministic assertions."""
        self.module = importlib.import_module("acestep.ui.gradio.events.wiring")

    def test_all_contains_context_and_lazy_names(self):
        """Public export list should include eager context names and lazy handlers."""
        exported = set(self.module.__all__)
        self.assertIn("GenerationWiringContext", exported)
        self.assertIn("build_mode_ui_outputs", exported)
        self.assertIn("register_generation_mode_handlers", exported)

    def test_dir_includes_lazy_exports(self):
        """dir(module) should advertise lazy handler names for introspection."""
        names = set(dir(self.module))
        self.assertIn("register_training_run_handlers", names)
        self.assertIn("register_results_aux_handlers", names)


if __name__ == "__main__":
    unittest.main()
