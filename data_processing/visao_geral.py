import pandas as pd
import os
import glob
import json

from config import ( PROCESSED_DATA_PATH, YEARS_TO_PROCESS, FINAL_MEDIA_JSON_PATH, FINAL_JSON_PATH, CURSO_MAP)

MEDIAS_NACIONAIS_BASE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Medias_Nacionais')
MEDIAS_UFC_BASE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Medias_UFC')
CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv')

def load_single_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Erro ao carregar {file_path}: {e}")
        return None

def load_averages_all_years(base_path, average_type_name):
    averages_map = {}

    for year in YEARS_TO_PROCESS:
        file_path = os.path.join(base_path, str(year), f'medias_{average_type_name.lower()}.json')
        if os.path.exists(file_path):
            data_year = load_single_json(file_path)
            if data_year:
                 averages_map[str(year)] = data_year
        else:
             averages_map[str(year)] = {}

    return averages_map

def load_course_metadata():
    try:
        df_cursos = pd.read_csv(CURSOS_CSV_PATH, sep=';', usecols=['Código', 'CO_GRUPO'])
        df_cursos.columns = ['CO_CURSO', 'CO_GRUPO']
        df_cursos = df_cursos.dropna(subset=['CO_CURSO', 'CO_GRUPO'])
        df_cursos['CO_CURSO'] = pd.to_numeric(df_cursos['CO_CURSO'], errors='coerce').astype('Int64')
        df_cursos['CO_GRUPO'] = pd.to_numeric(df_cursos['CO_GRUPO'], errors='coerce').astype('Int64')
        df_cursos = df_cursos.drop_duplicates(subset=['CO_CURSO'], keep='first')
        mapa = pd.Series(df_cursos.CO_GRUPO.values, index=df_cursos.CO_CURSO).to_dict()
        return mapa
    except KeyError:
        return {}
    except Exception:
         return {}

def analisar_campus_ano(campus_path, campus_name, year, medias_nacionais_map, medias_ufc_map, curso_grupo_map):

    notas_file_path = glob.glob(os.path.join(campus_path, '*arq3.csv'))

    df_notas = pd.read_csv(notas_file_path[0], sep=';', encoding='utf-8', low_memory=False)
    df_notas.columns = [col.upper() for col in df_notas.columns]

    colunas_notas = ['NT_GER', 'NT_FG', 'NT_CE']
    for col in colunas_notas:
            if df_notas[col].dtype == 'object':
                df_notas[col] = df_notas[col].str.replace(',', '.', regex=False).astype(float)
            df_notas[col] = pd.to_numeric(df_notas[col], errors='coerce')

    analise = df_notas.groupby('CO_CURSO').agg(
        nota_geral_media=('NT_GER', 'mean'),
        nota_fg_media=('NT_FG', 'mean'),
        nota_ce_media=('NT_CE', 'mean'),
        total_participantes=('CO_CURSO', 'size')
    ).reset_index()

    analise['CO_CURSO'] = pd.to_numeric(analise['CO_CURSO'], errors='coerce').astype('Int64')
    analise.dropna(subset=['CO_CURSO'], inplace=True)

    analise['NO_CURSO'] = analise['CO_CURSO'].map(CURSO_MAP).fillna('Nome Desconhecido')
    analise['CAMPUS'] = campus_name
    analise['CO_GRUPO'] = analise['CO_CURSO'].map(curso_grupo_map)
    analise['CO_GRUPO'] = analise['CO_GRUPO'].astype('Int64')

    medias_ano_nacional = medias_nacionais_map.get(str(year), {})
    medias_ano_ufc = medias_ufc_map.get(str(year), {})

    def get_average(row, source_map, prefix, key_suffix):
        grupo = row['CO_GRUPO']
        if pd.isna(grupo): return None
        grupo_str = str(int(grupo))
        return source_map.get(grupo_str, {}).get(f"{prefix}_{key_suffix}")

    analise['media_nacional_geral'] = analise.apply(lambda r: get_average(r, medias_ano_nacional, 'media_nacional', 'geral'), axis=1)
    analise['media_nacional_fg'] = analise.apply(lambda r: get_average(r, medias_ano_nacional, 'media_nacional', 'fg'), axis=1)
    analise['media_nacional_ce'] = analise.apply(lambda r: get_average(r, medias_ano_nacional, 'media_nacional', 'ce'), axis=1)

    analise['media_ufc_geral'] = analise.apply(lambda r: get_average(r, medias_ano_ufc, 'media_ufc', 'geral'), axis=1)
    analise['media_ufc_fg'] = analise.apply(lambda r: get_average(r, medias_ano_ufc, 'media_ufc', 'fg'), axis=1)
    analise['media_ufc_ce'] = analise.apply(lambda r: get_average(r, medias_ano_ufc, 'media_ufc', 'ce'), axis=1)

    analise_final = analise.round(2)

    output_dir = os.path.join(FINAL_JSON_PATH, campus_name)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'visao_geral_{year}.json')

    analise_final.to_json(output_path, orient='records', indent=4, force_ascii=False)
    print(f"  -> Sucesso! Análise salva em '{output_path}'")


def main():
    medias_nacionais_map = load_averages_all_years(MEDIAS_NACIONAIS_BASE_PATH, "Nacionais")

    medias_ufc_map = load_averages_all_years(MEDIAS_UFC_BASE_PATH, "UFC")
    curso_grupo_map = load_course_metadata()

    if not medias_nacionais_map or not medias_ufc_map or curso_grupo_map is None or not curso_grupo_map:
        return

    os.makedirs(FINAL_JSON_PATH, exist_ok=True) # Garante que a pasta base exista
    campus_folders = [d for d in os.listdir(PROCESSED_DATA_PATH) if os.path.isdir(os.path.join(PROCESSED_DATA_PATH, d))]

    for campus_name in campus_folders:
        for year_str in YEARS_TO_PROCESS:
            campus_year_path = os.path.join(PROCESSED_DATA_PATH, campus_name, str(year_str))
            if os.path.exists(campus_year_path):
                analisar_campus_ano(campus_year_path, campus_name, str(year_str),
                                    medias_nacionais_map, medias_ufc_map, curso_grupo_map)

if __name__ == '__main__':
    main()