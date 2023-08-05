"""
Plots an Interactive pie chart.
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_pie_chart_interactive(df, col, year, year1, sticker):

    """
    Plots an interactive pie chart of sticker by col.

    :param df: data
    :param col: column of df (omitting the year)
    :param year: the first year
    :param year1: the second year
    :param sticker: column of df (the individuals in the pie chart)
    :return: Plotly figure

    One example of this simple graph:

    .. raw:: html

        <iframe src="example_ipchar.html" height="800px" width="100%"></iframe>

    """
    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError(f"df must be a DataFrame not {type(df)}.")

    if len(df.shape) != 2:
        raise ValueError(f"df must be a matrix but shape is {df.shape}")

    if df.shape[1] < 3:
        raise ValueError(
            f"df must be a matrix with at least three columns but shape is {df.shape}"
        )
    if type(year) != int:
        raise ValueError(f"{year} must be an integer.")
    if type(year1) != int:
        raise ValueError(f"{year} must be an integer.")
    if type(col) != str:
        raise ValueError(f"{col} must be a string.")

    if year not in range(2003, 2018):
        raise ValueError(
            f"{year} is not a valid year. It must be between 2003 and 2018"
        )

    if year1 not in range(2003, 2018):
        raise ValueError(
            f"{year1} is not a valid year. It must be between 2003 and 2018"
        )

    if col + str(year) not in df.columns:
        raise ValueError(f"{col+str(year)} is not a valid column name.")

    if col + str(year1) not in df.columns:
        raise ValueError(f"{col+str(year1)} is not a valid column name.")

    if df[col + str(year)].dtype != "float64":
        raise ValueError(
            f"{col + str(year1)} must contain numeric values, specifically float64."
        )

    if df[col + str(year1)].dtype != "float64":
        raise ValueError(
            f"{col + str(year1)} must contain numeric values, specifically float64."
        )

    if sticker not in df.columns:
        raise ValueError(
            f"{sticker} is not a valid column name. Please consider adding it to your data frame if it doesn't figure yet"
        )

    if df[sticker].dtype != "O":
        raise ValueError(f"{sticker} must contain string values.")

    if sticker not in ["Regions", "Departements", "Communes"]:
        raise ValueError(
            f"{sticker} is not a valid name. Possible values are: Regions, Departements or Communes "
        )

    test = list(set(df[sticker]))
    d1 = {key: 0 for key in test}
    d = {key: 0 for key in test}
    label, label1 = col + str(year), col + str(year1)
    for i in df.index:
        d[df.loc[i, sticker]] += df.loc[i, label]
        d1[df.loc[i, sticker]] += df.loc[i, label1]
    labels = list(d.keys())
    values = list(d.values())
    labels1 = list(d1.keys())
    values1 = list(d1.values())
    fig = make_subplots(
        rows=2, cols=1, specs=[[{'type': 'domain'}], [{'type': 'domain'}]]
    )
    fig.add_trace(go.Pie(labels=labels, values=values, name=year), 1, 1)
    fig.add_trace(go.Pie(labels=labels1, values=values1, name=year1), 2, 1)
    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(
        title_text="Percentage of "
        + col.lower()
        + f" per {sticker} in two years.",
        # Add annotations in the center of the donut pies.
        annotations=[
            dict(text=year, x=0.5, y=0.82, font_size=20, showarrow=False),
            dict(text=year1, x=0.5, y=0.18, font_size=20, showarrow=False),
        ],
    )
    return fig
