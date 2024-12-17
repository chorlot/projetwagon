import streamlit as st
import pandas as pd
from keplergl import KeplerGl
import geopandas as gpd
# Charger les fichiers GeoJSON pour les régions et départements
regions_geojson = 'reg.json'
departments_geojson = 'dep.json'
# Charger les données de villes
df = pd.read_csv('indices_simples_ok.csv')
df2 = pd.read_csv('indices_complets_ok.csv')
# Light/Dark Mode Selection
st.sidebar.header("Options d'affichage")
dark_mode = st.sidebar.checkbox("Activer le Dark Mode")

# CSS pour Dark Mode complet (Sidebar, Header, Textes, Boutons)
dark_mode_css = """
    <style>
        /* Fond global et conteneur principal */
        body, .stApp, .block-container {
            background-color: #1e1e1e !important;
            color: #ffffff !important;
        }

        /* Header (bandeau supérieur de Streamlit) */
        header, .st-emotion-cache-18e3th9, .st-emotion-cache-16txtl3 {
            background-color: #242424 !important;
            color: #ffffff !important;
        }

        /* Sidebar (fond et contenu) */
        section[data-testid="stSidebar"] {
            background-color: #242424 !important;
        }

        /* Appliquer la couleur blanche à tous les textes descendants de la sidebar */
        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        /* Texte de la sidebar (labels et sliders) */
        .stSlider label, .stTextInput label, .stSelectbox label {
            color: #ffffff !important;
        }

        /* Titres de la sidebar */
        .stSidebar .st-emotion-cache-1qj3r6n, .st-emotion-cache-1xarl3l {
            color: #ffffff !important;
        }

        /* Boutons */
        .stButton>button {
            background-color: #444444 !important;
            color: #ffffff !important;
            border: 1px solid #ffffff !important;
        }

        /* Champs de saisie */
        .stTextInput>div>div>input, .stSelectbox>div>div>input {
            background-color: #333333 !important;
            color: #ffffff !important;
            border: 1px solid #ffffff !important;
        }

        /* Messages d'alerte, sliders et autres textes */
        .st-at, .st-bb, .st-cf, .st-ai, .st-ab {
            color: #ffffff !important;
        }

        /* Scrollbar en dark mode */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-thumb {
            background-color: #444444 !important;
            border-radius: 10px;
        }
        /* Style pour les tableaux st.table en Dark Mode */
table {
    background-color: #333333 !important;
    color: #ffffff !important;
    border: 1px solid #444444 !important;
}

thead th {
    background-color: #444444 !important;
    color: #ffffff !important;
}

tbody tr td {
    background-color: #333333 !important;
    color: #ffffff !important;
    border: 1px solid #444444 !important;
}

tbody tr:hover {
    background-color: #555555 !important;
}

    </style>
"""

light_mode_css = """
    <style>
        body, .stApp, .block-container {
            background-color: #f0f2f6;
            color: #000000;
        }
        .sidebar .sidebar-content, .stSidebar {
            background-color: #ffffff;
            color: #000000;
        }
        header, .st-emotion-cache-1gulkj5 {
            background-color: #ffffff;
            color: #000000;
        }
        .st-bb, .st-at, .st-cf, .st-ai, .st-ab {
            color: #000000;
        }
        .stButton>button, .stTextInput>div>div>input {
            background-color: #008CBA;
            color: #ffffff;
        }
    </style>
"""

# Appliquer le thème global en fonction du choix de l'utilisateur
if dark_mode:
    st.markdown(dark_mode_css, unsafe_allow_html=True)
    # Injection de CSS supplémentaire pour forcer le style des tables
    st.markdown("""
        <style>
        table {
            background-color: #333333 !important;
            color: #ffffff !important;
            border: 1px solid #444444 !important;
        }
        thead th {
            background-color: #444444 !important;
            color: #ffffff !important;
        }
        tbody tr td {
            background-color: #333333 !important;
            color: #ffffff !important;
            border: 1px solid #444444 !important;
        }
        tbody tr:hover {
            background-color: #555555 !important;
        }
        </style>
    """, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["CARTE", "TABLEAU"])

