import streamlit as st
import streamlit.components.v1 as components

def render_header():
    # --- Logo e Player do Spotify ---
    col_logo, col_player = st.columns([1, 2])

    with col_logo:
        st.image("https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_Green.png", width=300)

    with col_player:
        components.html(
            """
            <iframe data-testid="embed-iframe" style="border-radius:12px" src="https://open.spotify.com/embed/playlist/3TbaONdCxJkFmYn8ok1z77?utm_source=generator&theme=0&si=5414e245186e4e0b" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
            """,
            height=152
        )
