"""
Plot Polar Bar Evolution Example.
=============================================
"""
import os
import pandas as pd
from templot import plot_polar_bar_evolution, add_regions, download_irep


filepath = os.path.join('..', 'templot', 'data', 'df.csv')

if not os.path.exists(filepath):
    download_irep(filepath)

df = pd.read_csv(filepath)
df = add_regions(df, "LLX", "LLY")


df = pd.melt(
    df,
    id_vars=['Identifiant', 'Nom_Etablissement_x', 'LLX', 'LLY', 'Regions'],
    var_name='Annee',
    value_name='Quantite',
)
df = df[df.Quantite != 0]
df['Annee'] = df['Annee'].apply(lambda x: x[-4:])
anim = plot_polar_bar_evolution(df, var="Quantite", year="Annee")

# visualize the html results in sphinx gallery
tmp_dir = os.path.join('..', 'dist', 'html')
if os.path.exists(tmp_dir):
    anim.save(
        os.path.join(tmp_dir, 'example_polarbar_animation.gif'),
        writer='imagemagick',
    )


####################################
# .. raw:: html
#
#     <img src="../example_polarbar_animation.gif" height="620px" width="100%">
