import time

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from functools import wraps

def log_time(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        f = open("log_dev.txt",'a',encoding="utf8")
        time_res = end - start
        f.write("\n"+func.__name__+ " time = " + str(time_res))
        return result

    return wrapper

def finished_log():
    f = open("log.txt", 'a', encoding="utf8")
    f.write("\n\n")
    for i in range(150):
        f.write("-")
    f.write("\n\n")

st.title("this is the dashboard of the project")

if st.sidebar.button("2020 mutations"):
    st.subheader("2020 mutations")

    file_path = "part2020_sample.csv"

    @log_time
    def read_file(file_path):
        return pd.read_csv(file_path, delimiter=',', low_memory=False)

    df = read_file(file_path)

    st.write(df.astype(str).head(5))
#######

    st.subheader("Data transformation")


    @log_time
    @st.cache(suppress_st_warning=True, allow_output_mutation=True)
    def prepare_sample(dataframe):
        first_sample = dataframe.sample(n=100000)
        #st.write(first_sample.head(5))
        first_sample.drop(['nature_culture_speciale', 'code_nature_culture_speciale', "code_nature_culture", "code_type_local", "nombre_lots", "lot5_surface_carrez", "lot5_numero", "lot4_surface_carrez", "lot4_numero", "lot3_surface_carrez", "lot3_numero", "lot2_surface_carrez", "lot2_numero", "lot1_surface_carrez", "lot1_numero", "numero_volume", "ancien_id_parcelle", "id_parcelle", "ancien_nom_commune", "ancien_code_commune"], axis=1, inplace=True)
        return first_sample

    df = prepare_sample(df)
    st.expander("dropping unused columns") .write(df.head(5))


    @log_time
    @st.cache(suppress_st_warning=True, allow_output_mutation=True)
    def map_to_datetime(dataframe):
        dataframe["date_mutation"] = dataframe["date_mutation"].map(pd.to_datetime)
        return dataframe

    df = map_to_datetime(df)
    st.expander("Dataframe after the to_datetime mapping").write(df.head(5))


    def get_month(dt):
        return dt.month

    @log_time
    @st.cache(suppress_st_warning=True, allow_output_mutation=True)
    def add_column_month(dataframe):
        dataframe["month_mutation"] = dataframe["date_mutation"].map(get_month)
        return dataframe

    df = add_column_month(df)
    st.expander("dataframe after adding month column").write(df.head(5))



    def count_rows(rows):
        return len(rows)


    @log_time
    @st.cache(suppress_st_warning=True, allow_output_mutation=True)
    def group_by_nom_commune(dataframe):
        dataframe.groupby("nom_commune").apply(count_rows)
        return dataframe

    df_gb_nom_commune = group_by_nom_commune(df)
    st.expander("data grouped by 'nom commune'").write(df_gb_nom_commune.head(5))


######
    st.subheader("Visual representation")


    # On observe le nombre de mutation par type de local

    @log_time
    def plot_frequency_by_local_type(dataframe):
        figure = plt.figure()
        x = ["Appartement","Dépendance", "Local industriel.\ncommercial\nassimilé", "Maison"]
        y = dataframe.groupby("type_local").apply(count_rows)
        plt.pie(y, labels=x)
        return figure

    figure = plot_frequency_by_local_type(df)
    st.expander("Frequency by type local").write(figure)




    #on voit quel mois on a le plus de vente
    #def bar_group_by_month(dataframe):
    @log_time
    def plot_bar_month_mutation(dataframe):
        figure = plt.figure()
        y = dataframe.groupby("month_mutation").apply(count_rows)
        plt.bar(range(1,13),y)
        return figure

    figure = plot_bar_month_mutation(df)
    st.expander("number of mutation by month").write(figure)




    # On observe la fréquence de transactions en fonction du nombre de pièce
    @log_time
    def hist_mutation_nb_piede(dataframe):
        figure, ax = plt.subplots()
        ax.hist(dataframe['nombre_pieces_principales'], bins=10, range=(0,10))
        plt.xlabel("nb pièce")
        plt.ylabel("Frequency")
        return figure

    figure = hist_mutation_nb_piede(df)
    st.expander("number of mutation for each number of room").write(figure)





    # On observe la valeur foncière minimale par nombre de piece principales
    @log_time
    def value_nb_room(dataframe):
        data_gb_nbpiece = dataframe.groupby("nombre_pieces_principales").agg({"valeur_fonciere":"min"})
        return  data_gb_nbpiece

    data = value_nb_room(df)
    st.expander("data grouped by nb room").write(data.head(55))

    @log_time
    def plot_nbroom_value(data):
        figure = plt.figure()
        plt.plot(data)
        return figure

    figure = plot_nbroom_value(data)
    st.expander("plot nb room - value").write(figure)