with tab1:

    # Initialize session state for reset
    if "selected_regions" not in st.session_state:
        st.session_state.selected_regions = ["All"]
    if "selected_departments" not in st.session_state:
        st.session_state.selected_departments = ["All"]
    if "selected_density" not in st.session_state:
        st.session_state.selected_density = ["All"]

    def reset():
        st.session_state.selected_regions = ["All"]
        st.session_state.selected_departments = ["All"]
        st.session_state.selected_density = ["All"]

    #add filter departement and region(sort by A-Z)
    #creat a list of resgions and a list of deparments from dataframe
    regions = ["All"] + df["reg_nom"].unique().tolist()
    departments = ["All"] + sorted(df["dep_nom"].unique().tolist())
    densities = ["All"] + sorted(df["grille_densite"].unique().tolist())

    #affichage des sidebar pour région et département
    selected_regions = st.sidebar.multiselect("Sélectionnez Région:", options=regions, default=st.session_state.selected_regions)
    selected_departments = st.sidebar.multiselect("Sélectionnez Département:", options=departments, default=st.session_state.selected_departments)
    # Reset button
    st.sidebar.button("Reset Région/Département", on_click=reset)
    #ajouter une option pour filtrer sur le top 50 des communes
    top50 = st.sidebar.checkbox('Filtrer les communes (Top 50)')
    #ajouter une option pour filtrer sur les communes du littoral
    littoral = st.sidebar.checkbox('Afficher seulement les communes littorales')
    #affichage des sidebar pour la taille d'urbanisation
    selected_density = st.sidebar.selectbox("Sélectionnez la taille d'urbanisation:", options=densities, index=0)

    # Update session state with current selections
    st.session_state.selected_regions = selected_regions
    st.session_state.selected_departments = selected_departments
    st.session_state.selected_density = selected_density

    # Filter function
    def filter_data(data, selected_regions, selected_departments, selected_density):
        filtered_data = data.copy()
        if "All" not in selected_regions:
            filtered_data = filtered_data[filtered_data["reg_nom"].isin(selected_regions)]
        if "All" not in selected_departments:
            filtered_data = filtered_data[filtered_data["dep_nom"].isin(selected_departments)]
        if "All" != selected_density:
            filtered_data = filtered_data[filtered_data["grille_densite"] == selected_density]
        return filtered_data

    # Filter data based on selected filters
    filtered_data = filter_data(df, selected_regions, selected_departments,selected_density)

    #add research bar
    search_commune = st.sidebar.text_input("Cherchez une commune:", "")
    if search_commune:
        filtered_data = filtered_data[filtered_data["com_nom"].str.contains(search_commune, case=False, na=False)]
    #decide the dynamique geo center 
    if filtered_data.empty:
        st.warning("No data found for the selected filters.")
        # Default center (France)
        center_lat = 46.603354
        center_lon = 1.888334
        zoom_level = 5  # Default zoom level
    else:
        #calculate geo center
        center_lat = filtered_data["latitude_mairie"].mean()
        center_lon = filtered_data["longitude_mairie"].mean()

    #calculate zoom level
    lat_range = filtered_data["latitude_mairie"].max() - filtered_data["latitude_mairie"].min()
    lon_range = filtered_data["longitude_mairie"].max() - filtered_data["longitude_mairie"].min()
    zoom_level = max(5, min(12, 10 - max(lat_range, lon_range)))  
    # Sliders for weights
    st.sidebar.header("Ajustez vos préférences:")
    st.sidebar.write("0 = Ne pas en tenir compte")
    st.sidebar.write("9 = Très important à mes yeux")
    weights = {}
    questions = {
        "indice_education_norm": "Accès à une offre éducative complète",
        "indice_sante": "Accès aux soins",
        "indice_loisirsculture": "Accès aux loisirs et à la culture",
        "indice_alimentationservices": "Accès à l'alimentation et aux services",
        "indice_loyer_norm": "Loyers abordables",
        "indice_gare": "Présence d'une gare ferroviaire",
        "score_ensoleillement": "Nombre de jours ensoleillés par an",
        "indice_chomage_norm": "Taux de chômage",
        "indice_crime": "Sentiment de sécurité",
        "indice_risques_norm": "Éviter les zones à risques naturels",
        "indice_charge_VE": "Proximité avec une borne de rechargement VE",
        "indice_salaire_prive": "Salaires du secteur privé",
        #"indice_salaire_publique": "Salaires du secteur public",
    }
    # Create a slider for each weight
    for key, label in questions.items():
        weights[key] = st.sidebar.slider(f"{label} (0-9)", 0, 9, 5)  # Default value = 5
    # Display selected weights
    #st.sidebar.write("Selected Preferences:")
    #st.sidebar.write(weights)
    # Normalize the weights so they sum to 1
    total_weight = sum(weights.values())
    weights = {key: value / total_weight for key, value in weights.items()}
    # Create a copy of the original DataFrame so it won't be overwritten by user before
    df_copy = df.copy()
    # Apply transformations to the copy
    df_copy = df_copy.set_index(['dep_code', 'dep_nom', 'latitude_mairie', 'com_insee', 'coordonnees', 'population',
                                'longitude_mairie', 'reg_nom', 'densite', 'com_nom', 'grille_densite'])  # Set index before mapping
    df_copy = df_copy.mul(pd.Series(weights), axis=1)  # Apply weights
    df_copy["score_de_ville"] = round(df_copy.sum(axis=1) * 100, 1)  # Calculate final score
    df_copy = df_copy.reset_index()  # Reset index for display

    # Appliquer les filtres principaux sur filtered_data
    if littoral:
        st.write("Vous affichez seulement les communes littorales de France métropolitaine.")
        filtered_data = filtered_data[filtered_data["indice_littoral"] == 1]
        
    if top50:
        st.write("Vous affichez le TOP 50 des communes de France métropolitaine correspondant à vos critères.")
        # Trier et sélectionner le top 50
        filtered_data = filtered_data.copy()
        filtered_data = filtered_data.set_index(['dep_code', 'dep_nom', 'latitude_mairie', 'com_insee', 
                                                'coordonnees', 'population', 'longitude_mairie', 
                                                'reg_nom', 'densite', 'com_nom', 'grille_densite'])
        filtered_data = filtered_data.mul(pd.Series(weights), axis=1)
        filtered_data["score_de_ville"] = round(filtered_data.sum(axis=1) * 100, 2)
        filtered_data = filtered_data.reset_index().sort_values(by="score_de_ville", ascending=False).head(50)

    if "score_de_ville" not in filtered_data.columns:
        filtered_data = filtered_data.set_index(['dep_code', 'dep_nom', 'latitude_mairie', 'com_insee', 
                                                'coordonnees', 'population', 'longitude_mairie', 
                                                'reg_nom', 'densite', 'com_nom', 'grille_densite'])
        filtered_data = filtered_data.mul(pd.Series(weights), axis=1)
        filtered_data["score_de_ville"] = round(filtered_data.sum(axis=1) * 100, 2)
        filtered_data = filtered_data.reset_index()

    filtered_kepler_data = pd.DataFrame({
            "latitude": filtered_data["latitude_mairie"],
            "longitude": filtered_data["longitude_mairie"],
            "Region": filtered_data["reg_nom"],
            "Département": filtered_data["dep_nom"],
            "Commune": filtered_data["com_nom"],
            "Score de Ville": filtered_data["score_de_ville"]
        })

    # Calcul du Top 5 après application des filtres
    top_5_communes = filtered_data.sort_values(by="score_de_ville", ascending=False).head(5)

    # Mise en forme
    top_5_communes.rename(columns={
        "com_nom": "Commune",
        "population": "Population", 
        "score_de_ville": "Score de ville",
        "dep_nom": "Département", 
        "reg_nom": "Région"}, inplace=True)
    # Reset index for display
    top_5_communes = top_5_communes.reset_index(drop=True)
    top_5_communes.index += 1

    top_5_communes["Population"] = top_5_communes["Population"].astype(int)
    top_5_communes["Population"] = top_5_communes["Population"].apply(lambda x: f"{x:,}")
    top_5_communes["Score de ville"] = top_5_communes["Score de ville"].map("{:.2f}".format)



    # Affichage
    st.subheader("Top 5 communes par score de ville")
    st.table(top_5_communes[["Commune", "Score de ville", "Population", "Département", "Région"]])

    # Configurer kepler
    config = {
            "version": "v1",
            "config": {
                "mapState": {
                    "latitude": center_lat,  
                    "longitude": center_lon,  
                    "zoom": zoom_level,  
                    "pitch": 0,
                    "bearing": 0
                },
                "mapStyle": {
                    "styleType": "dark" if dark_mode else "light"
                }
            }
        }

    #initialize kepler
    map_ = KeplerGl(height=800, config=config)
    #add filtered data to kepler
    map_.add_data(data=filtered_kepler_data, name="Filtered Data")
    #save map to html and integrate to streamlit
    map_.save_to_html(file_name='kepler_map.html', read_only=True)
    st.components.v1.html(open('kepler_map.html', 'r').read(), height=800)

