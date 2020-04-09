# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 22:00:56 2020

@author: Giovanni
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import pandas as pd  # used to read csv files
import matplotlib.pyplot as plt


def show_dati_province(root_folder: str):
    # Load the data using pandas
    dati_province = pd.read_csv(root_folder +
                                "dati-province\\dpc-covid19-ita-province.csv ",
                                delimiter=',')
    dati_province.plot(kind="scatter",
                       x="long",
                       y="lat",
                       alpha=0.4,
                       label="contagi",
                       s=dati_province["totale_casi"],
                       c="totale_casi",
                       cmap=plt.get_cmap("jet"))
    plt.legend()
    plt.show()


def load_lista_regioni(root_folder: str):
    # Use pandas to read json file, creating a dataframe
    lista_regioni_json = pd.read_json(root_folder + "Italy\\regioni.json",
                                      "r",
                                      encoding="utf8",
                                      dtype={
                                          "id": str,
                                          "nome": str,
                                          "latitudine": float,
                                          "longitudine": float,
                                          "flag": str
                                      })
    print(lista_regioni_json)


def load_lista_comuni(root_folder: str):
    lista_comuni = pd.read_csv(root_folder + "Italy\\comuni.csv",
                               delimiter=';')

    print(lista_comuni)


def read_province(root_folder: str):
    with open(root_folder + "Italy\\province.txt", mode="r",
              encoding="utf-8") as f:
        lista_province = f.readlines()
        # remove the trailer '\n'
        lista_province = [provincia[:-1] for provincia in lista_province]
        return lista_province


def read_poplazione_province(root_folder: str):
    lista_provincie = pd.read_csv(root_folder +
                                  "Italy\\province_popolazione.csv")

    print(lista_provincie)


def load_dati_regioni(root_folder: str):
    # Load the data using pandas
    dati_regioni = pd.read_csv(root_folder +
                               "dati-regioni\\dpc-covid19-ita-regioni.csv",
                               delimiter=',')

    dati_regioni.plot(kind="scatter",
                      x="long",
                      y="lat",
                      alpha=0.4,
                      label="contagi",
                      s=dati_regioni["totale_casi"],
                      c="totale_casi",
                      cmap=plt.get_cmap("jet"))
    plt.legend()
    plt.show()


def filter_by_region(root_folder: str):
    dati_regioni = pd.read_csv(root_folder +
                               "dati-regioni\\dpc-covid19-ita-regioni.csv",
                               delimiter=',')
    dati_regioni = dati_regioni.copy()
    dati_regioni = dati_regioni.drop(columns=['note_it', 'note_en'])
    dati_regioni = dati_regioni[dati_regioni['denominazione_regione'] ==
                                'P.A. Trento']
    dati_regioni = dati_regioni['totale_casi']
    #array= dati_regioni.to_numpy()
    #array.savetxt(root_folder + "dati-regioni\\dpc-covid19-ita-regione.csv", a, delimiter=",")
    print(dati_regioni)


def load_dati_andamento_nazionale(root_folder: str):
    # Load the data using pandas
    andamento_nazionale = pd.read_csv(
        root_folder +
        "dati-andamento-nazionale\\dpc-covid19-ita-andamento-nazionale.csv",
        index_col=0,
        delimiter=',')
    andamento_nazionale = andamento_nazionale.copy()
    andamento_nazionale = andamento_nazionale.drop(columns=[
        'tamponi', 'nuovi_positivi', 'variazione_totale_positivi',
        'terapia_intensiva', 'totale_casi'
    ])
    andamento_nazionale.plot()
    plt.show()


def normalized_contagions_by_province(pc_folder: str, genocs_folder: str):

    # load data coming from protezione civile
    dati_covid_province = pd.read_csv(
        pc_folder + "dati-province\\dpc-covid19-ita-province.csv")

    # remove unused column
    dati_covid_province = dati_covid_province.drop(columns=[
        'stato', 'codice_regione', 'denominazione_regione', 'note_it',
        'note_en'
    ])

    # read dati provincie
    lista_provincie = pd.read_csv(genocs_folder +
                                  "Italy\\province_popolazione.csv")

    # merge dati protezione civile with dati popolazione
    merged = pd.merge(dati_covid_province,
                      lista_provincie,
                      on='denominazione_provincia')

    # calculate contagi normalized by population
    merged['contagi_percentuali'] = (merged['totale_casi'] *
                                     1000000) / (merged['popolazione'])

    # save data to csv
    merged.to_csv(genocs_folder + "Italy\\province_popolazione_merge.csv")

    lista_province = read_province(genocs_folder)

    for prov in lista_province:
        print(prov)
        provincia = merged.copy()
        provincia = provincia[provincia['denominazione_provincia'] == prov]
        dati_province = provincia['totale_casi']
        dati_provincegeo = provincia[['lat', 'long']]

        lat = 0.0
        lon = 0.0

        if (dati_provincegeo.shape[0] > 0):
            lat = dati_provincegeo.iloc[0][0]
            lon = dati_provincegeo.iloc[0][1]

            # Pandas dataframe to one line comma separated values
            vals = ['%s, ' % ele for ele in dati_province]
            s = ''.join(vals)
            # Now unpack the input list `vals` into the format string. Done!
            formatted = '%s,%s' % (prov, s.format(*vals))
            formatted = formatted[:-2]  # remove the trailer

            # append on file
            file_name = ".\\build\\provice.csv"
            opened_file = open(file_name, 'a')
            opened_file.write("%s\n" % formatted)
            opened_file.close()


def main(args=""):

    pc_repo: str = 'C:\\dev\\COVID-19\\'
    genocs_geo_repo: str = 'C:\\dev\\genocs\\geo\\'

    #show_dati_province(pc_repo)
    #load_dati_regioni(pc_repo)
    #filter_by_region(pc_repo)
    #load_dati_andamento_nazionale(pc_repo)
    #filter_by_province(pc_repo)
    #read_province()

    #read_province2(genocs_geo_repo)
    normalized_contagions_by_province(pc_repo, genocs_geo_repo)


if __name__ == '__main__':
    main()
