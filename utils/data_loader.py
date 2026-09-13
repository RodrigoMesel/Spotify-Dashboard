import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    url = "spotify_data_processed.csv"
    try:
        df = pd.read_csv(url)
    except FileNotFoundError:
        st.error(f"Arquivo '{url}' não encontrado no diretório local.")
        st.stop()
            
    colunas_drop = ['key', 'loudness', 'mode', 'instrumentalness', 'tempo',
                    'explicit', 'label', 'loudness_category', 'key_name',
                    'mode_name', 'release_quarter', 'is_weekend_release',
                    'log_stream_count', 'upbeat_score', 'artist_track_count']
    df = df.drop(columns=[col for col in colunas_drop if col in df.columns], errors='ignore')
    return df

