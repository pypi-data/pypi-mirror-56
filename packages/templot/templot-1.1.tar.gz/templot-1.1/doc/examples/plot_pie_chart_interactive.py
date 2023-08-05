"""
Plots an interactive Pie chart Example.
=========================================
"""

import os
import pandas as pd
import plotly
from templot import plot_pie_chart_interactive, add_regions, download_irep


filepath = os.path.join('..', 'templot', 'data', 'df.csv')

if not os.path.exists(filepath):
    download_irep(filepath)

df = pd.read_csv(filepath)
df = add_regions(df, "LLX", "LLY")

fig = plot_pie_chart_interactive(df, "Quantite", 2004, 2005, "Regions")

# visualize the html results in sphinx gallery
tmp_dir = os.path.join('..', 'dist', 'html')
if os.path.exists(tmp_dir):
    plotly.offline.plot(
        fig,
        filename=os.path.join(tmp_dir, 'example_ipchar.html'),
        auto_open=False,
    )

####################################
# .. raw:: html
#
#     <iframe src="../example_ipchar.html" height="800px" width="100%"></iframe>
