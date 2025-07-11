import pandas as pd
import folium
import os
from typing import Tuple, Optional

def carregar_dados_mortalidade():
    """Carrega e processa os dados de mortalidade"""
    dfs = []
    for ano in range(2018, 2024):
        caminho = f'./data/MortalidadeBrasil/ETLSIM.DORES_PE_{ano}_t.csv'
        try:
            df = pd.read_csv(caminho, encoding='latin-1', sep=',', dtype={'CODMUNRES': str})
            dfs.append(df)
        except FileNotFoundError:
            continue
    
    if not dfs:
        return pd.DataFrame()
    
    return pd.concat(dfs, ignore_index=True)

def preprocessar_dados_chuva():
    """Pré-processa dados de chuva"""
    try:
        df1 = pd.read_csv('./data/Chuvas/Chuvas18-21.csv', sep=',', decimal=',', encoding='utf-8', dtype=str)
        df2 = pd.read_csv('./data/Chuvas/Chuvas21-25.csv', sep=',', decimal=',', encoding='utf-8', dtype=str)
    except FileNotFoundError:
        return pd.DataFrame()

    df_chuva = pd.concat([df1, df2], ignore_index=True)

    # Padronização temporal
    meses = {
        'jan./': '01/', 'fev./': '02/', 'mar./': '03/', 'abr./': '04/',
        'mai./': '05/', 'jun./': '06/', 'jul./': '07/', 'ago./': '08/',
        'set./': '09/', 'out./': '10/', 'nov./': '11/', 'dez./': '12/'
    }

    for old, new in meses.items():
        df_chuva['Mês/Ano'] = df_chuva['Mês/Ano'].str.replace(old, new)

    # Normalização de nomes geográficos
    mapeamento_cidades = {
        'Araçoiaba (Granja Cristo Redentor)': 'Araçoiaba',
        'Cabo (Barragem de Gurjaú)': 'Cabo de Santo Agostinho',
        'Cabo (Barragem de Suape)': 'Cabo de Santo Agostinho',
        'Cabo (Pirapama)': 'Cabo de Santo Agostinho',
        'Ipojuca (Suape) - PCD': 'Ipojuca',
        'Jaboatão (Cidade da Copa) - PCD': 'Jaboatão dos Guararapes',
        'Recife (Codecipe / Santo Amaro)': 'Recife',
        'Recife (Várzea)': 'Recife',
        'São Lourenço da Mata (Tapacurá)': 'São Lourenço da Mata'
    }

    df_chuva['Posto'] = df_chuva['Posto'].replace(mapeamento_cidades)

    # Conversão numérica
    day_cols = [str(i) for i in range(1, 32)]
    for col in day_cols + ['Acumulado']:
        df_chuva[col] = (
            df_chuva[col]
            .str.replace('[^0-9,]', '', regex=True)
            .str.replace(',', '.')
            .replace('', '0')
            .astype(float)
        )

    df_chuva = df_chuva.groupby(['Mês/Ano', 'Posto']).first().reset_index()
    return df_chuva

def processar_dados_chuva():
    """Processa dados de chuva para formato long"""
    df_chuva = preprocessar_dados_chuva()
    if df_chuva.empty:
        return pd.DataFrame()
    
    df_chuva_reform = df_chuva.melt(
        id_vars=['Posto', 'Mês/Ano'],
        value_vars=[str(i) for i in range(1, 32)],
        var_name='Dia',
        value_name='Chuva_mm'
    )
    
    df_chuva_reform['Dia'] = df_chuva_reform['Dia'].astype(int)
    return df_chuva_reform

