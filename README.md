# Spotify Dashboard

Um dashboard interativo desenvolvido em Streamlit e Plotly para análise exploratória de dados do Spotify (2015-2025). O projeto foi modularizado para facilitar a manutenção e escalabilidade.

## Estrutura do Projeto

- `app.py`: Arquivo principal da aplicação. Controla o layout e o sidebar.
- `components/`: Contém os componentes de interface (ex: `header.py` com a logo e player do Spotify).
- `graphs/`: Módulos responsáveis pela geração dos gráficos do Plotly.
  - `artists.py`: Gráficos relacionados a artistas.
  - `genres.py`: Gráficos focados nos gêneros musicais (ignoram filtros restritos).
  - `trends.py`: Gráficos de linha e evolução ao longo do tempo.
- `utils/`: Utilitários gerais.
  - `data_loader.py`: Script para carregamento, limpeza e cache dos dados.
- `.streamlit/`: Contém as configurações de tema da aplicação (Spotify Dark Theme).

## Como Executar

1. Crie o seu ambiente virtual e ative-o (exemplo com WSL/Linux):
   ```bash
   python3 -m venv st-venv
   source st-venv/bin/activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute a aplicação:
   ```bash
   streamlit run app.py
   ```