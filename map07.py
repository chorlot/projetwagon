import streamlit as st
import pandas as pd
from keplergl import KeplerGl
import geopandas as gpd

#page config (icone, titre d'onglet, layout)
st.set_page_config(
    page_title="Projet QV",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
    )
#st.cache_data
@st.cache_data(ttl=3600)
def load_data_simple():
    """Charge les données depuis un fichier CSV."""
    return pd.read_csv('indices_simples_ok.csv')

@st.cache_data(ttl=3600)
def load_data_complet():
    """Charge les données depuis un fichier CSV."""
    return pd.read_csv('indices_complets_ok.csv')
# Charger les données de villes
df = load_data_simple()
df2 = load_data_complet()
df = df[~df['com_nom'].str.contains("Arrondissement", case=False, na=False)]
df2 = df2[~df2['com_nom'].str.contains("Arrondissement", case=False, na=False)]

st.sidebar.image('PROJET QV.png')
#TITRE
st.title('Projet QV')
st.header('Qualité de Vie en France Métropolitaine', divider="grey")


# Light/Dark Mode Selection
dark_mode = st.sidebar.toggle("Activer le Dark Mode")
st.sidebar.divider()

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

        /* Correction pour les petits labels au-dessus des selectbox */
        label {
            color: #ffffff !important; /* Texte blanc pour tous les labels */
        }

        /* Style des cases Selectbox */
        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        div[data-baseweb="select"] span {
            color: #000000 !important;
        }

        /* Correction pour le bouton Reset */
        .stButton>button {
            background-color: #ffffff !important; /* Fond blanc */
            color: #000000 !important; /* Texte noir toujours visible */
            border: 1px solid #ffffff !important; /* Bordure blanche */
        }

        .stButton>button:hover {
            background-color: #e0e0e0 !important; /* Légère variation au survol */
        }

        /* Correction pour la case de recherche de commune */
        .stTextInput input {
            background-color: #ffffff !important; /* Fond blanc */
            color: #000000 !important; /* Texte noir */
            border: 1px solid #dddddd !important; /* Bordure grise */
        }

        /* Onglets (Mode d'emploi, Carte, etc.) */
        .stTabs [data-testid="stTab"] button {
            color: #ffffff !important; /* Texte blanc */
            background-color: #1e1e1e !important; /* Fond pour l'onglet inactif */
        }

        .stTabs [data-testid="stTab"].st-emotion-cache-1j5e2sq button {
            color: #ffffff !important; /* Onglet actif en blanc */
            border-bottom: 2px solid #ff4b4b !important; /* Soulignement onglet actif */
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
        /* Style des onglets (Dark Mode) */
        .stTabs [data-baseweb="tab"] {
            color: #ffffff !important; /* Couleur du texte pour les onglets inactifs */
        }

        /* Style pour l'onglet actif */
        .stTabs [aria-selected="true"] {
            color: #ff4b4b !important; /* Rouge pour l'onglet actif */
            border-bottom: 2px solid #ff4b4b !important; /* Soulignement rouge */
        }

        /* Soulignement de l'onglet actif pour plus de visibilité */
        .stTabs [aria-selected="true"] button {
            font-weight: bold !important; /* Texte en gras pour l'onglet actif */
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


#création des onglets
tab1, tab2, tab3, tab4, tab5 = st.tabs(["CARTE", "TABLEAUX", "MODE D'EMPLOI", "DOCUMENTATION", "ABOUT"])

# Ajout d'un cache pour chaque onglet
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "CARTE"

#onglet carte
with tab1:
    if st.session_state.active_tab == "CARTE":
        st.session_state.active_tab = "CARTE"
        st.header("Carte Interactive")

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
    left, middle, middle2, right = st.columns(4, vertical_alignment="bottom")
    selected_regions = left.multiselect("Sélectionnez Région:", options=regions, default=st.session_state.selected_regions)
    # Filtrer les départements selon les régions sélectionnées
    if "All" in selected_regions or not selected_regions:
        filtered_departments = ["All"] + sorted(df["dep_nom"].unique().tolist())
    else:
        filtered_departments = ["All"] + sorted(df[df["reg_nom"].isin(selected_regions)]["dep_nom"].unique().tolist())


    selected_departments = middle.multiselect("Sélectionnez Département :", options=filtered_departments, default=st.session_state.selected_departments
)
    # Reset button
    middle2.button("Reset Région/Département", on_click=reset)

    st.sidebar.header("Options d'affichage")
    #ajouter une option pour filtrer sur les gare
    gare= st.sidebar.checkbox('Afficher les communes avec une gare ferroviaire')
    #ajouter une option pour filtrer sur le top 50 des communes
    top50 = st.sidebar.checkbox('Filtrer les communes (Top 50)')
    #ajouter une option pour filtrer sur les communes du littoral
    littoral = st.sidebar.checkbox('Afficher les communes littorales')
    #ajouter une option pour filtrer sur les charge_VE
    charge_VE= st.sidebar.checkbox('Afficher les communes avec une borne de recharge VE')
    #affichage des sidebar pour la taille d'urbanisation
    selected_density = right.selectbox("Sélectionnez la taille d'urbanisation:", options=densities, index=0)

    # Update session state with current selections
    st.session_state.selected_regions = selected_regions
    st.session_state.selected_departments = selected_departments
    st.session_state.selected_density = selected_density

    # Filter function
    @st.cache_data(show_spinner=False)
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

    questions = {
        "indice_education_norm": "Accès à une offre éducative complète",
        "indice_sante": "Accès aux soins",
        "indice_loisirsculture": "Accès aux loisirs et à la culture",
        "indice_alimentationservices": "Accès à l'alimentation et aux services",
        "indice_loyer_norm": "Loyers abordables",
        #"indice_gare": "Présence d'une gare ferroviaire",
        "score_ensoleillement": "Nombre de jours ensoleillés par an",
        "indice_chomage_norm": "Taux de chômage",
        "indice_crime": "Sentiment de sécurité",
        "indice_risques_norm": "Éviter les zones à risques naturels",
        #"indice_charge_VE": "Proximité avec une borne de rechargement VE",
        "indice_salaire_prive": "Salaires du secteur privé",
        #"indice_salaire_publique": "Salaires du secteur public",
    }
    # Initialize session state for slider values if not already initialized
    if "slider_values" not in st.session_state:
        st.session_state.slider_values = {key: 5 for key in questions}  # Default values
        # Initialize each keys for each slider in session state
        for key in questions:
            st.session_state[key] = 5
    # si on clique sur Réinitialiser
    if st.sidebar.button("Réinitialiser"):
        # Reset slider values to default value
        st.session_state.slider_values = {key: 5 for key in questions}
        for key in questions:
            st.session_state[key] = 5  # Also reset slider keys
    # Create sliders for weighting criteria
    st.sidebar.write("**Pondérez les critères :**")
    for key, label in questions.items():
        # Create sliders using the stored session state values
        st.session_state.slider_values[key] = st.sidebar.slider(
            label, 0, 9, st.session_state.slider_values[key], key=key
        )

# Normalisation des pondérations
    total_weight = sum(st.session_state.slider_values.values())
    normalized_weights = {key: value / total_weight for key, value in st.session_state.slider_values.items()}

# Application des pondérations et calcul des scores
    @st.cache_data
    def apply_weights(data, weights):
        df_copy = data.copy()
        df_copy = df_copy.set_index(['dep_code', 'dep_nom', 'latitude_mairie', 'com_insee', 'coordonnees', 'population',
                                 'longitude_mairie', 'reg_nom', 'densite', 'com_nom', 'grille_densite', "indice_gare",
                                 "indice_charge_VE", "indice_littoral"])
        df_copy = df_copy.mul(pd.Series(weights), axis=1)  # Appliquer les pondérations
        df_copy["score_de_ville"] = round(df_copy.sum(axis=1) * 100, 1)  # Calcul du score final
        return df_copy.reset_index()  # Réinitialiser l'index

    df_copy = apply_weights(df, normalized_weights)

    # Apply transformations to the copy
    df_copy = df.copy()  # Create a copy of the DataFrame
    df_copy = df_copy.set_index(['dep_code', 'dep_nom', 'latitude_mairie', 'com_insee', 'coordonnees', 'population',
                            'longitude_mairie', 'reg_nom', 'densite', 'com_nom', 'grille_densite',"indice_gare","indice_charge_VE","indice_littoral"])  # Set index before mapping
    # Apply normalized weights
    df_copy = df_copy.mul(pd.Series(normalized_weights), axis=1)  # Apply weights
    # Calculate final score
    df_copy["score_de_ville"] = round(df_copy.sum(axis=1) * 100, 1)  # Calculate final score
    df_copy = df_copy.reset_index()  # Reset index for display

    # Appliquer les checkbox principaux sur filtered_data
    if littoral:
        st.write("Afficher les communes littorales de France métropolitaine.")
        filtered_data = filtered_data[filtered_data["indice_littoral"] == 1]
        if len(filtered_data) == 0:
            st.warning("Aucune commune ne correspond aux critères sélectionnés après application du filtre littoral.")
    # Ajouter une checkbox pour les communes ayant une gare
    if gare:
        st.write("Afficher les communes ayant une gare ferroviaire.")
        filtered_data = filtered_data[filtered_data["indice_gare"] == 1] 
        if len(filtered_data) == 0:
            st.warning("Aucune commune ne correspond aux critères sélectionnés après application du filtre gare.")
    # Ajouter une checkbox pour les communes ayant des charge VE
    if charge_VE:
        st.write("Afficher les communes ayant une borne de recharge VE.")
        filtered_data = filtered_data[filtered_data["indice_charge_VE"] == 1] 
        if len(filtered_data) == 0:
            st.warning("Aucune commune ne correspond aux critères sélectionnés après application du filtre charge_VE.")
        
    if top50:
        if len(filtered_data) == 0:
            st.warning("Aucune commune ne correspond aux critères sélectionnés.")
        elif len(filtered_data) < 50:
            st.write(f"Il y a {len(filtered_data)} correspondant à vos critères.")
            filtered_data = filtered_data.copy()
            if "score_de_ville" not in filtered_data.columns:
                filtered_data = filtered_data.set_index(['dep_code', 'dep_nom', 'latitude_mairie', 'com_insee', 
                                                        'coordonnees', 'population', 'longitude_mairie', 
                                                        'reg_nom', 'densite', 'com_nom', 'grille_densite'])
                filtered_data = filtered_data.mul(pd.Series(normalized_weights), axis=1)
                filtered_data["score_de_ville"] = round(filtered_data.sum(axis=1) * 100, 2)
                filtered_data = filtered_data.reset_index()
            filtered_data = filtered_data.sort_values(by="score_de_ville", ascending=False)
        else:
            st.write("Vous affichez le TOP 50 des communes de France métropolitaine correspondant à vos critères.")
            filtered_data = filtered_data.copy()
            if "score_de_ville" not in filtered_data.columns:
                filtered_data = filtered_data.set_index(['dep_code', 'dep_nom', 'latitude_mairie', 'com_insee', 
                                                        'coordonnees', 'population', 'longitude_mairie', 
                                                        'reg_nom', 'densite', 'com_nom', 'grille_densite'])
                filtered_data = filtered_data.mul(pd.Series(normalized_weights), axis=1)
                filtered_data["score_de_ville"] = round(filtered_data.sum(axis=1) * 100, 2)
                filtered_data = filtered_data.reset_index()
            filtered_data = filtered_data.sort_values(by="score_de_ville", ascending=False).head(50)

    if "score_de_ville" not in filtered_data.columns:
        filtered_data = filtered_data.set_index(['dep_code', 'dep_nom', 'latitude_mairie', 'com_insee', 
                                                'coordonnees', 'population', 'longitude_mairie', 
                                                'reg_nom', 'densite', 'com_nom', 'grille_densite'])
        filtered_data = filtered_data.mul(pd.Series(normalized_weights), axis=1)
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
        "score_de_ville": "Score de ville (sur 100)",
        "dep_nom": "Département", 
        "reg_nom": "Région"}, inplace=True)
    # Reset index for display
    top_5_communes = top_5_communes.reset_index(drop=True)
    top_5_communes.index += 1

    top_5_communes["Population"] = top_5_communes["Population"].astype(int)
    top_5_communes["Population"] = top_5_communes["Population"].apply(lambda x: f"{x:,}")
    top_5_communes["Score de ville (sur 100)"] = top_5_communes["Score de ville (sur 100)"].map("{:.2f}".format)

    # Affichage
    st.subheader("Top 5 communes par score de ville")
    st.table(top_5_communes[["Commune", "Score de ville (sur 100)", "Population", "Département", "Région"]])

    # Configurer kepler

    @st.cache_resource
    def get_kepler_config(style, lat, lon, zoom):
     return {
        "version": "v1",
        "config": {
            "mapState": {
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 0,
                "bearing": 0,
            },
            "mapStyle": {
                "styleType": style
            }
        }
    }

    config = get_kepler_config(
    "dark" if dark_mode else "light",
    center_lat, 
    center_lon, 
    zoom_level
)

    map_ = KeplerGl(height=800, config=config)
    #add filtered data to kepler
    map_.add_data(data=filtered_kepler_data, name="Filtered Data")
    #save map to html and integrate to streamlit
    map_.save_to_html(file_name='kepler_map.html', read_only=True)
    st.components.v1.html(open('kepler_map.html', 'r').read(), height=800)

