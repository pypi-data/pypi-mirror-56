"""
Plot Aggregated Map Example.
============================
"""
import os
import pandas as pd
from templot import plot_aggregated_map, add_regions, download_irep


filepath = os.path.join('..', 'templot', 'data', 'df.csv')
if not os.path.exists(filepath):
    if not os.path.exists(os.path.join('..', 'templot', 'data')):
        os.makedirs(os.path.join('..', 'templot', 'data'))
    download_irep(filepath)
    df = pd.read_csv(filepath)
    df = add_regions(df, "LLX", "LLY")
    df.to_csv(filepath, index=False)

df = pd.read_csv(filepath)

my_map = plot_aggregated_map(
    data=df,
    variables=[
        "Quantite2004",
        "Quantite2005",
        "Quantite2006",
        "Quantite2007",
        "Quantite2008",
        "Quantite2009",
    ],
    aggregation_method="average",
    height=300,
)

# visualize the html results in sphinx gallery
tmp_dir = os.path.join('..', 'dist', 'html')
if os.path.exists(tmp_dir):
    with open(os.path.join(tmp_dir, 'example_agrmap.html'), 'wt') as fh:
        fh.write(my_map.get_root().render())

####################################
# .. raw:: html
#
#     <iframe src="../example_agrmap.html" height="600px" width="100%"></iframe>
