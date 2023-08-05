"""
Plot Interactive polar bar.
"""

import plotly.express as px


def plot_polar_bar_evolution_interactive(
    df, var, year, group="Regions", agr="average"
):

    """
    Plots an interactive animated polar bar showing the evolution of a variable by group across year.

    :param df: DataFrame
    :param var: name of the column containing the values.
    :param year: name of the column containing the year of each observation.
    :param group: group variable column name. Possible values are "Regions", "Departements", "Communes". Defaults to "Regions".
    :param aggregation_method: aggregation method. Possible values are "average", "median", "min", "max" and "count". Defaults to "average".
    :return: Plotly figure

    One example of this simple graph:

    .. raw:: html

        <iframe src="example_polarbar.html" height="620px" width="100%"></iframe>

    """

    aggregates = {
        "average": df.groupby([group, year])[var].mean().reset_index(),
        "median": df.groupby([group, year])[var].median().reset_index(),
        "max": df.groupby([group, year])[var].max().reset_index(),
        "min": df.groupby([group, year])[var].min().reset_index(),
        "count": df.groupby([group, year])[var]
        .count()
        .astype("float")
        .reset_index(),
    }

    df_agr = aggregates[agr]

    fig = px.bar_polar(
        df_agr,
        r=var,
        theta=group,
        color=group,
        animation_frame=year,
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Plasma[-2::-1],
    )
    fig.update_layout(showlegend=False)
    return fig
