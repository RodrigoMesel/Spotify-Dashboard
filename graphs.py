import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Configuração Inicial ---
st.set_page_config(page_title="Dashboard Spotify - Análise", layout="wide")
st.title("Dashboard Spotify: Análise Exploratória (2015-2025)")
st.markdown("Visualizações interativas convertidas para Plotly Express.")

# --- Carregamento dos Dados ---
@st.cache_data
def load_data():
    # Caminho do arquivo original do notebook
    url = "spotify_data_processed.csv"
    try:
        df = pd.read_csv(url)
    except FileNotFoundError:
        st.error(f"Arquivo '{url}' não encontrado no diretório local.")
        st.stop()
            
    # Remoção das colunas como no notebook original
    colunas_drop = ['key', 'loudness', 'mode', 'instrumentalness', 'tempo',
                    'explicit', 'label', 'loudness_category', 'key_name',
                    'mode_name', 'release_quarter', 'is_weekend_release',
                    'log_stream_count', 'upbeat_score', 'artist_track_count']
    df = df.drop(columns=[col for col in colunas_drop if col in df.columns], errors='ignore')
    return df

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

# Aplica o filtro de ano
df_filtrado = df[(df['release_year'] >= anos_selecionados[0]) & (df['release_year'] <= anos_selecionados[1])]

# --- Visão Geral (Valores Nulos) ---
with st.expander("Verificar Qualidade dos Dados (Valores Nulos)"):
    st.markdown("Heatmap de valores nulos (originalmente feito com `sns.heatmap`)")
    fig_null = px.imshow(
        df_filtrado.isnull(),
        aspect="auto",
        color_continuous_scale="gray",
        labels=dict(x="Colunas", y="Índice das Linhas", color="É Nulo?"),
        title="Mapa de Calor de Valores Faltantes"
    )
    fig_null.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_null, use_container_width=True)

# Layout em Colunas
col1, col2 = st.columns(2)

# --- Gráfico 1: Top 10 Artistas ---
with col1:
    groupedArtists = df_filtrado.groupby('artist_name')['stream_count'].sum().reset_index()
    top10Artists = groupedArtists.sort_values(by='stream_count', ascending=False).head(10)

    fig_artists = px.bar(
        top10Artists,
        x='stream_count',
        y='artist_name',
        orientation='h',
        color='stream_count',
        color_continuous_scale='mako',
        labels={'stream_count': 'Total de Streams', 'artist_name': 'Artista'},
        title='Top 10 Artistas com Mais Streams'
    )
    fig_artists.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_artists, use_container_width=True)

# --- Gráfico 2: Top 10 Gêneros ---
with col2:
    groupedGenres = df_filtrado.groupby('genre')['stream_count'].sum().reset_index()
    top10Genres = groupedGenres.sort_values(by='stream_count', ascending=False).head(10)

    fig_genres = px.bar(
        top10Genres,
        x='stream_count',
        y='genre',
        orientation='h',
        color='stream_count',
        color_continuous_scale='rocket',
        labels={'stream_count': 'Total de Streams', 'genre': 'Gênero'},
        title='Top 10 Gêneros Musicais por Volume de Streams'
    )
    fig_genres.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_genres, use_container_width=True)

# Outra linha de layout
col3, col4 = st.columns(2)

# --- Gráfico 3: Evolução dos Streams por Ano ---
with col3:
    streams_by_year = df_filtrado.groupby('release_year')['stream_count'].sum().reset_index()
    
    fig_streams_year = px.line(
        streams_by_year, 
        x='release_year', 
        y='stream_count', 
        markers=True,
        labels={'release_year': 'Ano de Lançamento', 'stream_count': 'Total de Streams'},
        title=f'Evolução do Volume de Streams ({anos_selecionados[0]}-{anos_selecionados[1]})'
    )
    fig_streams_year.update_traces(line=dict(width=3))
    st.plotly_chart(fig_streams_year, use_container_width=True)

# --- Gráfico 4: Popularidade Média por Ano ---
with col4:
    pop_year = df_filtrado.groupby('release_year')['popularity'].mean().reset_index()
    
    fig_pop_year = px.line(
        pop_year, 
        x='release_year', 
        y='popularity', 
        markers=True,
        color_discrete_sequence=['orange'],
        labels={'release_year': 'Ano de Lançamento', 'popularity': 'Popularidade Média'},
        title='Popularidade Média das Músicas por Ano'
    )
    fig_pop_year.update_traces(line=dict(width=3))
    st.plotly_chart(fig_pop_year, use_container_width=True)


