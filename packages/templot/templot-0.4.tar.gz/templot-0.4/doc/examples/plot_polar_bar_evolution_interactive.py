"""
Plot Interactive Polar Bar Evolution Example.
=============================================
"""
import os
import pandas as pd
import plotly
from templot import (
    plot_polar_bar_evolution_interactive,
    add_regions,
    download_irep,
)


filepath = os.path.join('..', 'templot', 'data', 'df.csv')

if not os.path.exists(filepath):
    download_irep(filepath)
    df = pd.read_csv(filepath)
    df = add_regions(df, "LLX", "LLY")
    df.to_csv(filepath, index=False)

df = pd.read_csv(filepath)


df = pd.melt(
    df,
    id_vars=['Identifiant', 'Nom_Etablissement_x', 'LLX', 'LLY', 'Regions'],
    var_name='Annee',
    value_name='Quantite',
)
df = df[df.Quantite != 0]
df['Annee'] = df['Annee'].apply(lambda x: x[-4:])
fig = plot_polar_bar_evolution_interactive(df=df, var="Quantite", year="Annee")

# visualize the html results in sphinx gallery
tmp_dir = os.path.join('..', 'dist', 'html')
if os.path.exists(tmp_dir):
    plotly.offline.plot(
        fig,
        filename=os.path.join(tmp_dir, 'example_polarbar.html'),
        auto_open=False,
    )


####################################
# .. raw:: html
#
#     <iframe src="../example_polarbar.html" height="620px" width="100%"></iframe>
