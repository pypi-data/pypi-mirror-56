"""
Plot Interactive polar bar.
"""

import plotly.express as px
import pandas as pd
import warnings


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

    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError(f"df must be a dfFrame not {type(df)}.")

    if len(df.shape) != 2:
        raise ValueError(f"df must be a matrix but shape is {df.shape}")

    if df.shape[1] < 2:
        raise ValueError(
            f"df must be a matrix with at least two columns but shape is {df.shape}"
        )

    if var not in df.columns:
        raise ValueError(f"{var} is not a valid column name.")

    if df[var].dtype not in [
        'int16',
        'int32',
        'int64',
        'float16',
        'float32',
        'float64',
    ]:
        raise ValueError(f"{var} must contain numeric values.")

    if year not in df.columns:
        raise ValueError(f"{year} is not a valid column name.")

    if group not in df.columns:
        raise ValueError(f"{group} is not a valid column name.")

    if group not in ["Regions", "Departements", "Communes"]:
        raise ValueError(
            f"{group} is not a valid name. Possible values are: Regions, Departements or Communes"
        )

    if len(df[group].unique()) > 90:
        warnings.warn(
            f"Having too many groups may result in reduced performance."
        )

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

    if agr not in aggregates:
        raise ValueError(
            f"{agr} is not a valid aggregation method. Possible values are: {', '.join([k for k in aggregates])}"
        )

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
