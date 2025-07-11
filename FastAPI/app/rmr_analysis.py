import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from typing import Dict, Any, Optional
import base64
from io import BytesIO

# Configuração global de estilo
plt.style.use('dark_background')
sns.set_palette("Set2")

# Cores personalizadas para corresponder ao tema da aplicação
APP_COLORS = {
    'background': '#1A2B3C',  # darkNavy
    'card_bg': '#2C4055',     # mediumNavy
    'accent': '#E0A800',      # burntYellow
    'accent_light': '#F2C45E', # lightBurntYellow
    'text': '#F0F0F0',        # offWhite
    'text_secondary': '#A0A0A0', # lightGrey
    'border': '#3D546B'       # lightNavy
}


class RMRAnalyzer:
    """Classe para análise de dados RMR baseada no notebook"""
    
    def __init__(self):
        self.df_mortalidade = None
        self.df_chuva = None
        self.df_final = None
        self.cid_w_mapping = self._create_cid_w_mapping()
        self._load_data()
    
    def _create_cid_w_mapping(self):
        """Cria mapeamento dos códigos CID-W para suas descrições"""
        cid_w_list = [
            "W00 - Queda no mesmo nível por escorregão, tropeção ou cambalhota",
            "W01 - Queda no mesmo nível por tropeção ou escorregão com colisão",
            "W02 - Queda envolvendo patins, esqui, patinete ou pranchas",
            "W03 - Queda em cadeira de rodas",
            "W04 - Queda ao ser carregado ou apoiado por outra pessoa",
            "W05 - Queda que envolve cama",
            "W06 - Queda que envolve sofá",
            "W07 - Queda que envolve cadeira",
            "W08 - Queda que envolve outros móveis",
            "W09 - Queda em ou de equipamento de recreação",
            "W10 - Queda em ou de escadas ou degraus",
            "W11 - Queda em ou de escada",
            "W12 - Queda em ou de andaime",
            "W13 - Queda de, ou através de edifício",
            "W14 - Queda de árvore",
            "W15 - Queda de penhasco",
            "W16 - Mergulho ou salto na água causando outro ferimento que não afogamento ou submersão",
            "W17 - Outra queda de um mesmo nível a outro",
            "W18 - Outra queda no mesmo nível",
            "W19 - Queda, não especificada",
            "W20 - Atingido por objeto lançado, projetado ou em queda",
            "W21 - Atingido por equipamento esportivo",
            "W22 - Atingido por outro objeto",
            "W23 - Ficando preso, esmagado ou apertado entre objetos",
            "W24 - Contato com dispositivos de elevação e transmissão, não classificados em outra parte",
            "W25 - Contato com vidro cortante",
            "W26 - Contato com faca, espada e punhal",
            "W27 - Contato com ferramenta manual cortante ou perfurante",
            "W28 - Contato com ferramenta ou objeto doméstico",
            "W29 - Contato com outro objeto cortante ou perfurante",
            "W30 - Contato com outro equipamento agrícola",
            "W31 - Contato com outra máquina e com máquina não especificada",
            "W32 - Disparo de arma curta",
            "W33 - Disparo de espingarda, fuzil e arma de fogo de maior calibre",
            "W34 - Descarga de outra arma de fogo",
            "W35 - Explosão ou ruptura de caldeira",
            "W36 - Explosão ou ruptura de cilindro de gás",
            "W37 - Explosão ou ruptura de outra substância pressurizada",
            "W38 - Explosão de fogos de artifício",
            "W39 - Explosão de outra substância",
            "W40 - Exposição à pressão de ondas",
            "W41 - Exposição a vibração",
            "W42 - Exposição a ruído",
            "W43 - Exposição à radiação",
            "W44 - Penetração de corpo estranho através de orifício natural",
            "W45 - Penetração de corpo estranho na pele",
            "W46 - Contato com agulha hipodérmica contaminada",
            "W49 - Exposição a outros fatores e aos não especificados",
            "W50 - Agressão por golpe, batida ou pancada por outra pessoa",
            "W51 - Agressão por empurrão por outra pessoa",
            "W52 - Agressão por compressão por multidão ou aglomeração humana",
            "W53 - Mordedura ou pancada provocada por rato",
            "W54 - Mordedura ou pancada provocada por cão",
            "W55 - Mordedura ou pancada provocada por outros mamíferos",
            "W56 - Contato com animais marinhos",
            "W57 - Mordedura ou picada por inseto e outros artrópodes não venenosos",
            "W58 - Mordedura por crocodilo ou aligátor",
            "W59 - Mordedura ou pancada por outros répteis",
            "W60 - Contato com espinhos, farpas ou plantas espinhosas",
            "W64 - Outros traumatismos acidentais especificados",
            "W65 - Afogamento e submersão enquanto na banheira",
            "W66 - Afogamento e submersão após queda na banheira",
            "W67 - Afogamento e submersão enquanto na piscina",
            "W68 - Afogamento e submersão após queda em piscina",
            "W69 - Afogamento e submersão enquanto em águas naturais",
            "W70 - Afogamento e submersão após queda em águas naturais",
            "W73 - Outros afogamentos e submersões especificados",
            "W74 - Afogamento e submersão não especificados",
            "W75 - Estrangulamento e sufocação acidental na cama",
            "W76 - Outros estrangulamentos e sufocações acidentais",
            "W77 - Envolvimento ou engolfamento em avalanche, deslizamento ou outro movimento de massa",
            "W78 - Inalação de alimentos causando obstrução",
            "W79 - Inalação de outros objetos causando obstrução",
            "W80 - Aspiração de vômito",
            "W81 - Aspiração de conteúdo gástrico",
            "W83 - Outros acidentes especificados que causam privação de respiração",
            "W84 - Acidente não especificado causando privação de respiração",
            "W85 - Exposição a linha de força elétrica transmitida ao ar livre",
            "W86 - Exposição a outra corrente elétrica especificada",
            "W87 - Exposição a corrente elétrica, não especificada",
            "W88 - Exposição à radiação ionizante",
            "W89 - Exposição à luz e radiação ultravioleta artificiais",
            "W90 - Exposição a outras radiações não ionizantes especificadas",
            "W91 - Exposição a radiações não ionizantes, não especificada",
            "W92 - Exposição a calor de equipamento doméstico",
            "W93 - Exposição a calor de outros equipamentos",
            "W94 - Exposição a calor e luz de origem natural",
            "W99 - Exposição a outras forças de origem não especificada"
        ]
        
        # Criar dicionário mapeando código para descrição
        mapping = {}
        for item in cid_w_list:
            codigo = item.split(' - ')[0]  # Extrai o código (ex: W00)
            mapping[codigo] = item
        
        return mapping

    def _load_data(self):
        """Carrega e processa os dados"""
        try:
            # Carregar dados de mortalidade
            self.df_mortalidade = self._carregar_dados_mortalidade()
            
            # Carregar dados de chuva
            self.df_chuva = self._processar_dados_chuva()
            
            # Processar e fazer merge
            if self.df_mortalidade is not None and self.df_chuva is not None:
                df_processado = self._processar_dados_mortalidade(self.df_mortalidade)
                
                if df_processado is not None:
                    self.df_final = pd.merge(
                        df_processado,
                        self.df_chuva,
                        left_on=['ocor_MUNNOME', 'MES_ANO', 'DIA'],
                        right_on=['Posto', 'Mês/Ano', 'Dia'],
                        how='left'
                    )
                    
                    # Filtrar apenas causas CID-W (causas externas)
                    print(f"Registros antes do filtro CID-W: {len(self.df_final):,}")
                    self.df_final = self.df_final[self.df_final['CAUSABAS'].str.startswith(('W'), na=False)]
                    print(f"Registros após filtro CID-W: {len(self.df_final):,}")
                    
                    # Adicionar coluna data_obito para compatibilidade
                    self.df_final['data_obito'] = self.df_final['DTOBITO']
                    
                    print(f"✅ Dados carregados e filtrados: {len(self.df_final):,} registros CID-W")
                else:
                    print("❌ Falha no processamento dos dados de mortalidade")
            else:
                print("❌ Falha no carregamento dos dados")
                
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
    
    def _carregar_dados_mortalidade(self):
        """Carrega dados de mortalidade"""
        dfs = []
        for ano in range(2018, 2024):
            try:
                caminho = f'./data/MortalidadeBrasil/ETLSIM.DORES_PE_{ano}_t.csv'
                df = pd.read_csv(caminho, encoding='latin-1', sep=',', dtype={'CODMUNRES': str})
                dfs.append(df)
            except FileNotFoundError:
                print(f"⚠️ Arquivo não encontrado: {caminho}")
            except Exception as e:
                print(f"❌ Erro ao carregar {ano}: {e}")
        
        if not dfs:
            return None
            
        return pd.concat(dfs)
    
    def _processar_dados_chuva(self):
        """Processa dados de chuva"""
        try:
            # Carregar dados brutos
            df1 = pd.read_csv('./data/Chuvas/Chuvas18-21.csv', sep=',', decimal=',', encoding='utf-8', dtype=str)
            df2 = pd.read_csv('./data/Chuvas/Chuvas21-25.csv', sep=',', decimal=',', encoding='utf-8', dtype=str)
            
            # Unificação
            df_chuva = pd.concat([df1, df2], ignore_index=True)
            
            # Padronização temporal
            meses = {
                'jan./': '01/', 'fev./': '02/', 'mar./': '03/', 'abr./': '04/',
                'mai./': '05/', 'jun./': '06/', 'jul./': '07/', 'ago./': '08/',
                'set./': '09/', 'out./': '10/', 'nov./': '11/', 'dez./': '12/'
            }
            
            for old, new in meses.items():
                df_chuva['Mês/Ano'] = df_chuva['Mês/Ano'].str.replace(old, new)
            
            # Normalização de cidades
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
            
            # Consistência
            df_chuva = df_chuva.groupby(['Mês/Ano', 'Posto']).first().reset_index()
            
            # Formato long
            df_chuva_reform = df_chuva.melt(
                id_vars=['Posto', 'Mês/Ano'],
                value_vars=[str(i) for i in range(1, 32)],
                var_name='Dia',
                value_name='Chuva_mm'
            )
            
            df_chuva_reform['Dia'] = df_chuva_reform['Dia'].astype(int)
            
            return df_chuva_reform
            
        except Exception as e:
            print(f"❌ Erro ao processar dados de chuva: {e}")
            return None
    
    def _processar_dados_mortalidade(self, df):
        """Processa dados de mortalidade para RMR"""
        if df is None:
            return None
        
        # Códigos RMR
        codigos_rmr_6digitos = [
            '261160', '260790', '260960', '261070', '260290', '260345',
            '261370', '260680', '260005', '260720', '260940', '260105',
            '260775', '260760'
        ]
        
        nomes_municipios = {
            '260005': 'Abreu e Lima', '260105': 'Olinda', '260290': 'Cabo de Santo Agostinho', '260345': 'Camaragibe',
            '260680': 'Igarassu', '260720': 'Ipojuca', '260760': 'Itamaracá',
            '260775': 'Itapissuma', '260790': 'Jaboatão dos Guararapes',
            '260940': 'Moreno', '260960': 'Recife', '261070': 'Paulista',
            '261160': 'São Lourenço da Mata', '261370': 'São Lourenço da Mata'
        }
        
        # Filtrar PE
        df_pe = df[df['ocor_SIGLA_UF'] == 'PE']
        
        # Filtrar RMR
        df_pe['CODMUNOCOR'] = df_pe['CODMUNOCOR'].astype(str).str[:6]
        df_rmr = df_pe[df_pe['CODMUNOCOR'].isin(codigos_rmr_6digitos)].copy()
        
        if df_rmr.empty:
            return None
        
        # Adicionar nomes
        df_rmr['NOME_MUNICIPIO'] = df_rmr['CODMUNOCOR'].map(nomes_municipios)
        
        # Corrigir dados
        df_rmr = self._corrigir_df_rmr(df_rmr)
        
        # Criar colunas de junção
        df_rmr['MES_ANO'] = df_rmr['DTOBITO'].dt.strftime('%m/%Y')
        df_rmr['DIA'] = df_rmr['DTOBITO'].dt.day
        
        return df_rmr
    
    def _corrigir_df_rmr(self, df):
        """Corrige encoding e converte dados"""
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
        
        # Mapear sexo
        df['SEXO'] = df['SEXO'].map({1: 'Masculino', 2: 'Feminino', 0: 'Ignorado'})
        
        # Corrigir nomes específicos
        df['ocor_MUNNOME'] = df['ocor_MUNNOME'].replace('Ilha de Itamaracá', 'Itamaracá')
        
        return df
    
    def comparar_rmr_dia(self, data_input: str, cidade: str, top_n: int = 10) -> Dict[str, Any]:
        """
        Versão da função do notebook que retorna dados JSON em vez de plotar
        """
        rmr_cidades = [
            'Recife', 'Igarassu', 'Camaragibe', 'Araçoiaba', 'Cabo de Santo Agostinho',
            'São Lourenço da Mata', 'Itamaracá', 'Jaboatão dos Guararapes', 'Paulista',
            'Ipojuca', 'Moreno', 'Olinda', 'Abreu e Lima', 'Itapissuma'
        ]
        
        if self.df_final is None:
            return {"error": "Dados não carregados"}
        
        try:
            data = pd.to_datetime(data_input).date()
        except:
            return {"error": "Data inválida. Use o formato 'YYYY-MM-DD'."}
        
        # Filtrar dados
        df_rmr_dia = self.df_final[
            (self.df_final['ocor_MUNNOME'].isin(rmr_cidades)) &
            (self.df_final['DTOBITO'].dt.date == data)
        ]
        
        if df_rmr_dia.empty:
            return {"error": f"Nenhum dado encontrado para a RMR em {data}."}
        
        dados_cidade = df_rmr_dia[df_rmr_dia['ocor_MUNNOME'].str.upper() == cidade.upper()]
        
        if dados_cidade.empty:
            return {"error": f"Nenhum dado encontrado para {cidade.title()} em {data}."}
        
        # Preparar dados
        causas = dados_cidade['CAUSABAS'].value_counts().head(top_n)
        
        # Encontrar causas únicas nos dados e mapear suas descrições
        causas_encontradas = dados_cidade['CAUSABAS'].unique()
        descrições_causas = []
        
        for causa in causas_encontradas:
            codigo_cid = causa[:3]  # Primeiros 3 dígitos
            if codigo_cid in self.cid_w_mapping:
                descrições_causas.append(self.cid_w_mapping[codigo_cid])
            else:
                descrições_causas.append(f"{codigo_cid} - Descrição não encontrada")
        
        # Remover duplicatas e ordenar
        descrições_causas = sorted(list(set(descrições_causas)))
        agrupado = df_rmr_dia.groupby('ocor_MUNNOME').agg({
            'DTOBITO': 'count',
            'Chuva_mm': 'mean'
        }).rename(columns={'DTOBITO': 'Total_Obitos', 'Chuva_mm': 'Media_Chuva_mm'}).fillna(0)
        
        # Gerar gráfico
        try:
            # Configurar matplotlib para não usar GUI
            plt.switch_backend('Agg')
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))
            
            # Pizza - Causas
            if not causas.empty:
                ax1.pie(causas, labels=causas.index, autopct='%1.1f%%', startangle=140,
                        colors=sns.color_palette('Reds', n_colors=len(causas)))
                ax1.set_title(f'{cidade.title()} - {data}\\nTop {top_n} Causas de Óbito CID-W')
            else:
                ax1.text(0.5, 0.5, 'Sem dados\\npara esta cidade', ha='center', va='center', transform=ax1.transAxes)
                ax1.set_title(f'{cidade.title()} - {data}\\nSem dados CID-W')
            
            # Barras + linha - Comparativo RMR
            if not agrupado.empty:
                cores = ['darkblue' if cidade.lower() == mun.lower() else 'red' for mun in agrupado.index]
                
                # Fix seaborn warning by setting hue explicitly
                sns.barplot(x=agrupado.index, y=agrupado['Total_Obitos'], 
                           hue=agrupado.index, palette=cores, ax=ax2, legend=False)
                ax2.set_ylabel('Total de Óbitos CID-W', color='black')
                ax2.set_xlabel('')
                ax2.set_xticklabels(agrupado.index, rotation=45, ha='right')
                
                ax3 = ax2.twinx()
                sns.lineplot(x=range(len(agrupado)), y=agrupado['Media_Chuva_mm'], 
                            color='blue', marker='o', label='Chuva Média (mm)', ax=ax3)
                ax3.set_ylabel('Média de Chuva (mm)', color='blue')
                ax3.tick_params(axis='y', labelcolor='blue')
                
                ax2.set_title(f'Óbitos CID-W vs Chuva na RMR - {data}')
            
            plt.tight_layout()
            
            # Converter para base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            # Retornar dados
            return {
                "success": True,
                "data": {
                    "date": str(data),
                    "city": cidade.title(),
                    "total_deaths": len(dados_cidade),
                    "average_rain": float(dados_cidade['Chuva_mm'].mean()) if not dados_cidade['Chuva_mm'].isna().all() else 0,
                    "causes": causas.to_dict() if not causas.empty else {},
                    "cause_descriptions": descrições_causas,
                    "rmr_comparison": agrupado.to_dict('index') if not agrupado.empty else {},
                    "chart_image": f"data:image/png;base64,{image_base64}"
                }
            }
            
        except Exception as e:
            return {"error": f"Erro ao gerar gráfico: {str(e)}"}