with tab2:
    if st.session_state.active_tab == "TABLEAUX":
        st.session_state.active_tab = "TABLEAUX"
        st.header("Tableaux Dynamique")

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

    # Arrondir la colonne 'Loyer Abordable' à 2 décimales
    df2_filtered['indice_loyer_norm'] = df2_filtered['indice_loyer_norm'].round(2)
    #formatage des colonnes salaires / taux
    df2_filtered['prive'] = df2_filtered['prive'].apply(lambda x: f"{x} €" if pd.notnull(x) else "")
    df2_filtered['publique'] = df2_filtered['publique'].apply(lambda x: f"{x} €" if pd.notnull(x) else "")
    df2_filtered['T2_2024'] = df2_filtered['T2_2024'].apply(lambda x: f"{x} %" if pd.notnull(x) else "")

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
        'risque_minier': 'Risque minier',
        'Ecole_maternelle': 'École maternelle',
        'Ecole_elementaire': 'École élémentaire',
        'Lycee': 'Lycée',
        'College': 'Collège',
        'Medico_social': 'Médico-social'
    })

    # Tables à afficher avec les nouveaux noms de colonnes
    tables = {
        "Données Globales": df2_filtered[['Code_insee', 'Commune', 'Région', 'Département', 'Population', 'Urbanisation']],
        "Commerces": df2_filtered[['Commune', 'Boulangerie / Pâtisserie', 'Banque', 'Commerce de proximité', 'Cinéma', 'Pharmacie', 'Tabac', 'Garagiste', 'Restaurant', 'Café / Bar', 'Boite de nuit', 'Bureau de poste', 'Bibliothèque', 'Centre commercial', 'Ski', 'Surf', 'Location de bateau', 'Supermarché']],
        "Écoles": df2_filtered[['Commune','École maternelle','École élémentaire', 'Lycée', 'Collège', 'Médico-social']],
        "Transport": df2_filtered[['Commune', 'Gares', 'Stations de charges voitures electriques']],
        "Pouvoir d'achat": df2_filtered[['Commune', 'Taux de chômage', 'Loyer Abordable', 'Salaire privé', 'Salaire publique']],
        "Santé": df2_filtered[['Commune', 'Accès aux médecins généralistes', 'Accès aux sages-femmes', 'Accès aux kinésithérapeutes', 'Accès aux infirmières', 'Accès aux dentistes']],
        "Environnement": df2_filtered[['Commune','Jours ensoleillés par an','En bord de mer']],
        "Risques": df2_filtered[['Commune','Catastrophe naturelle','Zone inondable','Risque technologique','Risque minier']]
    }

    for table_name, table_data in tables.items():
        st.subheader(table_name)
        if table_name == "Santé":
            st.markdown("La table Santé présente l'APL (Accessibilité Potentielle Localisée), qui traduit le nombre de spécialistes disponibles par habitant dans un rayon de 20 minutes de déplacement en voiture.")
        table_data_no_index = table_data.reset_index(drop=True)  # Réinitialise l'index
        st.dataframe(table_data_no_index, hide_index=True)

