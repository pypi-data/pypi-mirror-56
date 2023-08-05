"""
Plot Top 10 Barchart
"""

import pandas as pd
import warnings
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as path_effects
import matplotlib.cm as cm
from numpy import linspace


def plot_top10_barchart(
    year,
    df,
    values,
    year_var,
    color_var,
    names_var,
    title='',
    label='',
    ax=None,
    **kwargs,
):
    """
    Plots a barchart of the top 10 values colored by group.

    :param year: year to be plotted (int)
    :param df: dataset (pandas DataFrame)
    :param values: sorting variable name (string)
    :param year_var: year variable name (string)
    :param color_var: color group variable name (string)
    :param names_var: bar labels variable name (string)
    :param title: title (string)
    :param label: label and unit of the values (string)
    :param ax: graph axes

    Gif example of this graph:

    .. raw:: html

        <img src="example_top10.gif" height="620px" width="100%">
    """

    if not isinstance(year, int):
        raise TypeError(f"year must be an int, not {type(year)}")

    if not isinstance(df, pd.core.frame.DataFrame):
        raise TypeError(f"data must be a DataFrame not {type(df)}.")

    if len(df.shape) != 2:
        raise ValueError(f"data must be a matrix but shape is {df.shape}")

    for var in [values, year_var, color_var, names_var]:
        if var not in df.columns:
            raise ValueError(f"{var} is not a valid column name.")

    if not isinstance(title, str):
        raise TypeError(f"title must be a string not {type(title)}.")

    if not isinstance(label, str):
        raise TypeError(f"label must be a string not {type(label)}.")

    for var in [values, year_var]:
        if df[var].dtype not in [
            'int16',
            'int32',
            'int64',
            'float16',
            'float32',
            'float64',
        ]:
            raise ValueError(f"{var} must contain numeric values")

    if df[df[year_var] == year].shape[0] == 0:
        raise ValueError("404 year not found in dataframe")

    if len(df[color_var].unique()) > 25:
        warnings.warn(f"Having too many groups will result in repeated colors")

    dff = (
        df[df[year_var] == year]
        .sort_values(by=values, ascending=True)
        .tail(10)
    )
    if ax is None:
        ax = plt.gca()
    ax.clear()
    ll = list(dict.fromkeys(df[color_var]))
    if len(ll) < 8:
        colors = dict(
            zip(ll, [cm.Set2(x) for x in linspace(0, 0.87, len(ll))])
        )
    else:
        colors = dict(
            zip(
                ll,
                [cm.Set2(x) for x in linspace(0, 0.87, 8)]
                + [cm.Set3(x) for x in linspace(0.09, 1, len(ll) - 8)],
            )
        )
    bars = ax.barh(
        dff[names_var],
        dff[values],
        color=[colors[x] for x in dff[color_var]],
        alpha=0.73,
        edgecolor='#998D8F',
        linewidth=1.5,
        **kwargs,
    )
    dx = dff[values].max() / 200
    for i, (value, name) in enumerate(zip(dff[values], dff[names_var])):
        if len(name) > 0.43 * value / dx:
            name = name[: int(0.43 * value / dx)] + '..'
        ax.text(value - dx, i, name, size=16, ha='right', va='center')
        ax.text(
            value + dx, i, f'{value:,.0f}', size=14, ha='left', va='center'
        )

        ax.text(
            0.97,
            0.4,
            year,
            transform=ax.transAxes,
            color='#FFECEF',
            size=46,
            ha='right',
            weight=800,
            path_effects=[
                path_effects.Stroke(linewidth=3, foreground='black'),
                path_effects.Normal(),
            ],
        )
    ax.text(0, 1.06, label, transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(
        0, 1.1, title, transform=ax.transAxes, size=22, weight=600, ha='left'
    )
    plt.box(False)
    color_var_uniq = list(dict.fromkeys(dff[color_var][::-1]))
    lgd = ax.legend(bars, color_var_uniq, loc=(0.82, 0.03))
    for i, j in enumerate(lgd.legendHandles):
        j.set_color([colors[x] for x in color_var_uniq][i])