# Instância global
rmr_analyzer = RMRAnalyzer()


def comparar_rmr_dia_api(data_input, cidade, top_n=10):
    """Versão da função comparar_rmr_dia adaptada para API"""
    
    rmr_cidades = [
        'Recife', 'Igarassu', 'Camaragibe', 'Araçoiaba', 'Cabo de Santo Agostinho',
        'São Lourenço da Mata', 'Itamaracá', 'Jaboatão dos Guararapes', 'Paulista',
        'Ipojuca', 'Moreno', 'Olinda', 'Abreu e Lima', 'Itapissuma'
    ]

    # Usar dados já carregados na instância global
    df = rmr_analyzer.df_final.copy()
    
    # Filtrar apenas causas W (infecciosas/acidentes)
    df = df[df['CAUSABAS'].str.startswith(('W'), na=False)]
    
    try:
        data = pd.to_datetime(data_input).date()
    except:
        raise ValueError("Data inválida. Use o formato 'YYYY-MM-DD'.")

    # Filtrar dados por data e RMR
    df_rmr_dia = df[
        (df['ocor_MUNNOME'].isin(rmr_cidades)) &
        (pd.to_datetime(df['DTOBITO']).dt.date == data)
    ]

    if df_rmr_dia.empty:
        # Se não há dados, criar um gráfico vazio informativo
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        fig.patch.set_facecolor(APP_COLORS['background'])
        ax.set_facecolor(APP_COLORS['card_bg'])
        
        ax.text(0.5, 0.5, f'Nenhum dado encontrado para a RMR em {data}', 
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=18, color=APP_COLORS['text_secondary'],
                bbox=dict(boxstyle="round,pad=0.3", facecolor=APP_COLORS['card_bg'], 
                         edgecolor=APP_COLORS['border'], alpha=0.8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        plt.title(f'Dados não disponíveis para {data}', fontsize=20, 
                 color=APP_COLORS['accent'], fontweight='bold', pad=20)
        return fig

    # Filtrar dados da cidade específica
    dados_cidade = df_rmr_dia[df_rmr_dia['ocor_MUNNOME'].str.upper() == cidade.upper()]

    # Preparar dados para visualização
    agrupado = df_rmr_dia.groupby('ocor_MUNNOME').agg({
        'DTOBITO': 'count',
        'Chuva_mm': 'mean'
    }).rename(columns={'DTOBITO': 'Total_Obitos', 'Chuva_mm': 'Media_Chuva_mm'}).fillna(0)

    rmr_existentes = [c for c in rmr_cidades if c in agrupado.index]
    if rmr_existentes:
        agrupado = agrupado.loc[rmr_existentes]
    
    cores = ['red' if cidade.lower() != mun.lower() else 'darkblue' for mun in agrupado.index]

    # Criar gráfico
    if not dados_cidade.empty and len(dados_cidade['CAUSABAS'].value_counts()) > 0:
        # Dois gráficos lado a lado se há dados da cidade
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        fig.patch.set_facecolor(APP_COLORS['background'])
        
        # Pizza das causas
        causas = dados_cidade['CAUSABAS'].value_counts().head(top_n)
        colors_pie = sns.color_palette("Set2", n_colors=len(causas))
        ax1.pie(causas, labels=causas.index, autopct='%1.1f%%', startangle=140,
                colors=colors_pie, textprops={'color': APP_COLORS['text'], 'fontsize': 10})
        ax1.set_title(f'{cidade.title()} - {data}\nTop {min(top_n, len(causas))} Causas de Óbito (CAUSABAS)',
                     color=APP_COLORS['accent'], fontsize=14, fontweight='bold', pad=20)
        ax1.set_facecolor(APP_COLORS['card_bg'])
        
    else:
        # Apenas gráfico de barras se não há dados da cidade
        fig, ax2 = plt.subplots(1, 1, figsize=(14, 8))
        fig.patch.set_facecolor(APP_COLORS['background'])

    # Gráfico de barras + linha
    if not agrupado.empty:
        # Criar cores personalizadas para as barras
        cores_custom = [APP_COLORS['accent'] if cidade.lower() == mun.lower() else APP_COLORS['border'] for mun in agrupado.index]
        
        bars = ax2.bar(agrupado.index, agrupado['Total_Obitos'], color=cores_custom, alpha=0.8, edgecolor=APP_COLORS['text'], linewidth=0.5)
        ax2.set_ylabel('Total de Óbitos', color=APP_COLORS['text'], fontsize=12, fontweight='bold')
        ax2.set_xlabel('')
        ax2.set_xticklabels(agrupado.index, rotation=45, ha='right', color=APP_COLORS['text'], fontsize=10)
        ax2.tick_params(colors=APP_COLORS['text'])
        ax2.set_facecolor(APP_COLORS['card_bg'])
        
        # Destacar a cidade selecionada
        for i, bar in enumerate(bars):
            if agrupado.index[i].lower() == cidade.lower():
                bar.set_color(APP_COLORS['accent'])
                bar.set_alpha(1.0)

        # Linha de chuva
        ax3 = ax2.twinx()
        line = ax3.plot(agrupado.index, agrupado['Media_Chuva_mm'], 
                       color=APP_COLORS['accent_light'], marker='o', linewidth=3, 
                       markersize=8, label='Chuva Média (mm)', alpha=0.9)
        ax3.set_ylabel('Média de Chuva (mm)', color=APP_COLORS['accent_light'], fontsize=12, fontweight='bold')
        ax3.tick_params(axis='y', labelcolor=APP_COLORS['accent_light'], colors=APP_COLORS['accent_light'])
        ax3.tick_params(axis='x', colors=APP_COLORS['text'])
        
        # Grid sutil
        ax2.grid(True, alpha=0.3, color=APP_COLORS['text'])
        ax3.grid(False)
        
    else:
        ax2.text(0.5, 0.5, 'Nenhum dado disponível para visualização', 
                horizontalalignment='center', verticalalignment='center',
                transform=ax2.transAxes, fontsize=16, color=APP_COLORS['text_secondary'])
        ax2.set_facecolor(APP_COLORS['card_bg'])

    ax2.set_title(f'Comparativo por Cidade na RMR - {data}', 
                 color=APP_COLORS['accent'], fontsize=16, fontweight='bold', pad=20)

    # Ajustar layout e cores gerais
    plt.tight_layout()
    
    # Aplicar estilo geral da figura
    for ax in fig.get_axes():
        ax.spines['bottom'].set_color(APP_COLORS['border'])
        ax.spines['top'].set_color(APP_COLORS['border'])
        ax.spines['right'].set_color(APP_COLORS['border'])
        ax.spines['left'].set_color(APP_COLORS['border'])
        
    return fig
