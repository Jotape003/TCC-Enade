import pandas as pd
import os
import glob
import json
from collections import defaultdict
from utils import safe_numeric_convert

from config import PROCESSED_DATA_PATH, YEARS_TO_PROCESS, FINAL_VG_JSON_PATH, CURSO_MAP, FINAL_MEDIA_JSON_PATH

MEDIAS_AGREGADAS_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Visao_Geral', 'medias_agregadas_geral.json')
CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv')

BASE_OUTPUT_PATH = os.path.join(FINAL_VG_JSON_PATH)

def load_single_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Erro ao carregar {file_path}: {e}")
        return None

def load_course_metadata():
    try:
        df_cursos = pd.read_csv(CURSOS_CSV_PATH, sep=';', usecols=['Código', 'CO_GRUPO'])
        df_cursos.columns = ['CO_CURSO', 'CO_GRUPO']
        df_cursos = df_cursos.dropna(subset=['CO_CURSO', 'CO_GRUPO'])
        df_cursos['CO_CURSO'] = pd.to_numeric(df_cursos['CO_CURSO'], errors='coerce').astype('Int64')
        df_cursos['CO_GRUPO'] = pd.to_numeric(df_cursos['CO_GRUPO'], errors='coerce').astype('Int64')
        df_cursos = df_cursos.drop_duplicates(subset=['CO_CURSO'], keep='first')
        
        mapa = pd.Series(df_cursos.CO_GRUPO.astype(str).values, index=df_cursos.CO_CURSO).to_dict()
        return mapa
    except Exception as e:
         print(f"Erro ao ler metadados dos cursos: {e}")
         return {}

def process_year_data(campus_path, campus_name, year, medias_agregadas_map, curso_grupo_map):
    print(f"  -> Processando ano {year}...")
    
    notas_file_path = glob.glob(os.path.join(campus_path, '*arq3.csv'))
    if not notas_file_path:
        print(f"     Aviso: arq3.csv não encontrado em {campus_path}.")
        return None

    try:
        df_notas = pd.read_csv(notas_file_path[0], sep=';', encoding='utf-8', low_memory=False)
        df_notas.columns = [col.upper() for col in df_notas.columns]

        colunas_notas = ['NT_GER', 'NT_FG', 'NT_CE']
        for col in colunas_notas:
             df_notas[col] = safe_numeric_convert(df_notas[col])

        analise = df_notas.groupby('CO_CURSO').agg(
            nota_geral=('NT_GER', 'mean'),
            nota_fg=('NT_FG', 'mean'),
            nota_ce=('NT_CE', 'mean'),
            numero_participantes=('CO_CURSO', 'size')
        ).reset_index()

        analise['CO_CURSO'] = pd.to_numeric(analise['CO_CURSO'], errors='coerce').astype('Int64')
        analise.dropna(subset=['CO_CURSO'], inplace=True)

        # Enriquecimento com Metadados
        analise['NO_CURSO'] = analise['CO_CURSO'].map(CURSO_MAP).fillna('Nome Desconhecido')
        analise['CAMPUS'] = campus_name
        analise['CO_GRUPO'] = analise['CO_CURSO'].map(curso_grupo_map)
        analise = analise.dropna(subset=['CO_GRUPO'])

        # Enriquecimento com Médias Agregadas (UFC, Região, Brasil)
        medias_ano_agregadas = medias_agregadas_map.get(str(year), {})
        
        def get_all_averages(row):
            grupo = row['CO_GRUPO']
            if pd.isna(grupo): return pd.Series([None]*12)
            
            grupo_str = str(grupo) # O mapa de médias usa string nas chaves
            medias = medias_ano_agregadas.get(grupo_str, {})
            
            # Mapeia as chaves do JSON de médias para as colunas do DataFrame
            return pd.Series([
                medias.get('media_ufc_ger'), medias.get('media_ufc_fg'), medias.get('media_ufc_ce'),
                medias.get('media_uf_ger'), medias.get('media_uf_fg'), medias.get('media_uf_ce'),
                medias.get('media_regiao_ger'), medias.get('media_regiao_fg'), medias.get('media_regiao_ce'),
                medias.get('media_nacional_ger'), medias.get('media_nacional_fg'), medias.get('media_nacional_ce'),
            ])

        new_cols = [
            'media_ufc_geral', 'media_ufc_fg', 'media_ufc_ce',
            'media_uf_geral', 'media_uf_fg', 'media_uf_ce',
            'media_regiao_geral', 'media_regiao_fg', 'media_regiao_ce',
            'media_nacional_geral', 'media_nacional_fg', 'media_nacional_ce'
        ]
        
        analise[new_cols] = analise.apply(get_all_averages, axis=1)
        analise = analise.where(pd.notna(analise), None)
        
        return analise.round(2)

    except Exception as e:
        print(f"     ERRO ao processar DataFrame {campus_name}/{year}: {e}")
        return None

def main():
    print("--- INICIANDO CONSOLIDAÇÃO DE VISÃO GERAL ---")
    
    # Carrega metadados globais
    curso_grupo_map = load_course_metadata()
    medias_agregadas_map = load_single_json(MEDIAS_AGREGADAS_PATH)

    if not medias_agregadas_map or not curso_grupo_map:
        print("Encerrando: Faltando arquivos de médias agregadas ou metadados de cursos.")
        return

    # Garante que a pasta de saída existe
    os.makedirs(BASE_OUTPUT_PATH, exist_ok=True)
    
    # Identifica pastas de Campus
    campus_folders = [d for d in os.listdir(PROCESSED_DATA_PATH) if os.path.isdir(os.path.join(PROCESSED_DATA_PATH, d))]

    for campus_name in campus_folders:
        print(f"\nIniciando Campus: {campus_name}")
        
        # Estrutura Consolidada: { "CO_CURSO": { "2014": {...}, "2017": {...} } }
        campus_consolidated = defaultdict(dict)
        
        for year in YEARS_TO_PROCESS:
            campus_year_path = os.path.join(PROCESSED_DATA_PATH, campus_name, str(year))
            
            if os.path.exists(campus_year_path):
                # Processa os dados deste ano
                df_year = process_year_data(campus_year_path, campus_name, str(year), medias_agregadas_map, curso_grupo_map)
                
                if df_year is not None and not df_year.empty:
                    # Converte para lista de dicionários
                    records = df_year.to_dict(orient='records')
                    
                    # Acumula na estrutura consolidada
                    for row in records:
                        co_curso = str(row['CO_CURSO'])
                        # Remove chaves internas que não precisam ser salvas se quiser limpar, 
                        # mas manter tudo também não tem problema.
                        campus_consolidated[co_curso][str(year)] = row

        # Salva o arquivo consolidado do Campus se houver dados
        if campus_consolidated:
            output_dir = os.path.join(BASE_OUTPUT_PATH, campus_name)
            os.makedirs(output_dir, exist_ok=True)
            
            output_path = os.path.join(output_dir, 'visao_geral_consolidado.json')
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(campus_consolidated, f, indent=4, ensure_ascii=False)
            
            print(f"Sucesso! Arquivo consolidado salvo em: {output_path}")
        else:
            print(f"Aviso: Nenhum dado processado para {campus_name}.")

if __name__ == '__main__':
    main()