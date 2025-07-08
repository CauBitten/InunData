# main.py
from fastapi import FastAPI, HTTPException              # type: ignore
from fastapi.responses import StreamingResponse         # type: ignore
from fastapi.middleware.cors import CORSMiddleware      # type: ignore

from datetime import datetime
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt                         # type: ignore

from app.plots import plot_monthly_city_rainfall
from app.utils import to_mm_yyyy


app = FastAPI(title='Chuvas API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# ────────────────────────────
# 1. Pré-carrega os CSVs uma só vez
#    (evita custo de I/O a cada requisição)
# ────────────────────────────
DATA_BEFORE = pd.read_csv('./data/Chuvas/Chuvas18-21.csv', decimal=',')
DATA_AFTER  = pd.read_csv('./data/Chuvas/Chuvas21-25.csv', decimal=',')

CUTOFF = datetime(2021, 5, 1)


@app.get('/monthly_city_rainfall/{month_year}', response_class=StreamingResponse,
         summary='Top 15 cidades por chuva no mês')
async def monthly_city_rainfall(month_year: str):
    '''
    Retorna um gráfico PNG com as 15 cidades que mais choveram
    no mês informado (YYYY-MM-DD).
    '''
    # ── 1. Escolhe o dataframe certo ───────────────────────
    date = datetime.strptime(month_year, '%Y-%m-%d')
    data = DATA_BEFORE if date <= CUTOFF else DATA_AFTER

    # ── 2. Normaliza/valida a data ─────────────────────────
    try:
        date = to_mm_yyyy(month_year)     
    except ValueError as exc:
        raise HTTPException(400, f'Formato de data inválido: {exc}')

    # ── 3. Gera a figura (Matplotlib) ──────────────────────
    fig = plot_monthly_city_rainfall(data, date, top_n=15)

    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')  
    plt.close(fig)                                     
    buf.seek(0)

    return StreamingResponse(buf, media_type='image/png')
