import pandas as pd
import os
import glob
import json

from config import PROCESSED_DATA_PATH, YEARS_TO_PROCESS, FINAL_JSON_PATH, CURSO_MAP

MEDIAS_AGREGADAS_PATH = os.path.join(FINAL_JSON_PATH, 'medias_agregadas_geral.json')
CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv')

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

def analisar_campus_ano(campus_path, campus_name, year, medias_agregadas_map, curso_grupo_map):
    print(f"Analisando: {campus_name} - {year}")
    
    notas_file_path = glob.glob(os.path.join(campus_path, '*arq3.csv'))
    if not notas_file_path:
        print(f"  -> Aviso: arq3.csv não encontrado.")
        return

    try:
        df_notas = pd.read_csv(notas_file_path[0], sep=';', encoding='utf-8', low_memory=False)
        df_notas.columns = [col.upper() for col in df_notas.columns]

        colunas_notas = ['NT_GER', 'NT_FG', 'NT_CE']
        for col in colunas_notas:
             if df_notas[col].dtype == 'object':
                 df_notas[col] = df_notas[col].str.replace(',', '.', regex=False).astype(float)
             df_notas[col] = pd.to_numeric(df_notas[col], errors='coerce')

        analise = df_notas.groupby('CO_CURSO').agg(
            nota_geral_media_curso=('NT_GER', 'mean'),
            nota_fg_media_curso=('NT_FG', 'mean'),
            nota_ce_media_curso=('NT_CE', 'mean'),
            total_participantes=('CO_CURSO', 'size')
        ).reset_index()

        analise['CO_CURSO'] = pd.to_numeric(analise['CO_CURSO'], errors='coerce').astype('Int64')
        analise.dropna(subset=['CO_CURSO'], inplace=True)

        analise['NO_CURSO'] = analise['CO_CURSO'].map(CURSO_MAP).fillna('Nome Desconhecido')
        analise['CAMPUS'] = campus_name
        analise['CO_GRUPO'] = analise['CO_CURSO'].map(curso_grupo_map)
        analise['CO_GRUPO'] = analise['CO_GRUPO'].astype('Int64')
        
        # Pega o mapa de médias do ano específico
        medias_ano_agregadas = medias_agregadas_map.get(str(year), {})
        
        # --- NOVO: Adiciona todas as médias agregadas ---
        def get_all_averages(row):
            grupo = row['CO_GRUPO']
            if pd.isna(grupo):
                return pd.Series([None] * 12) # 4 níveis * 3 notas = 12 colunas
            
            grupo_str = str(int(grupo))
            medias_do_grupo = medias_ano_agregadas.get(grupo_str, {})
            
            return pd.Series([
                medias_do_grupo.get('media_ufc_ger'),
                medias_do_grupo.get('media_ufc_fg'),
                medias_do_grupo.get('media_ufc_ce'),
                medias_do_grupo.get('media_uf_ger'),
                medias_do_grupo.get('media_uf_fg'),
                medias_do_grupo.get('media_uf_ce'),
                medias_do_grupo.get('media_regiao_ger'),
                medias_do_grupo.get('media_regiao_fg'),
                medias_do_grupo.get('media_regiao_ce'),
                medias_do_grupo.get('media_nacional_ger'),
                medias_do_grupo.get('media_nacional_fg'),
                medias_do_grupo.get('media_nacional_ce'),
            ])

        # Nomes das novas colunas
        new_cols = [
            'media_ufc_geral', 'media_ufc_fg', 'media_ufc_ce',
            'media_uf_geral', 'media_uf_fg', 'media_uf_ce',
            'media_regiao_geral', 'media_regiao_fg', 'media_regiao_ce',
            'media_nacional_geral', 'media_nacional_fg', 'media_nacional_ce'
        ]
        
        analise[new_cols] = analise.apply(get_all_averages, axis=1)
        # --- FIM DA ADIÇÃO ---

        analise_final = analise.round(2)

        output_dir = os.path.join(FINAL_JSON_PATH, campus_name)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'visao_geral_{year}.json')

        analise_final.to_json(output_path, orient='records', indent=4, force_ascii=False)
        print(f"  -> Sucesso! Análise salva em '{output_path}'")

    except Exception as e:
        print(f"  -> ERRO ao processar {campus_name}/{year}: {e}")

def main():
    # Carrega os dois mapas necessários
    curso_grupo_map = load_course_metadata()
    medias_agregadas_map = load_single_json(MEDIAS_AGREGADAS_PATH)

    if not medias_agregadas_map or not curso_grupo_map:
        print("Encerrando script. Arquivos 'medias_agregadas_geral.json' ou 'cursos_ufc.csv' não encontrados ou inválidos.")
        return

    os.makedirs(FINAL_JSON_PATH, exist_ok=True)
    campus_folders = [d for d in os.listdir(PROCESSED_DATA_PATH) if os.path.isdir(os.path.join(PROCESSED_DATA_PATH, d))]

    for campus_name in campus_folders:
        for year_str in YEARS_TO_PROCESS:
            campus_year_path = os.path.join(PROCESSED_DATA_PATH, campus_name, str(year_str))
            if os.path.exists(campus_year_path):
                analisar_campus_ano(campus_year_path, campus_name, str(year_str),
                                    medias_agregadas_map, curso_grupo_map)

if __name__ == '__main__':
    main()