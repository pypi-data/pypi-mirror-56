"""
Plot Aggregated Map.
"""

import numpy as np
import pandas as pd
import folium
import json
import pkg_resources
import os
import warnings
import matplotlib.pyplot as plt
import re
from io import BytesIO
import base64

DATA_PATH = pkg_resources.resource_filename('templot', 'data')


def plot_aggregated_map(
    data, variables, group="Regions", aggregation_method="average", height=300
):

    """
    Plots a map that shows the evolution of an aggregated value of variables per group (regions, departments or communes)
    For example, this function can be used to show the evolution of the average of each of two variables (each representing a year) by region.

    :param data: Pandas DataFrame containing (at least) two columns; one of the group and another(/others) of the variable(s) of interest.
    :param variables: a list of column names containing values each year
    :param group: group variable name. Possible values are "Regions", "Departements", "Communes". Defaults to "Regions".
    :param aggregation_method: aggregation method. Possible values are "average", "median", "min", "max" and "count". Defaults to "average".
    :param height: tooltip height in pixels. Defaults to 300.
    :return: Folium map

    One example of this map:

    .. raw:: html

        <iframe src="example_agrmap.html" height="600px" width="100%"></iframe>

    """

    if not isinstance(data, pd.core.frame.DataFrame):
        raise TypeError(f"data must be a DataFrame not {type(data)}.")

    if len(data.shape) != 2:
        raise ValueError(f"data must be a matrix but shape is {data.shape}")

    if data.shape[1] < 2:
        raise ValueError(
            f"data must be a matrix with at least two columns but shape is {data.shape}"
        )

    if not variables:
        raise ValueError(f"variables must be supplied.")

    if not isinstance(variables, list):
        raise TypeError(f"variables must be a list, not {type(variables)}")

    for var in variables:
        if var not in data.columns:
            raise ValueError(f"{var} is not a valid column name.")

        if data[var].dtype not in [
            'int16',
            'int32',
            'int64',
            'float16',
            'float32',
            'float64',
        ]:
            raise ValueError(f"{var} must contain numeric values.")

    if group not in data.columns:
        raise ValueError(f"{group} is not a valid column name.")

    if group not in ["Regions", "Departements", "Communes"]:
        raise ValueError(
            f"{group} is not a valid name. Possible values are: Regions, Departements or Communes"
        )

    if not isinstance(height, int):
        raise TypeError(f"Height must be an int, not {type(height)}")

    if height <= 0:
        raise ValueError("Tooltip height must be positive")

    if len(data[group].unique()) > 90:
        warnings.warn(
            f"Having too many groups may result in reduced performance."
        )

    aggregates = {
        "average": data.groupby(group).mean(),
        "median": data.groupby(group).agg(lambda x: x[x > 0].median()),
        "max": data.groupby(group).max(),
        "min": data.groupby(group).agg(lambda x: x[x > 0].min()),
        "count": data.groupby(group).agg(lambda x: x[x > 0].count()),
    }

    if aggregation_method not in aggregates:
        raise ValueError(
            f"{aggregation_method} is not a valid aggregation method. Possible values are: {', '.join([k for k in aggregates])}"
        )

    map_data = aggregates[aggregation_method][variables]

    if group == "Regions":
        with open(
            os.path.join(DATA_PATH, 'regions.geojson'), encoding="utf8"
        ) as f:
            geojson = json.loads(f.read())

    if group == "Departements":
        with open(
            os.path.join(DATA_PATH, 'departements.geojson'), encoding="utf8"
        ) as f:
            geojson = json.loads(f.read())

    if group == "Communes":
        with open(
            os.path.join(DATA_PATH, 'communes.geojson'), encoding="utf8"
        ) as f:
            geojson = json.loads(f.read())

    for feat in geojson["features"]:
        if feat["properties"]["nom"] in map_data.index:
            row = map_data[map_data.index == feat["properties"]["nom"]]
            heights = (row[variables]).values.flatten().tolist()
            y_pos = np.arange(len(variables))
            plt.bar(y_pos, heights)
            labels = [
                re.search(r"\d{4}", s).group() if re.search(r"\d{4}", s) else s
                for s in variables
            ]
            plt.xticks(y_pos, labels)
            plt.xticks(rotation=45, size=9)
            plt.title(
                f'Evolution of the {aggregation_method} in {feat["properties"]["nom"]}'
            )
            img2bytes = BytesIO()
            plt.savefig(img2bytes, format='png')
            plt.close()
            img2bytes.seek(0)
            bytesto64 = base64.b64encode(img2bytes.read())
            feat["properties"][
                "image"
            ] = f'<img height="{height}" src="data:image/png;base64,{bytesto64.decode("utf-8")}"/>'

        else:
            feat["properties"]["image"] = ""

    m = folium.Map(tiles="CartoDB positron", zoom_start=2)
    choropleth = folium.Choropleth(
        geo_data=geojson,
        data=map_data.mean(axis=1),
        fill_color="BuPu",
        key_on="feature.properties.nom",
        highlight=True,
        bins=9,
    ).add_to(m)

    choropleth.color_scale.caption = (
        f'Mean {aggregation_method} over the {len(variables)} years'
    )
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(fields=["image"], labels=False)
    )

    m.fit_bounds(m.get_bounds())
    return m
