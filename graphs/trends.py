import streamlit as st
import plotly.express as px
import pandas as pd

def render_streams_evolution(df: pd.DataFrame, anos_selecionados: tuple):
    streams_by_year = df.groupby('release_year')['stream_count'].sum().reset_index()
    
    fig_streams_year = px.line(
        streams_by_year, 
        x='release_year', 
        y='stream_count', 
        markers=True,
        color_discrete_sequence=['#1DB954'],
        labels={'release_year': 'Ano de Lançamento', 'stream_count': 'Total de Streams'},
        title=f'Evolução do Volume de Streams ({anos_selecionados[0]}-{anos_selecionados[1]})'
    )
    fig_streams_year.update_traces(line=dict(width=3))
    st.plotly_chart(fig_streams_year, width='stretch')

def render_popularity_evolution(df: pd.DataFrame):
    pop_year = df.groupby('release_year')['popularity'].mean().reset_index()
    
    fig_pop_year = px.line(
        pop_year, 
        x='release_year', 
        y='popularity', 
        markers=True,
        color_discrete_sequence=['#1DB954'],
        labels={'release_year': 'Ano de Lançamento', 'popularity': 'Popularidade Média'},
        title='Popularidade Média das Músicas por Ano'
    )
    fig_pop_year.update_traces(line=dict(width=3))
    st.plotly_chart(fig_pop_year, width='stretch')

