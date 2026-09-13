import streamlit as st
import plotly.express as px
import pandas as pd

def render_top_artists(df: pd.DataFrame):
    groupedArtists = df.groupby('artist_name')['stream_count'].sum().reset_index()
    top10Artists = groupedArtists.sort_values(by='stream_count', ascending=False).head(10)

    fig_artists = px.bar(
        top10Artists,
        x='stream_count',
        y='artist_name',
        orientation='h',
        color='stream_count',
        color_continuous_scale=['#08401e', '#1DB954', '#1ED760'],
        labels={'stream_count': 'Total de Streams', 'artist_name': 'Artista'},
        title='Top 10 Artistas com Mais Streams'
    )
    fig_artists.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_artists, width='stretch')

def render_long_tail(df: pd.DataFrame):
    artistas_streams = df.groupby('artist_name')['stream_count'].sum().sort_values(ascending=False)
    streams_acumulados = artistas_streams.cumsum()
    porcentagem_acumulada = (streams_acumulados / artistas_streams.sum() * 100).reset_index(drop=True)

    fig_long_tail = px.line(
        x=porcentagem_acumulada.index, 
        y=porcentagem_acumulada.values,
        color_discrete_sequence=['#1ED760'],
        labels={'x': 'Número de Artistas (Ordenados do maior para menor)', 'y': 'Porcentagem Acumulada de Streams (%)'},
        title='Distribuição de Streams: A Cauda Longa dos Artistas'
    )
    # Adiciona linha de referência dos 80%
    fig_long_tail.add_hline(y=80, line_dash="dash", line_color="gray", annotation_text="80% dos Streams")
    fig_long_tail.update_traces(line=dict(width=3))
    st.plotly_chart(fig_long_tail, width='stretch')

def render_consistency_map(df: pd.DataFrame):
    artistas_contagem = df['artist_name'].value_counts()
    artistas_frequentes = artistas_contagem[artistas_contagem >= 5].index
    df_freq = df[df['artist_name'].isin(artistas_frequentes)]

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
        
        consistencia_plot = consistencia.reset_index()
        
        color_map = {
            'Geral': '#404040',
            'One-Hit Wonders': '#FF4632',
            'Artistas Consistentes': '#1ED760'
        }

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
        st.plotly_chart(fig_consistencia, width='stretch')
    else:
        st.info("Não há dados suficientes para exibir o Mapa de Consistência com os filtros atuais.")

