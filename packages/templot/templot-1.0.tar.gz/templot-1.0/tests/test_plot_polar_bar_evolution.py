"""
Unit tests for ``plot_polar_bar_evolution``.
"""
import unittest
from templot import plot_polar_bar_evolution, download_irep, add_regions
import os
import pandas as pd


class TestPlotPolarBarEvolution(unittest.TestCase):
    "Tests for submodule plot_polar_bar_evolution"
    filepath = os.path.join('tests', 'df_test.csv')

    if not os.path.exists(filepath):
        download_irep(filepath)
        df = pd.read_csv(filepath)
        df = add_regions(
            df, "LLX", "LLY", add=["regions", "departements", "communes"]
        )
        df.to_csv(filepath, index=False)

    df = pd.read_csv(filepath)

    def test_empty(self):
        with self.assertRaises(TypeError):
            df = []
            plot_polar_bar_evolution(df)

    def test_bad_year(self):
        with self.assertRaises(ValueError):
            plot_polar_bar_evolution(
                self.df,
                var="Quantite",
                year="annee",
                group="Regions",
                agr="average",
            )

    def test_bad_group(self):
        with self.assertRaises(ValueError):
            plot_polar_bar_evolution(
                self.df,
                var="Quantite",
                year="Annee",
                group="Departement",
                agr="average",
            )

    def test_bad_agr(self):
        with self.assertRaises(ValueError):
            plot_polar_bar_evolution(
                self.df,
                var="Quantite",
                year="Annee",
                group="Regions",
                agr="averag",
            )


if __name__ == '__main__':
    unittest.main()
