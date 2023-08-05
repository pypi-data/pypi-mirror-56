"""
Unit tests for ``plot_aggregated_map``.
"""
import unittest
from templot import plot_pie_chart_interactive, download_irep, add_regions
import os
import pandas as pd


class TestPlotPieChart(unittest.TestCase):
    "Tests for plot_pie_chart_interactive"
    filepath = os.path.join('tests', 'df_test.csv')

    if not os.path.exists(filepath):
        download_irep(filepath)
        df = pd.read_csv(filepath)
        df = add_regions(
            df, "LLX", "LLY", add=["regions", "departements", "communes"]
        )
        df.to_csv(filepath, index=False)

    df = pd.read_csv(filepath)

    def test_bad_df(self):
        with self.assertRaises(TypeError):
            df = []
            plot_pie_chart_interactive(df, "Quantite", 2004, 2005, "Regions")

    def test_bad_col(self):
        with self.assertRaises(ValueError):
            plot_pie_chart_interactive(
                self.df,
                col="Quantit",
                year=2004,
                year1=2005,
                sticker="Regions",
            )

    def test_bad_year(self):
        with self.assertRaises(ValueError):
            plot_pie_chart_interactive(
                self.df, col="Quantite", year=20, year1=2005, sticker="Regions"
            )

    def test_bad_year1(self):
        with self.assertRaises(ValueError):
            plot_pie_chart_interactive(
                self.df,
                col="Quantite",
                year=2004,
                year1=2025,
                sticker="Regions",
            )

    def test_bad_sticker(self):
        with self.assertRaises(ValueError):
            plot_pie_chart_interactive(
                self.df, col="Quantite", year=2004, year1=2025, sticker="LLX"
            )


if __name__ == '__main__':
    unittest.main()
