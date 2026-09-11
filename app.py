import streamlit as st
import pandas as pd

from utils.data_loader import load_data
from components.header import render_header
from graphs.artists import render_top_artists, render_long_tail, render_consistency_map
from graphs.genres import render_top_genres, render_market_share
from graphs.trends import render_streams_evolution, render_popularity_evolution

# --- Configuração Inicial ---
st.set_page_config(page_title="Dashboard Spotify - Análise", layout="wide")
st.title("Dashboard Spotify: Análise Exploratória (2015-2025)")

def main():
    # Carregamento dos dados
    df = load_data()

    # --- Filtros / Parâmetros do Usuário ---
    st.sidebar.header("Filtros do Dashboard")
    ano_min = int(df['release_year'].min()) if 'release_year' in df.columns else 2015
    ano_max = int(df['release_year'].max()) if 'release_year' in df.columns else 2025

    anos_selecionados = st.sidebar.slider(
        "Filtrar por Período de Lançamento (Ano):", 
        min_value=ano_min, 
        max_value=ano_max, 
        value=(ano_min, ano_max)
    )

    # Aplica o filtro de ano base
    df_filtrado = df[(df['release_year'] >= anos_selecionados[0]) & (df['release_year'] <= anos_selecionados[1])]

    # --- Filtro de Gênero ---
    todos_generos = sorted(df['genre'].dropna().unique())
    generos_selecionados = st.sidebar.multiselect(
        "Filtrar por Gênero(s):",
        options=todos_generos,
        default=[]
    )

    if generos_selecionados:
        df_filtrado_genero = df_filtrado[df_filtrado['genre'].isin(generos_selecionados)]
    else:
        df_filtrado_genero = df_filtrado.copy()

    # --- Renderização do Dashboard ---
    
    # Cabeçalho (Logo e Player)
    render_header()

    # Primeira linha: Top Artistas e Top Gêneros
    col1, col2 = st.columns(2)
    with col1:
        render_top_artists(df_filtrado_genero)
    with col2:
        # Nota: Market Share e Top Generos usam o df_filtrado (ignoram o filtro de genero)
        render_top_genres(df_filtrado)

    # Segunda linha: Evolução de Streams e Popularidade
    col3, col4 = st.columns(2)
    with col3:
        render_streams_evolution(df_filtrado_genero, anos_selecionados)
    with col4:
        render_popularity_evolution(df_filtrado_genero)

    # Terceira linha: Cauda Longa
    st.markdown("---")
    render_long_tail(df_filtrado_genero)

    # Quarta linha: Market Share (ignora filtro de gênero)
    st.markdown("---")
    render_market_share(df_filtrado)

    # Quinta linha: Mapa de Consistência
    st.markdown("---")
    render_consistency_map(df_filtrado_genero)

if __name__ == "__main__":
    main()

