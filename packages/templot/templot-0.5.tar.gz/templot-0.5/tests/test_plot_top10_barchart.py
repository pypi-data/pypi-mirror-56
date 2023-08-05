"""
Unit tests for ``plot_top10_barchart``.
"""
import unittest
from templot import plot_top10_barchart, download_irep, add_regions
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class TestPlotTop10(unittest.TestCase):
    "Tests for submodule plot_top10_barchart"

    """
    Tests if plot_top10_barchart outputs the same graph as intended by the developers.
    If the function is modified, this test will be invalid unless test.img is regenerated
    or output.png renamed to be the new test.png
    """

    def test_image_correct(self):
        filepath = os.path.join('tests', 'df_test.csv')
        if not os.path.exists(filepath):
            download_irep(filepath)
            df = pd.read_csv(filepath)
            df = add_regions(df, "LLX", "LLY")
            df.to_csv(filepath, index=False)
        df = pd.read_csv(filepath)
        df = pd.melt(
            df,
            id_vars=df.columns & [
                'Identifiant',
                'Nom_Etablissement_x',
                'LLX',
                'LLY',
                'Regions',
                'Departements',
                'Communes'
            ],
            var_name='Annee',
            value_name='Quantite',
        )
        df = df[df.Quantite != 0]
        df['Annee'] = df['Annee'].apply(lambda x: int(x[-4:]))
        fig, ax = plt.subplots(figsize=(16, 9), dpi=220, facecolor='#F8F7F7')
        plot_top10_barchart(
            2003,
            df,
            values="Quantite",
            year_var="Annee",
            color_var="Regions",
            names_var='Nom_Etablissement_x',
            title='Les établissement émettant le plus de déchets dangereux en 2017',
            label='Déchets dangereux (t/an)',
        )
        plt.savefig(os.path.join('tests', 'output.png'))
        output = mpimg.imread(os.path.join('tests', 'output.png'))
        testimg = mpimg.imread(os.path.join('tests', 'test.png'))
        self.assertFalse(False in (output == testimg))


if __name__ == '__main__':
    unittest.main()
