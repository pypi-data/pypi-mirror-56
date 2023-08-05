"""
Unit tests for ``plot_polar_bar_evolution``.
"""
import unittest
from templot import plot_polar_bar_evolution


class TestPlotPolarBarEvolution(unittest.TestCase):
    "Tests for submodule plot_polar_bar_evolution"

    def test_empty(self):
        with self.assertRaises(AttributeError):
            df = []
            plot_polar_bar_evolution(df, var="Quantite", year="Annee")


if __name__ == '__main__':
    unittest.main()
