import streamlit as st
import plotly.express as px
import pandas as pd

def render_top_genres(df: pd.DataFrame):
    groupedGenres = df.groupby('genre')['stream_count'].sum().reset_index()
    top10Genres = groupedGenres.sort_values(by='stream_count', ascending=False).head(10)

    fig_genres = px.bar(
        top10Genres,
        x='stream_count',
        y='genre',
        orientation='h',
        color='stream_count',
        color_continuous_scale=['#08401e', '#1DB954', '#1ED760'],
        labels={'stream_count': 'Total de Streams', 'genre': 'Gênero'},
        title='Top 10 Gêneros Musicais por Volume de Streams'
    )
    fig_genres.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_genres, width='stretch')

def render_market_share(df: pd.DataFrame):
    genre_year_streams = df.groupby(['release_year', 'genre'])['stream_count'].sum().unstack().fillna(0)
    genre_market_share = genre_year_streams.div(genre_year_streams.sum(axis=1), axis=0) * 100

    top_5_genres_all_time = df.groupby('genre')['stream_count'].sum().nlargest(5).index
    genre_market_share_top = genre_market_share[top_5_genres_all_time].reset_index()

    # Derreter (melt) o dataframe para o Plotly Express formatar adequadamente as cores e áreas
    genre_market_share_top_melted = genre_market_share_top.melt(id_vars='release_year', var_name='genre', value_name='market_share')

    fig_market_share = px.area(
        genre_market_share_top_melted,
        x='release_year',
        y='market_share',
        color='genre',
        color_discrete_sequence=['#1DB954', '#509BF5', '#FF4632', '#FFC864', '#AF2896'],
        labels={'release_year': 'Ano', 'market_share': 'Porcentagem do Total de Streams (%)', 'genre': 'Gênero'},
        title='Evolução do Market Share dos 5 Principais Gêneros'
    )
    st.plotly_chart(fig_market_share, width='stretch')