#onglet mode d'emploi
with tab3:
    if st.session_state.active_tab == "MODE D'EMPLOI":
        st.session_state.active_tab = "MODE D'EMPLOI"
        st.header("Mode d'Emploi")
    st.subheader('La SIDEBAR', divider=True)
    st.write('Organe d\'intéraction principal du site, il permet de régler les paramètres de sélection du lieu de vie idéal.')
    st.write('**Options d\'affichage**')
    st.write('Par défaut, la CARTE affiche toutes les communes de notre dataset (34,881). Vous pouvez ici choisir 3 filtrages, afin de réduire ce nombre et rendre la carte plus intelligible :')
    st.write('- Afficher le top 50: Affiche le top 50 des communes correspondant aux autres critères sélectionnés.')
    st.write('- Afficher seulement les communes littorales: Affiche seulement les communes qui ont un accès direct à la mer.')
    st.write('- Cherchez une commune: Barre de recherche qui vous permet de chercher une commune en particulier. Attention à l\'orthographe, il faut les tirets("-") et les accents pour retrouver la bonne commune. Vous pouvez consulter les détails concernant cette commune dans l\'onglet Tableaux.')
    st.write('**Ajustez vos préférences**')
    st.write('Ici vous entrez dans le "vif du sujet". Vous pouvez faire varier les paramètres de 0 (ne pas en tenir compte) à 9 (crucial à vos yeux).')
    st.write('La variation de ces paramètres génère un score de ville pour chaque commune de France, sur la base de calculs qui sont détaillés dans l\'onglet "Documentation".')
    st.write('Concrètement, sur l\'interface de l\'onglet "Carte", vous verrez les communes dans le tableau Top 5 changer en fonction de vos paramètres, ainsi que la couleur des communes de la carte (jaune pour les communes avec un score très positif, violet pour les scores négatifs).')
    st.subheader('L\'onglet CARTE', divider=True)
    st.write('L\'onglet Carte est divisé en trois grandes parties :')
    st.write('- Une barre de filtres, qui vous permettent de choisir une région et/ou un département en particulier et/ou une taille d\'urbanisation (taille de la commune en fonction de la grille de densité telle que définie par l\'INSEE).')
    st.write('- Un tableau présentant le top 5 des communes par score de ville, en fonction des paramètres définis dans la sidebar.')
    st.write('- Une carte intéractive, présentant par défaut toutes les communes de France présentes dans notre base de données, que vous pouvez faire varier avec les paramètres de la sidebar et la barre de filtres.')
    st.subheader('L\'onglet TABLEAUX', divider=True)
    st.write('L\'onglet Tableaux fonctionne avec la barre de recherche des communes présent dans la sidebar :')
    st.write('Recherchez une commune précise en faisant attention à l\'orthographe (il faut les tirets(-), les apostrophes (\') et les accents pour retrouver la bonne commune).')
    st.write('Vous trouverez ici le détail des valeurs pour chaque catégorie permettant de calculer le score de ville pour la commune associée.')
    st.write('- Données globales : données administratives liées à la commune.')
    st.write('- Commerces : indique la présence ou l\'absence des commerces indiqués en colonne.')
    st.write('- Écoles : indique la présence ou l\'absence des établissements scolaires en fonction du niveau.')
    st.write('- Transport : indique la présence ou l\'absence des gares ferroviaires et des stations de recharge de véhicules électrique.')
    st.write('- Pouvoir d\'achat : indique le pourcentage de taux de chômage départemental, un indice normalisé des prix des loyers sur la commune (1 = loyer abordable, 0 = loyer très élevé), et les moyennes départementales pour les salaires privés et les salaires publics.')
    st.write('- Santé : présente l\'APL (Accessibilité Potentielle Localisée), qui traduit le nombre de spécialistes disponibles par habitant dans un rayon de 20 minutes de déplacement en voiture.')
    st.write('- Environnement : présente le nombre de jours d\'ensoleillement par an sur le département et si la commune est située sur le littoral ou non.')
    st.write('- Risques : Présente la présence ou l\'absence de géorisques de différentes nature sur la commune (Catastrophes naturelles, zones inondables, risques technologiques, risques miniers).')
    st.subheader('L\'onglet DOCUMENTATION', divider=True)
    st.write('L\'onglet Documentation présente toutes les étapes  de la construction de la base de données ainsi que les sources des tables ayant servi à la construction de la base de données.')