# --- Gráfico 5: Distribuição de Streams (Cauda Longa) ---
st.markdown("---")
artistas_streams = df_filtrado.groupby('artist_name')['stream_count'].sum().sort_values(ascending=False)
streams_acumulados = artistas_streams.cumsum()
porcentagem_acumulada = (streams_acumulados / artistas_streams.sum() * 100).reset_index(drop=True)

fig_long_tail = px.line(
    x=porcentagem_acumulada.index, 
    y=porcentagem_acumulada.values,
    color_discrete_sequence=['teal'],
    labels={'x': 'Número de Artistas (Ordenados do maior para menor)', 'y': 'Porcentagem Acumulada de Streams (%)'},
    title='Distribuição de Streams: A Cauda Longa dos Artistas'
)
# Adiciona linha de referência dos 80% (Pareto)
fig_long_tail.add_hline(y=80, line_dash="dash", line_color="gray", annotation_text="80% dos Streams")
fig_long_tail.update_traces(line=dict(width=3))
st.plotly_chart(fig_long_tail, use_container_width=True)


# --- Gráfico 6: Market Share dos 5 Principais Gêneros ---
st.markdown("---")
# Pega os Top 5 Gêneros do dataframe inteiro ou do filtrado dependendo da visão
genre_year_streams = df_filtrado.groupby(['release_year', 'genre'])['stream_count'].sum().unstack().fillna(0)
genre_market_share = genre_year_streams.div(genre_year_streams.sum(axis=1), axis=0) * 100

top_5_genres_all_time = df_filtrado.groupby('genre')['stream_count'].sum().nlargest(5).index
genre_market_share_top = genre_market_share[top_5_genres_all_time].reset_index()

# Derreter (melt) o dataframe para o Plotly Express formatar adequadamente as cores e áreas
genre_market_share_top_melted = genre_market_share_top.melt(id_vars='release_year', var_name='genre', value_name='market_share')

fig_market_share = px.area(
    genre_market_share_top_melted,
    x='release_year',
    y='market_share',
    color='genre',
    color_discrete_sequence=px.colors.qualitative.Set2,
    labels={'release_year': 'Ano', 'market_share': 'Porcentagem do Total de Streams (%)', 'genre': 'Gênero'},
    title='Evolução do Market Share dos 5 Principais Gêneros'
)
st.plotly_chart(fig_market_share, use_container_width=True)


# --- Gráfico 7: Mapa de Consistência ---
st.markdown("---")
artistas_contagem = df_filtrado['artist_name'].value_counts()
artistas_frequentes = artistas_contagem[artistas_contagem >= 5].index
df_freq = df_filtrado[df_filtrado['artist_name'].isin(artistas_frequentes)]

if not df_freq.empty:
    consistencia = df_freq.groupby('artist_name')['stream_count'].agg(['mean', 'std', 'max']).dropna()
    consistencia['CV'] = consistencia['std'] / consistencia['mean']
    
    # Categorizar artistas para colorir no Plotly
    consistencia['Categoria'] = 'Geral'
    
    # One-Hit Wonders e Consistentes
    one_hit_wonders = consistencia.sort_values(by='CV', ascending=False).head(5).index
    consistentes = consistencia.sort_values(by=['CV', 'mean'], ascending=[True, False]).head(5).index
    
    consistencia.loc[one_hit_wonders, 'Categoria'] = 'One-Hit Wonders'
    consistencia.loc[consistentes, 'Categoria'] = 'Artistas Consistentes'
    
    # Prepara pro Plotly
    consistencia_plot = consistencia.reset_index()
    
    # Mapeamento de cores original
    color_map = {
        'Geral': 'gray',
        'One-Hit Wonders': 'red',
        'Artistas Consistentes': 'green'
    }

    # Definir tamanho condicional (simulando sns.scatterplot e plt.scatter)
    consistencia_plot['Tamanho'] = consistencia_plot['Categoria'].apply(lambda x: 10 if x != 'Geral' else 4)

    fig_consistencia = px.scatter(
        consistencia_plot, 
        x='mean', 
        y='CV', 
        color='Categoria',
        color_discrete_map=color_map,
        size='Tamanho',
        hover_data=['artist_name'],
        labels={'mean': 'Média de Streams por Faixa (Log Scale)', 'CV': 'Variação entre as músicas (CV)'},
        title='Mapa de Consistência: Média de Streams vs. Coeficiente de Variação (CV)',
        log_x=True,
        opacity=0.7,
        size_max=15
    )
    
    fig_consistencia.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
    st.plotly_chart(fig_consistencia, use_container_width=True)
else:
    st.info("Não há dados suficientes para exibir o Mapa de Consistência com os filtros atuais.")

