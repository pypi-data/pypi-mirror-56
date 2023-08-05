"""
Unit tests for ``plot_polar_bar_evolution_interactive``.
"""
import unittest
from templot import plot_polar_bar_evolution_interactive


class TestPlotPolarBarEvolutionInteractive(unittest.TestCase):
    "Tests for submodule plot_polar_bar_evolution_interactive"

    def test_empty(self):
        with self.assertRaises(AttributeError):
            df = []
            plot_polar_bar_evolution_interactive(
                df, var="Quantite", year="Annee"
            )


if __name__ == '__main__':
    unittest.main()