#onglet documentation
with tab4:
    if st.session_state.active_tab == "DOCUMENTATION":
        st.session_state.active_tab = "DOCUMENTATION"
        st.header("Documentation")
    st.write('La section "Documentation" présente les étapes  de la construction de la base de données avec les transformations appliquées et les calculs nécessaires à la création des indices de qualité de vie.')
    st.write('Vous trouverez également toutes les sources de notre base de données en bas de page.')

    st.header('Construction de la base de données')
    left, right = st.columns(2, vertical_alignment="top")
    left.image('flowchart_mermaid.png')
    right.write('')
    right.write('**Étape 1** : Upload des tables brutes (raw data) dans BiqQuery.')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('**Étape 2** : Cleaning préliminaire des tables via SQL directement sur BigQuery.')
    right.write('**Étape 2 bis** : Transformation des tables via python pour les transformations les plus complexes.')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('**Étape 3** : En fonction du nettoyage des données, étude de l\'adaptabilité de chaque paramètre à notre projet, et sélection des indices retenus pour le calcul du "score de ville".')
    right.write('**Indices retenus** : santé, écoles, risques, loyers, sécurité, culture/loisirs, alimentation/services, salaires, taux de chômage, transports ferroviaires, véhicules électriques, littoral, ensoleillement.')
    right.write('')
    right.write('')
    right.write('')
    right.write('**Étape 4** : Certaines tables avaient en commun leur thématique, justifiant leur réunion en une seule table.')
    right.write('C\'était le cas, par exemple, des datasets sur la santé (divisés par spécialiste), sur les risques (divisés par type de risque), sur les loyers (séparés par type de logement), ou encore sur les salaires (séparés par catégorie socio-professionnelle)')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('**Étape 4 bis** : Dans le cas des indices complexes (utilisant plusieurs tables ou plusieurs colonnes pour créer un seul indice), on ne pouvait pas procéder directement à la création des indices.')
    right.write('Il a fallu dans un premier temps réunir les colonnes dans une seule table, normaliser les colonnes via une normalisation min-max, et ensuite créer l\'indice en pondérant les colonnes.')
    right.write('Voir **l\'exemple ci-dessous** illustrant la création de l\'indice Santé')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('**Étape 5 et 6** : Création des indices pour toutes les tables et les normaliser entre 0 et 1 afin de pouvoir comparer tous les paramètres retenus pour la création du score de ville.')
    right.write('Formule de la normalisation appliquée pour la création des indices:')
    right.latex(r'''
    x_{\text{norm}} = \frac{x - x_{\text{min}}}{x_{\text{max}} - x_{\text{min}}}
    ''')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('')
    right.write('**Étape 7** : Création d\'un "Proof of Concept" (POC) avec des indices à la pondération fixe et prédéterminée, afin de tester les variations du score de ville en fonction de la pondération affectée aux paramètres.')
    right.write('**Étape 8** : Création du produit définitif: rendre la pondération des indices dynamique en demandant à l\'utilisateur de donner un poids aux critères qu\'il juge les plus déterminants dans son choix de lieu de vie idéal, et calculer le score de ville en fonction de ses choix.')
    right.write('Formule définitive du calcul du score de ville:')
    right.latex(r'''
    \text{score\_de\_ville} = \sum_{i=1}^{n} \left( \text{pondération}_i \times x_{\text{norm}, i} \right) \times 100
    ''')
    right.write('Où : ')
    right.latex(r'''
    n \text{ est le nombre d'indices,} \\
    \text{pondération}_i \text{ est la pondération normalisée pour chaque indice } i, \\
    x_{\text{norm}, i} \text{ est la valeur normalisée de l'indice } i.
    ''')

    st.subheader('Exemple de transformations via SQL pour la création d\'un indice à partir d\'une table complexe')
    st.write('Exemple de la création de l\'indice Santé')
    st.code(f"""
-- ----------------- TABLE DÉFINITIVE -----------------
-- Étape 1: Normalisation de chaque colonne
CREATE OR REPLACE TABLE projet-qv.agg_data.indice_sante AS
WITH t1 AS (
  SELECT
    code_commune,
    libelle_commune,
    apl_aux_meds_ge,
    (apl_aux_meds_ge - MIN(apl_aux_meds_ge) OVER ()) / 
    (MAX(apl_aux_meds_ge) OVER () - MIN(apl_aux_meds_ge) OVER ()) AS apl_aux_meds_ge_norm,
    
    apl_aux_sages_femmes,
    (apl_aux_sages_femmes - MIN(apl_aux_sages_femmes) OVER ()) / 
    (MAX(apl_aux_sages_femmes) OVER () - MIN(apl_aux_sages_femmes) OVER ()) AS apl_aux_sages_femmes_norm,
    
    apl_aux_kines,
    (apl_aux_kines - MIN(apl_aux_kines) OVER ()) / 
    (MAX(apl_aux_kines) OVER () - MIN(apl_aux_kines) OVER ()) AS apl_aux_kines_norm,
    
    apl_aux_infirmieres,
    (apl_aux_infirmieres - MIN(apl_aux_infirmieres) OVER ()) / 
    (MAX(apl_aux_infirmieres) OVER () - MIN(apl_aux_infirmieres) OVER ()) AS apl_aux_infirmieres_norm,
    
    apl_aux_dentistes,
    (apl_aux_dentistes - MIN(apl_aux_dentistes) OVER ()) / 
    (MAX(apl_aux_dentistes) OVER () - MIN(apl_aux_dentistes) OVER ()) AS apl_aux_dentistes_norm
  FROM projet-qv.join_data.join_sante
),

-- Étape 2: Pondération des apl_normalisés + ajout d'un score par commune
-- meds_ge = 40%, sf, ki, inf, de = 15% chacun
t2 AS (
  SELECT
    t1.code_commune,
    t1.libelle_commune,
    (0.40 * t1.apl_aux_meds_ge_norm) + 
    (0.15 * t1.apl_aux_sages_femmes_norm) + 
    (0.15 * t1.apl_aux_kines_norm) + 
    (0.15 * t1.apl_aux_infirmieres_norm) + 
    (0.15 * t1.apl_aux_dentistes_norm) AS indice_APL_all
  FROM t1
)

-- Étape 3: Normalisation de l'indice_APL_all
SELECT
  cc.code_insee,
  cc.nom_standard,
  (t2.indice_APL_all - MIN(t2.indice_APL_all) OVER ()) / 
  (MAX(t2.indice_APL_all) OVER () - MIN(t2.indice_APL_all) OVER ()) AS indice_sante
FROM projet-qv.clean_data.clean_communes AS cc
LEFT JOIN t2 ON cc.code_insee = t2.code_commune;
""")

    #section sources
    st.header('Sources')
    st.subheader('Données globales') ###########################################
    st.write('Tables: Populations légales en 2021 (publié le 26/01/2024).')
    st.write('Source: https://www.insee.fr/fr/statistiques/7739582')
    st.write('Producteur: INSEE (Institut National de la Statistique et des Études Économiques)')
    st.subheader('Indice Santé') ###########################################
    st.write('Tables: médecins généralistes, infirmières, sages-femmes, chirurgiens-dentistes, kinés.')
    st.write('Source: https://drees.shinyapps.io/carto-apl/')
    st.write('Producteur: Ministère des Solidarités et de la Santé, Direction de la recherche, des études, de l\'évaluation et des statistiques')
    st.subheader('Indice Écoles') ###########################################
    st.write('Tables: Annuaire de l\'éducation (établissements scolaires par commune).')
    st.write('Source: https://data.education.gouv.fr/explore/dataset/fr-en-annuaire-education/table/')
    st.write('Producteur: Ministère de l\'Education nationale')
    st.subheader('Indice Risques') ###########################################
    st.write('Tables: Gestion ASsistée des Procédures Administratives relatives aux Risques (GASPAR) = table des zones inondables, des catastrophes naturelles, du PPRM (Plan de Prévention des Risques Miniers) et du PPRT (Plan de Prévention des Risques Technologiques).')
    st.write('Source: https://www.georisques.gouv.fr/donnees/bases-de-donnees')
    st.write('Producteur: Ministère de la Transition Écologique, de l\'Énergie, du Climat, et de la Prévention des Risques et le BRGM (établissement public français pour les applications des sciences de la Terre).')
    st.subheader('Indice Gares ferroviaires') ###########################################
    st.write('Tables: Gares.')
    st.write('Source: https://www.data.gouv.fr/fr/datasets/liste-des-gares/')
    st.write('Producteur: SNCF')
    st.subheader('Indice Bornes de Recharge Véhicules Électriques') ###########################################
    st.write('Tables: Bornes de Recharge Véhicules Électriques.')
    st.write('Source: https://www.data.gouv.fr/fr/datasets/5448d3e0c751df01f85d0572/')
    st.write('Producteur: Data Gouv (Direction Interministérielle du Numérique)')
    st.subheader('Indice Littoral') ###########################################
    st.write('Tables: Communes littorales en France')
    st.write('Source: https://www.data.gouv.fr/fr/datasets/communes-de-la-loi-littoral-au-code-officiel-geographique-cog-2020-2022/')
    st.write('Producteur: Ministère de la Cohésion des territoires')
    st.subheader('Indice Loyers') ###########################################
    st.write('Tables: Loyers appartements 1 pc, Loyers appartements 2 pcs, Loyers appartements 3 pcs, Loyers maisons')
    st.write('Source: https://www.data.gouv.fr/fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2022/')
    st.write('Producteur: Ministère de la Transition écologique')
    st.subheader('Indice Sécurité') ###########################################
    st.write('Tables: Bases statistiques communale, départementale et régionale de la délinquance enregistrée par la police et la gendarmerie nationales ')
    st.write('Source: https://www.data.gouv.fr/fr/datasets/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/')
    st.write('Producteur: Ministère de l\'Intérieur')
    st.subheader('Indice Culture/Loisirs et Indice Alimentation/Services') ###########################################
    st.write('Tables: Commerces.')
    st.write('Source: https://www.data.gouv.fr/fr/datasets/base-nationale-des-commerces-ouverte/#/resources')
    st.write('Producteur: "Ça reste ouvert" via OpenStreetMaps')
    st.subheader('Indice Ensoleillement') ###########################################
    st.write('Tables: Nombre de jours d\'ensoleillement par département et par an')
    st.write('Source: https://www.data.gouv.fr/fr/datasets/63909449447299655d304248/')
    st.write('Producteur: Hello Watt')
#onglet about
with tab5:
    if st.session_state.active_tab == "ABOUT":
        st.session_state.active_tab = "ABOUT"
        st.header("À propos")
    st.header('About')
    st.write('Base de données et application construites dans le cadre du projet final du Bootcamp "Data Analytics" du Wagon, Batch#1864.')
    st.write('Les sources de notre base de données sont listées dans l\'onglet "Documentation".')

    st.write('**Développé par:**')
    col1, col2, col3, col4, col5, a, b, c, d = st.columns(9, vertical_alignment="top")
    col1.link_button("Charles Durand", "https://www.linkedin.com/in/charlesdurandpro/")
    col2.link_button('Galaad Bastos', "https://www.linkedin.com/in/galaad-bastos")
    col3.link_button('Ilann Gaillard', "https://www.linkedin.com/in/ilann-gaillard-286b91224/")
    col4.link_button('Maria Vincent', "https://www.linkedin.com/in/maria-vincent-387a24161/")
    col5.link_button('Wenxuan Qiao', "https://www.linkedin.com/in/wenxuan-qiao-87989516b/")

    st.write('Décembre 2024.')
