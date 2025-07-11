# main.py
from fastapi import FastAPI, HTTPException              # type: ignore
from fastapi.responses import StreamingResponse         # type: ignore
from fastapi.middleware.cors import CORSMiddleware      # type: ignore

from datetime import datetime
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt                         # type: ignore
import seaborn as sns                                   # type: ignore

from app.plots import plot_monthly_city_rainfall
from app.utils import to_mm_yyyy
from app.rmr_analysis import comparar_rmr_dia_api


app = FastAPI(title='Chuvas API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://localhost:5174'],
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


@app.get('/comparar_rmr_dia/{city}', response_class=StreamingResponse,
         summary='Comparação de RMR por dia')
async def comparar_rmr_dia(city: str, start_date: str, end_date: str):
    '''
    Retorna um gráfico PNG comparando a RMR da cidade selecionada
    com a média das demais cidades, no período informado
    (YYYY-MM-DD a YYYY-MM-DD).
    '''
    # ── 1. Valida as datas ─────────────────────────────────
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError as exc:
        raise HTTPException(400, f'Formato de data inválido: {exc}')

    if start_date > end_date:
        raise HTTPException(400, 'A data de início deve ser anterior à data de término.')

    # ── 2. Gera a figura (Seaborn) ────────────────────────
    fig = comparar_rmr_dia_api(city, start_date, end_date)

    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf, media_type='image/png')


@app.get('/comparar_rmr_dia/{data}/{cidade}', response_class=StreamingResponse,
         summary='Comparação diária de óbitos e chuvas na RMR')
async def comparar_rmr_dia_endpoint(data: str, cidade: str):
    '''
    Retorna um gráfico PNG com a comparação de óbitos e chuvas
    para uma data e cidade específicas na RMR.
    Formato da data: YYYY-MM-DD
    '''
    try:
        # Valida formato da data
        datetime.strptime(data, '%Y-%m-%d')
        
        # Gera a figura usando a função de análise RMR
        fig = comparar_rmr_dia_api(data, cidade)
        
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
        plt.close(fig)
        buf.seek(0)
        
        return StreamingResponse(buf, media_type='image/png')
        
    except ValueError as exc:
        raise HTTPException(400, f'Formato de data inválido. Use YYYY-MM-DD: {exc}')
    except Exception as exc:
        raise HTTPException(500, f'Erro ao gerar gráfico: {exc}')
