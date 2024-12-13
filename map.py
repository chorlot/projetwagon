import streamlit as st
import pandas as pd
import folium
import geopandas as gpd
from folium.plugins import MarkerCluster
from branca.colormap import linear
from streamlit_folium import st_folium

# Fonction de chargement des données avec mise en cache
@st.cache_data
def load_data():
    df = pd.read_csv('score_com.csv')
    return df

# Charger les données
df = load_data()

# Optimisation des types de données
df['score_de_ville'] = df['score_de_ville'].fillna(0)
df['reg_nom'] = df['reg_nom'].astype('category')
df['dep_nom'] = df['dep_nom'].astype('category')

# Fonction pour créer la carte avec folium
def create_map(df):
    # Créer une carte
    map_center = [df['latitude_mairie'].mean(), df['longitude_mairie'].mean()]
    my_map = folium.Map(location=map_center, zoom_start=6, tiles='CartoDB Dark_Matter')

    # Ajouter les villes à la carte
    city_cluster = MarkerCluster(name="Villes")
    for index, row in df.iterrows():
        folium.CircleMarker(
            location=[row['latitude_mairie'], row['longitude_mairie']],
            radius=4,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.6,
            popup=f"<b>Ville :</b> {row['com_nom']}<br><b>Score :</b> {row['score_de_ville']:.2f}"
        ).add_to(city_cluster)

    city_cluster.add_to(my_map)
    return my_map

# Afficher la carte quand l'utilisateur appuie sur un bouton
if st.button("Afficher la carte"):
    my_map = create_map(df)
    st_folium(my_map, width=700, height=500)