with tab2:
    # Appliquer les filtres de région et de département sur df2
    if "All" not in selected_regions:
        df2_filtered = df2[df2["reg_nom"].isin(selected_regions)]
    else:
        df2_filtered = df2.copy()  # Si aucune région spécifique n'est sélectionnée, ne pas filtrer par région

    if "All" not in selected_departments:
        df2_filtered = df2_filtered[df2_filtered["dep_nom"].isin(selected_departments)]

    # Vérification si df2_filtered est déjà défini, sinon initialiser
    if 'df2_filtered' not in locals():
        df2_filtered = df2  # Si df2_filtered n'est pas encore défini, utiliser df2 comme source de données initiale
    
    # Filtrer les données sur la commune si un texte est entré dans la searchbar
    if search_commune:
        df2_filtered = df2_filtered[df2_filtered["com_nom"].str.contains(search_commune, case=False, na=False)]

    # Remplacer les valeurs binaires par "Oui" et "Non"
    binary_columns = [
        'boulangerie_patisserie', 'banque', 'commerce_proximite', 'cinema', 'pharmacie', 
        'tabac', 'garagiste', 'restaurant', 'cafe_bar', 'boites_de_nuit', 'bureau_de_postes', 
        'bibliotheques', 'centre_commercial', 'ski', 'surf', 'location_de_bateau', 'supermarches', 
        'Ecole_maternelle', 'Ecole_elementaire', 'Lycee', 'College', 'Medico_social','indice_gare','indice_charge_VE', 'indice_littoral',
        'risque_catastrophe_naturelle','zones_inondables','risque_technologique','risque_minier'
    ]

    for column in binary_columns:
        df2_filtered[column] = df2_filtered[column].apply(lambda x: "Oui" if x > 0 else "Non")

    # Renommer les colonnes pour l'affichage
    df2_filtered = df2_filtered.rename(columns={
        'com_insee': 'Code_insee',
        'com_nom': 'Commune',
        'reg_nom': 'Région',
        'dep_nom': 'Département',
        'grille_densite': 'Urbanisation',
        'indice_gare': 'Gares',
        'indice_charge_VE': 'Stations de charges voitures electriques',
        'T2_2024': 'Taux de chômage',
        'indice_loyer_norm': 'Loyer Abordable',
        'prive': 'Salaire privé',
        'publique': 'Salaire publique',
        'apl_aux_meds_ge': 'Accès aux médecins généralistes',
        'apl_aux_sages_femmes': 'Accès aux sages-femmes',
        'apl_aux_kines': 'Accès aux kinésithérapeutes',
        'apl_aux_infirmieres': 'Accès aux infirmières',
        'apl_aux_dentistes': 'Accès aux dentistes',
        'temp_jours': 'Jours ensoleillés par an',
        'indice_littoral': 'En bord de mer',
        'population':'Population',
        'boulangerie_patisserie': 'Boulangerie / Pâtisserie',
        'banque': 'Banque',
        'commerce_proximite': 'Commerce de proximité',
        'cinema': 'Cinéma',
        'pharmacie':'Pharmacie',
        'tabac': 'Tabac',
        'garagiste': 'Garagiste',
        'restaurant': 'Restaurant',
        'cafe_bar' : 'Café / Bar',
        'boites_de_nuit': 'Boite de nuit',
        'bureau_de_postes': 'Bureau de poste',
        'bibliotheques': 'Bibliothèque',
        'centre_commercial': 'Centre commercial',
        'ski': 'Ski',
        'surf': 'Surf',
        'location_de_bateau': 'Location de bateau',
        'supermarches': 'Supermarché',
        'risque_catastrophe_naturelle': 'Catastrophe naturelle',
        'zones_inondables': 'Zone inondable',
        'risque_technologique': 'Risque technologique',
        'risque_minier': 'Risque minier'
    })

    # Tables à afficher avec les nouveaux noms de colonnes
    tables = {
        "Données Globales": df2_filtered[['Code_insee', 'Commune', 'Région', 'Département', 'Population', 'Urbanisation']],
        "Commerces": df2_filtered[['Commune', 'Boulangerie / Pâtisserie', 'Banque', 'Commerce de proximité', 'Cinéma', 'Pharmacie', 'Tabac', 'Garagiste', 'Restaurant', 'Café / Bar', 'Boite de nuit', 'Bureau de poste', 'Bibliothèque', 'Centre commercial', 'Ski', 'Surf', 'Location de bateau', 'Supermarché']],
        "Écoles": df2_filtered[['Commune','Ecole_maternelle','Ecole_elementaire', 'Lycee', 'College', 'Medico_social']],
        "Transport": df2_filtered[['Commune', 'Gares', 'Stations de charges voitures electriques']],
        "Pouvoir d'achat": df2_filtered[['Commune', 'Taux de chômage', 'Loyer Abordable', 'Salaire privé', 'Salaire publique']],
        "Santé": df2_filtered[['Commune', 'Accès aux médecins généralistes', 'Accès aux sages-femmes', 'Accès aux kinésithérapeutes', 'Accès aux infirmières', 'Accès aux dentistes']],
        "Environnement": df2_filtered[['Commune','Jours ensoleillés par an','En bord de mer']],
        "Risques": df2_filtered[['Catastrophe naturelle','Zone inondable','Risque technologique','Risque minier']]
    }

    # Affichage des tables dynamiquement en fonction de la commune
    for table_name, table_data in tables.items():
        st.subheader(table_name)
        table_data_no_index = table_data.reset_index(drop=True)  # Réinitialise l'index
        st.dataframe(table_data_no_index, hide_index=True)

        #good one to take
