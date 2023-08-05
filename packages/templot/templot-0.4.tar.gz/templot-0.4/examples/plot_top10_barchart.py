"""
Plot Top 10 Barchart Example
============================
"""

import os
from templot import add_regions, download_irep, plot_top10_barchart
import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt

# Preparing the data
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
df['Annee'] = df['Annee'].apply(lambda x: int(x[-4:]))
# Delete a few outliers/incorrect values
df.drop(df.index[[80330, 78118, 73525]], inplace=True)

# Plot animation from 2003 to 2017 :
fig, ax = plt.subplots(figsize=(16, 9), dpi=220, facecolor='#F8F7F7')
ani = animation.FuncAnimation(
    fig,
    plot_top10_barchart,
    frames=range(2003, 2018),
    interval=1500,
    fargs=[
        df,
        "Quantite",
        "Annee",
        "Regions",
        'Nom_Etablissement_x',
        'Les établissement émettant le plus de déchets dangereux de 2003 à 2017',
        'Déchets dangereux (t/an)',
    ],
)

# visualize the result gif in sphinx gallery
tmp_dir = os.path.join('..', 'dist', 'html')
if os.path.exists(tmp_dir):
    ani.save(
        os.path.join(tmp_dir, "example_top10.gif"),
        writer="imagemagick",
        savefig_kwargs={'facecolor': '#F8F7F7'},
    )


####################################
# .. raw:: html
#
#     <img src="../example_top10.gif" height="620px" width="100%">