def corrigir_df_rmr(df):
    """Corrige e formata dados de mortalidade"""
    # Converter datas
    df['DTOBITO'] = pd.to_datetime(
        df['DTOBITO'].astype(str).str.zfill(8),
        format='%d%m%Y',
        errors='coerce'
    )

    # Ajustar encoding
    df['ocor_MUNNOME'] = (
        df['ocor_MUNNOME']
        .str.encode('latin-1').str.decode('utf-8', errors='ignore')
        .replace({
            'SÃ£o LourenÃ§o da Mata': 'São Lourenço da Mata',
            'JaboatÃ£o dos Guararapes': 'Jaboatão dos Guararapes',
            'Ilha de ItamaracÃ¡': 'Ilha de Itamaracá',
            'AraÃ§oiaba': 'Araçoiaba'
        })
    )

    # Mapear variáveis categóricas
    df['SEXO'] = df['SEXO'].map({1: 'Masculino', 2: 'Feminino', 0: 'Ignorado'})

    # Corrigir idade
    if 'idade_obito_anos' not in df.columns and 'IDADE' in df.columns:
        df['idade_obito_anos'] = df['IDADE'] // 365

    # Remover colunas vazias
    cols_vazias = [col for col in df.columns if df[col].isna().all()]
    df = df.drop(columns=cols_vazias)

    return df

def processar_dados_mortalidade(df):
    """Processa dados de mortalidade para RMR"""
    # Códigos IBGE dos municípios da RMR
    codigos_rmr_6digitos = [
        '261160', '260790', '260960', '261070', '260290', '260345',
        '261370', '260680', '260005', '260720', '260940', '260105',
        '260775', '260760'
    ]

    nomes_municipios = {
        '260005': 'Abreu e Lima', '260105': 'Araçoiaba',
        '260290': 'Cabo de Santo Agostinho', '260345': 'Camaragibe',
        '260680': 'Igarassu', '260720': 'Ipojuca', '260760': 'Itamaracá',
        '260775': 'Itapissuma', '260790': 'Jaboatão dos Guararapes',
        '260940': 'Moreno', '260960': 'Olinda', '261070': 'Paulista',
        '261160': 'Recife', '261370': 'São Lourenço da Mata'
    }

    # Filtrar PE
    df_pe = df[df['ocor_SIGLA_UF'] == 'PE']
    df_pe['CODMUNOCOR'] = df_pe['CODMUNOCOR'].astype(str).str[:6]

    # Filtrar RMR
    df_rmr = df_pe[df_pe['CODMUNOCOR'].isin(codigos_rmr_6digitos)].copy()
    df_rmr['NOME_MUNICIPIO'] = df_rmr['CODMUNOCOR'].map(nomes_municipios)

    # Aplicar correções
    df_rmr_corrigido = corrigir_df_rmr(df_rmr)
    df_rmr_corrigido['ocor_MUNNOME'] = df_rmr_corrigido['ocor_MUNNOME'].replace('Ilha de Itamaracá', 'Itamaracá')

    # Criar colunas de junção
    df_rmr_corrigido['MES_ANO'] = df_rmr_corrigido['DTOBITO'].dt.strftime('%m/%Y')
    df_rmr_corrigido['DIA'] = df_rmr_corrigido['DTOBITO'].dt.day

    return df_rmr_corrigido

