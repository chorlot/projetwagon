import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
from folium.plugins import MarkerCluster
from branca.colormap import linear
from streamlit_folium import st_folium

# Charger les fichiers GeoJSON pour les régions et départements
regions_geojson = 'reg.json'
departments_geojson = 'dep.json'

# Charger les données de villes
df = pd.read_csv('score_com_final.csv')
df['score_de_ville'] = df['score_de_ville'].fillna(0)

# Calculer les scores moyens par région et département
region_scores = df.groupby('reg_nom')['score_de_ville'].mean().reset_index()
department_scores = df.groupby('dep_nom')['score_de_ville'].mean().reset_index()

# Charger les géométries
regions_gdf = gpd.read_file(regions_geojson)
departments_gdf = gpd.read_file(departments_geojson)

# Joindre les scores aux géométries
regions_gdf = regions_gdf.merge(region_scores, left_on='libgeo', right_on='reg_nom')
departments_gdf = departments_gdf.merge(department_scores, left_on='libgeo', right_on='dep_nom')

# Créer une échelle de couleurs inversée (bas score = rouge, haut score = vert)
colormap = linear.RdYlGn_09.scale(df['score_de_ville'].min(), df['score_de_ville'].max())
colormap2 = linear.Blues_09.scale(df['score_de_ville'].min(), df['score_de_ville'].max())

# Créer la carte
map_center = [df['latitude_mairie'].mean(), df['longitude_mairie'].mean()]
my_map = folium.Map(location=map_center, zoom_start=6, tiles='CartoDB Dark_Matter')

# 1. Ajouter les régions (vue globale)
folium.GeoJson(
    regions_gdf,
    style_function=lambda x: {
        'fillColor': colormap2(x['properties']['score_de_ville']),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=['reg_nom', 'score_de_ville'],
                                  aliases=['Région', 'Score moyen']),
    name='Régions'
).add_to(my_map)

# 2. Ajouter les départements (zoom intermédiaire)
folium.GeoJson(
    departments_gdf,
    style_function=lambda x: {
        'fillColor': colormap2(x['properties']['score_de_ville']),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=['dep_nom', 'score_de_ville'],
                                  aliases=['Département', 'Score moyen']),
    name='Départements',
    show=False  # Masquer par défaut
).add_to(my_map)

# 3. Ajouter des clusters par ville (zoom maximal)
city_cluster = MarkerCluster(name="Villes")
for index, row in df.iterrows():
    # Normaliser le score pour colormap
    score_norm = (row['score_de_ville'] - df['score_de_ville'].min()) / (df['score_de_ville'].max() - df['score_de_ville'].min())
    color = colormap(score_norm)
    
    folium.CircleMarker(
        location=[row['latitude_mairie'], row['longitude_mairie']],
        radius=4,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        popup=f"<b>Ville :</b> {row['com_nom']}<br><b>Score :</b> {row['score_de_ville']:.2f}"
    ).add_to(city_cluster)

city_cluster.add_to(my_map)

# Ajouter les légendes
colormap.add_to(my_map)
colormap2.add_to(my_map)

# Streamlit Layout
st.title("Carte Interactive avec Streamlit et Folium")
st.write("Cette carte montre les régions, départements et clusters des villes en fonction de leur score.")

# Afficher la carte dans Streamlit
st_data = st_folium(my_map, width=700, height=500)
