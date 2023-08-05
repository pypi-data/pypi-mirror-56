import json
import requests
import geopip
import pandas as pd
import zipfile
import os
from pyproj import Proj, transform
import pkg_resources
import shutil

DATA_PATH = pkg_resources.resource_filename('templot', 'data')


def download_irep(filepath):

    """
    Downloads and parses the IREP dataset to a specified location.

    :param filepath: the path to where the CSV file of the dataset will be saved.

    Original Source: `Gabriel Romon <https://github.com/gabsens/Python-for-Data-Scientists-ENSAE/blob/master/Devoir/IREP%20et%20devoir.ipynb>`_
   """

    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': 'http://www.georisques.gouv.fr/dossiers/irep/telechargement',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,ru;q=0.6,de;q=0.5,pt;q=0.4',
    }

    url = 'http://www.georisques.gouv.fr/irep/data/'
    for i in range(2003, 2018):
        response = requests.get(url + str(i), headers=headers, verify=False)
        with open('./' + str(i) + '.zip', mode='wb') as localfile:
            localfile.write(response.content)

        with zipfile.ZipFile('./' + str(i) + '.zip', "r") as zip_ref:
            zip_ref.extractall("./data/" + str(i) + '/')

        os.remove('./' + str(i) + '.zip')

    p1 = Proj(init='epsg:4326')
    p2 = Proj(init='epsg:27572')

    df = pd.read_csv("./data/2003/Prod_dechets_dangereux.csv")
    df2 = pd.read_csv("./data/2003/etablissements.csv")
    long, lat = transform(
        p2, p1, df2.Coordonnees_X.values, df2.Coordonnees_Y.values
    )
    df2['LLX'] = long
    df2['LLY'] = lat
    df = df.merge(df2, on="Identifiant")
    df = (
        df.groupby(['Identifiant'])
        .agg(
            {
                'Quantite': 'sum',
                'Nom_Etablissement_x': 'first',
                'LLX': 'first',
                'LLY': 'first',
            }
        )
        .reset_index()
    )
    df = df.rename({'Quantite': 'Quantite2003'}, axis='columns')

    for i in range(2004, 2018):
        df_temp = pd.read_csv(
            "./data/" + str(i) + "/Prod_dechets_dangereux.csv"
        )
        df2_temp = pd.read_csv("./data/" + str(i) + "/etablissements.csv")
        long, lat = transform(
            p2,
            p1,
            df2_temp.Coordonnees_X.values,
            df2_temp.Coordonnees_Y.values,
        )
        df2_temp['LLX'] = long
        df2_temp['LLY'] = lat
        df_temp = df_temp.merge(df2_temp, on="Identifiant")
        df_temp = (
            df_temp.groupby(['Identifiant'])
            .agg(
                {
                    'Quantite': 'sum',
                    'Nom_Etablissement_x': 'first',
                    'LLX': 'first',
                    'LLY': 'first',
                }
            )
            .reset_index()
        )
        df_temp = df_temp.rename(
            {'Quantite': 'Quantite' + str(i)}, axis='columns'
        )
        df = df.merge(
            df_temp,
            on=["Identifiant", "Nom_Etablissement_x", "LLX", "LLY"],
            how="outer",
        )

    df = df.fillna('0')

    lim_metropole = [-5, 10, 41, 52]

    df_metro = df[
        (
            (df.LLX >= lim_metropole[0])
            & (df.LLX <= lim_metropole[1])
            & (df.LLY >= lim_metropole[2])
            & (df.LLY <= lim_metropole[3])
        )
    ]
    df_metro.to_csv(filepath, index=False)
    shutil.rmtree('./data', ignore_errors=True)


def add_regions(df, x, y, add=["regions"]):

    """
    Adds regions, departments and/or communes to a DataFrame.

    :param df: a DataFrame containing at least two coordinate columns; longitude and lattidude.
    :param x: name of the column containing longitudes.
    :param y: name of the columns containing lattidudes.
    :param add: list of the columns to add. Possible values are "regions", "deparements" and "communes". Defaults to ["regions"].
    :return: the original DataFrame with the added columns.
   """

    add_reg = "regions" in add
    add_dep = "departements" in add
    add_comm = "communes" in add

    if add_reg:
        region_geo_json = json.loads(
            open(
                os.path.join(DATA_PATH, 'regions.geojson'), encoding="utf8"
            ).read()
        )
        reg = geopip.GeoPIP(geojson_dict=region_geo_json)

    if add_dep:
        dep_geo_json = json.loads(
            open(
                os.path.join(DATA_PATH, 'departements.geojson'),
                encoding="utf8",
            ).read()
        )
        dep = geopip.GeoPIP(geojson_dict=dep_geo_json)

    if add_comm:
        com_geo_json = json.loads(
            open(
                os.path.join(DATA_PATH, 'communes.geojson'), encoding="utf8"
            ).read()
        )
        com = geopip.GeoPIP(geojson_dict=com_geo_json)

    regions = []
    departements = []
    communes = []

    if add_reg:
        i = 0
        while i < len(df.index):
            region = reg.search(df[x].iloc[i], df[y].iloc[i])
            if region:
                regions.append(region["nom"])
                i += 1
            else:
                df = df.drop(i)
        df["Regions"] = regions

    if add_dep:
        i = 0
        while i < len(df.index):
            departement = dep.search(df[x].iloc[i], df[y].iloc[i])
            if departement:
                departements.append(departement["nom"])
                i += 1
            else:
                df = df.drop(i)
        df["Departements"] = departements

    if add_comm:
        i = 0
        while i < len(df.index):
            commune = com.search(df[x].iloc[i], df[y].iloc[i])
            if commune:
                communes.append(commune["nom"])
                i += 1
            else:
                df = df.drop(i)
        df['Communes'] = communes

    return df