def gerar_mapa_rmr_com_dados(data_analise: str) -> str:
    """Gera o mapa Folium da RMR com dados reais de mortalidade e chuva"""
    
    # Carregar e processar dados reais
    try:
        df_mortalidade = carregar_dados_mortalidade()
        df_chuva = processar_dados_chuva()
        
        if df_mortalidade.empty or df_chuva.empty:
            return gerar_mapa_rmr_simples(data_analise)
        
        df_processado = processar_dados_mortalidade(df_mortalidade)
        
        # Merge dos dados
        df_final = pd.merge(
            df_processado,
            df_chuva,
            left_on=['ocor_MUNNOME', 'MES_ANO', 'DIA'],
            right_on=['Posto', 'Mês/Ano', 'Dia'],
            how='left'
        )
        
        # Filtrar apenas causas W (relacionadas ao tempo/clima)
        df_final = df_final[df_final['CAUSABAS'].str.startswith(('W'), na=False)]
        
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return gerar_mapa_rmr_simples(data_analise)

    # Coordenadas das cidades da RMR
    coordenadas_rmr = {
        'Abreu e Lima': [-7.915, -34.908],
        'Araçoiaba': [-7.876, -35.039],
        'Cabo de Santo Agostinho': [-8.293, -35.035],
        'Camaragibe': [-8.031, -34.992],
        'Igarassu': [-7.834, -34.918],
        'Ipojuca': [-8.397, -35.061],
        'Itamaracá': [-7.755, -34.821],
        'Itapissuma': [-7.747, -34.912],
        'Jaboatão dos Guararapes': [-8.106, -35.006],
        'Moreno': [-8.140, -35.093],
        'Olinda': [-8.010, -34.855],
        'Paulista': [-7.947, -34.887],
        'Recife': [-8.058, -34.884],
        'São Lourenço da Mata': [-8.005, -35.048]
    }

    # Definir centro da RMR
    center_lat = -8.058  # Recife como centro
    center_lon = -34.884

    # Criar mapa
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=10,
        tiles='OpenStreetMap'
    )

    # Adicionar shapefiles se disponíveis
    try:
        import geopandas as gpd
        from folium import GeoJson
        
        shp_dir = "./data/SHP-RMR"
        if os.path.exists(shp_dir):
            colors = ['red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'black', 'cadetblue', 'darkred']
            for idx, file in enumerate(os.listdir(shp_dir)):
                if file.endswith('.shp'):
                    shp_path = os.path.join(shp_dir, file)
                    try:
                        gdf = gpd.read_file(shp_path)
                        color = colors[idx % len(colors)]
                        GeoJson(
                            gdf,
                            name=os.path.splitext(file)[0],
                            style_function=lambda feature, color=color: {
                                'color': color,
                                'weight': 2,
                                'fillOpacity': 0.3
                            }
                        ).add_to(m)
                    except Exception as e:
                        print(f"Erro ao carregar shapefile {file}: {e}")
                        continue
    except ImportError:
        print("Geopandas não disponível - shapefiles não serão carregados")
    except Exception as e:
        print(f"Erro ao carregar shapefiles: {e}")

    # Adicionar marcadores com dados reais
    morte_chuva_layer = folium.FeatureGroup(name='Morte e Chuva').add_to(m)
    
    for cidade, coords in coordenadas_rmr.items():
        # Gerar informações usando dados reais
        info_popup, coordenadas = gerar_info_mapa_mortalidade_corrigida(data_analise, cidade, df_final)
        
        if coordenadas:
            folium.Marker(
                location=coordenadas,
                popup=folium.Popup(info_popup, max_width=300),
                icon=folium.Icon(color='darkblue', icon='cloud-showers-heavy', prefix='fa'),
                tooltip=f"{cidade} - {data_analise}"
            ).add_to(morte_chuva_layer)

    # Adicionar controle de camadas
    folium.LayerControl().add_to(m)
    
    return m._repr_html_()

def gerar_info_mapa_mortalidade_corrigida(data_input: str, cidade: str, df_completo: pd.DataFrame):
    """Versão corrigida da função que gera informações para popup do mapa"""
    
    coordenadas_rmr = {
        'Abreu e Lima': [-7.915, -34.908],
        'Araçoiaba': [-7.876, -35.039],
        'Cabo de Santo Agostinho': [-8.293, -35.035],
        'Camaragibe': [-8.031, -34.992],
        'Igarassu': [-7.834, -34.918],
        'Ipojuca': [-8.397, -35.061],
        'Itamaracá': [-7.755, -34.821],
        'Itapissuma': [-7.747, -34.912],
        'Jaboatão dos Guararapes': [-8.106, -35.006],
        'Moreno': [-8.140, -35.093],
        'Olinda': [-8.010, -34.855],
        'Paulista': [-7.947, -34.887],
        'Recife': [-8.058, -34.884],
        'São Lourenço da Mata': [-8.005, -35.048]
    }

    cidade = cidade.strip().title()
    try:
        data = pd.to_datetime(data_input)
        data_obj = data.date()
    except ValueError:
        return (f"Data inválida: '{data_input}'. Use o formato 'YYYY-MM-DD'.", None)

    coordenada = coordenadas_rmr.get(cidade, None)
    if coordenada is None:
        return (f"Cidade '{cidade}' não encontrada na RMR.", None)

    if df_completo.empty:
        info_string = (
            f"<b>{cidade}</b><br>"
            f"Data: {data.strftime('%d/%m/%Y')}<br>"
            f"Óbitos: 0 pessoas<br>"
            f"Chuva: 0.00 mm<br>"
            f"<small>Dados não disponíveis</small>"
        )
        return (info_string, coordenada)

    # Filtrar dados para a cidade e data específicas
    # Verificar diferentes variações do nome da cidade
    cidade_variants = [cidade, cidade.upper(), cidade.lower()]
    
    df_filtrado = df_completo[
        (df_completo['ocor_MUNNOME'].str.title().isin(cidade_variants) | 
         df_completo['ocor_MUNNOME'].isin(cidade_variants)) &
        (pd.to_datetime(df_completo['DTOBITO']).dt.date == data_obj)
    ]
    
    # Se não encontrar dados exatos, buscar dados próximos (mesmo mês)
    if df_filtrado.empty:
        mes_ano = data.strftime('%m/%Y')
        df_filtrado_mes = df_completo[
            (df_completo['ocor_MUNNOME'].str.title().isin(cidade_variants) | 
             df_completo['ocor_MUNNOME'].isin(cidade_variants)) &
            (df_completo['MES_ANO'] == mes_ano)
        ]
        
        total_obitos = len(df_filtrado_mes)
        chuva_mm = df_filtrado_mes['Chuva_mm'].mean() if not df_filtrado_mes.empty else 0
        nota_adicional = f"<br><small>Dados do mês {mes_ano}</small>"
    else:
        total_obitos = len(df_filtrado)
        chuva_mm = df_filtrado['Chuva_mm'].mean()
        nota_adicional = ""
    
    # Corrigir valores nulos
    chuva_mm = 0 if pd.isna(chuva_mm) else chuva_mm

    info_string = (
        f"<b>{cidade}</b><br>"
        f"Data: {data.strftime('%d/%m/%Y')}<br>"
        f"Óbitos: {total_obitos} pessoas<br>"
        f"Chuva: {chuva_mm:.2f} mm{nota_adicional}"
    )

    return (info_string, coordenada)

# Versão simplificada sem geopandas (fallback)
def gerar_mapa_rmr_simples(data_analise: str) -> str:
    """Gera o mapa Folium da RMR com dados de mortalidade e chuva (versão simplificada)"""
    
    # Coordenadas das cidades da RMR
    coordenadas_rmr = {
        'Abreu e Lima': [-7.915, -34.908],
        'Araçoiaba': [-7.876, -35.039],
        'Cabo de Santo Agostinho': [-8.293, -35.035],
        'Camaragibe': [-8.031, -34.992],
        'Igarassu': [-7.834, -34.918],
        'Ipojuca': [-8.397, -35.061],
        'Itamaracá': [-7.755, -34.821],
        'Itapissuma': [-7.747, -34.912],
        'Jaboatão dos Guararapes': [-8.106, -35.006],
        'Moreno': [-8.140, -35.093],
        'Olinda': [-8.010, -34.855],
        'Paulista': [-7.947, -34.887],
        'Recife': [-8.058, -34.884],
        'São Lourenço da Mata': [-8.005, -35.048]
    }

    # Definir centro da RMR
    center_lat = -8.058  # Recife como centro
    center_lon = -34.884

    # Criar mapa
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=10,
        tiles='OpenStreetMap'
    )

    # Adicionar marcadores para cada cidade
    for cidade, coords in coordenadas_rmr.items():
        # Dados simulados para demonstração
        total_obitos = 0  # Seria calculado dos dados reais
        chuva_mm = 0.0   # Seria calculado dos dados reais
        
        info_popup = (
            f"<b>{cidade}</b><br>"
            f"Data: {pd.to_datetime(data_analise).strftime('%d/%m/%Y')}<br>"
            f"Óbitos: {total_obitos} pessoas<br>"
            f"Chuva: {chuva_mm:.2f} mm<br>"
            f"<small>Dados em processamento...</small>"
        )
        
        folium.Marker(
            location=coords,
            popup=folium.Popup(info_popup, max_width=300),
            icon=folium.Icon(color='darkblue', icon='cloud-showers-heavy', prefix='fa'),
            tooltip=f"{cidade} - {data_analise}"
        ).add_to(m)

    return m._repr_html_()
