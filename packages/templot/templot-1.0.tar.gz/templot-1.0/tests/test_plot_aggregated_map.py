"""
Unit tests for ``plot_aggregated_map``.
"""
import unittest
from templot import plot_aggregated_map, download_irep, add_regions
import os
import pandas as pd


class TestPlotAggregatedMap(unittest.TestCase):
    "Tests for plot_aggregated_map"
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
            plot_aggregated_map(df, variables="Quantite2017")

    def test_bad_variables(self):
        with self.assertRaises(TypeError):
            plot_aggregated_map(
                self.df,
                variables="Quantite2017",
                group="Regions",
                aggregation_method="average",
            )

    def test_bad_group(self):
        with self.assertRaises(ValueError):
            plot_aggregated_map(
                self.df,
                variables=["Quantite2017"],
                group="Departement",
                aggregation_method="average",
            )

    def test_performance(self):
        with self.assertWarns(UserWarning):
            plot_aggregated_map(
                self.df,
                variables=["Quantite2017"],
                group="Departements",
                aggregation_method="average",
            )

    def test_bad_aggregation_method(self):
        with self.assertRaises(ValueError):
            plot_aggregated_map(
                self.df,
                variables=["Quantite2017"],
                group="Departements",
                aggregation_method="averag",
            )

    def test_bad_height(self):
        with self.assertRaises(TypeError):
            plot_aggregated_map(
                self.df,
                variables=["Quantite2017"],
                group="Regions",
                aggregation_method="average",
                height="-1",
            )

    params = [
        [["Quantite2016", "Quantite2017"], "Regions", "average", 200],
        [["Quantite2016", "Quantite2017"], "Regions", "median", 200],
        [["Quantite2016", "Quantite2017"], "Regions", "min", 200],
        [["Quantite2016", "Quantite2017"], "Regions", "max", 200],
        [["Quantite2016", "Quantite2017"], "Regions", "count", 200],
        [["Quantite2016", "Quantite2017"], "Departements", "average", 200],
        [["Quantite2016", "Quantite2017"], "Departements", "median", 200],
        [["Quantite2016", "Quantite2017"], "Departements", "min", 200],
        [["Quantite2016", "Quantite2017"], "Departements", "max", 200],
        [["Quantite2016", "Quantite2017"], "Departements", "count", 200],
    ]

    def test_combinations(self):
        for variables, group, aggregation_method, height in self.params:
            with self.subTest():
                try:
                    plot_aggregated_map(
                        self.df, variables, group, aggregation_method, height
                    )
                except Exception as e:
                    raise (e)


if __name__ == '__main__':
    unittest.main()
