"""
Plot polar bar.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import pandas as pd
import warnings


def plot_polar_bar_evolution(
    df,
    var,
    year,
    group="Regions",
    agr="average",
    y_grid=False,
    x_grid=False,
    y_ticks=False,
):

    """
    Plots an animated polar bar showing the evolution of a variable by group across year.

    :param df: DataFrame
    :param var: name of the column containing the values.
    :param year: name of the column containing the year of each observation.
    :param group: group variable column name. Possible values are "Regions", "Departements", "Communes". Defaults to "Regions".
    :param aggregation_method: aggregation method. Possible values are "average", "median", "min", "max" and "count". Defaults to "average".
    :param y_grid: boolean for showing the grid along the radial axis. Defaults to False.
    :param x_grid: boolean or showing an angular grid. Defaults to False.
    :param yticks: boolean for showing the radial ticks. Defaults to False.
    :return: MatplotLib animation

    One example of this plot:

    .. raw:: html

        <img src="example_polarbar_animation.gif" height="620px" width="100%">

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

    if not isinstance(x_grid, bool):
        raise TypeError(f"x_grid must be an int, not {type(x_grid)}")

    if not isinstance(y_grid, bool):
        raise TypeError(f"x_grid must be an int, not {type(x_grid)}")

    if not isinstance(y_ticks, bool):
        raise TypeError(f"x_grid must be an int, not {type(x_grid)}")

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

    N = len(df_agr[group].unique())

    theta = np.arange(0, 2 * np.pi, 2 * np.pi / N)
    data = df_agr[var]

    viridis = plt.cm.get_cmap('viridis')
    c = viridis(np.interp(data, (data.min(), data.max()), (0, +1)))

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, polar=True)
    ax.set_xticks(theta)
    ax.set_xticklabels(df_agr[group].unique())

    for th, label in zip(ax.get_xticks(), ax.get_xticklabels()):
        th = th * ax.get_theta_direction() + ax.get_theta_offset()
        th = np.pi / 2 - th
        y, x = np.cos(th), np.sin(th)
        if x >= 0.1:
            label.set_horizontalalignment('left')
        if x <= -0.1:
            label.set_horizontalalignment('right')
        if y >= 0.5:
            label.set_verticalalignment('bottom')
        if y <= -0.5:
            label.set_verticalalignment('top')

    ax.xaxis.grid(x_grid)
    ax.yaxis.grid(y_grid)
    plt.setp(ax.get_yticklabels(), visible=y_ticks)

    cNorm = mpl.colors.Normalize(vmin=data.min(), vmax=data.max())
    ax3 = fig.add_axes([0.9, 0.1, 0.03, 0.8])
    mpl.colorbar.ColorbarBase(ax3, norm=cNorm)
    plt.gcf().subplots_adjust(right=0.7)

    years = df_agr[year].unique()
    data = df_agr[df_agr[year] == years[0]][var]
    title = f"{agr} {var} in {years[0]}"
    ax.set_title(title, weight='bold', size='large', position=(0.5, 1.1))
    ax.bar(theta, data, width=0.4, color=c[df_agr[year] == years[0]])

    def update(i):
        data = df_agr[df_agr[year] == years[i]][var]
        for obj in ax.findobj(match=mpl.patches.Rectangle):
            obj.remove()
        title = f"{agr} {var} in {years[i]}"
        ax.set_title(title, weight='bold', size='large', position=(0.5, 1.1))
        bars = ax.bar(
            theta, data, width=0.4, color=c[df_agr[year] == years[i]]
        )
        return bars

    ani = animation.FuncAnimation(
        fig, update, frames=len(years), interval=1000, blit=False, repeat=False
    )
    plt.close()
    return ani
