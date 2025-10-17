import pandas as pd
import os
import glob
import json

from config import PROCESSED_DATA_PATH, YEARS_TO_PROCESS, FINAL_JSON_PATH, CURSO_MAP

def analisar_campus_ano(campus_path, campus_name, year):
    notas_file_path = glob.glob(os.path.join(campus_path, '*arq3.csv'))
    
    try:
        df_notas = pd.read_csv(notas_file_path[0], sep=';', encoding='utf-8', low_memory=False)

        df_notas.columns = [col.upper() for col in df_notas.columns]

        colunas_notas = ['NT_GER', 'NT_FG', 'NT_CE']
        for col in colunas_notas:
            if df_notas[col].dtype == 'object':
                df_notas[col] = df_notas[col].str.replace(',', '.').astype(float)
            df_notas[col] = pd.to_numeric(df_notas[col], errors='coerce')

        analise_geral = df_notas.groupby('CO_CURSO').agg(
            nota_geral_media=('NT_GER', 'mean'),
            nota_fg_media=('NT_FG', 'mean'),
            nota_ce_media=('NT_CE', 'mean'),
            total_alunos=('CO_CURSO', 'size')
        ).reset_index()

        analise_geral['NO_CURSO'] = analise_geral['CO_CURSO'].map(CURSO_MAP)
        analise_geral['NO_CURSO'] = analise_geral['NO_CURSO'].fillna('Nome Desconhecido')
        
        analise_geral['CAMPUS'] = campus_name

        analise_final = analise_geral.round(2)

        output_dir = os.path.join(FINAL_JSON_PATH, campus_name)
        
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f'visao_geral_{year}.json')

        analise_final.to_json(output_path, orient='records', indent=4, force_ascii=False)

    except Exception as e:
        print(f'Erro ao ler arquivos: {e}')

def main():
    os.makedirs(FINAL_JSON_PATH, exist_ok=True)
    campus_folders = [d for d in os.listdir(PROCESSED_DATA_PATH) if os.path.isdir(os.path.join(PROCESSED_DATA_PATH, d))]

    for campus_name in campus_folders:
        for year in YEARS_TO_PROCESS:
            campus_year_path = os.path.join(PROCESSED_DATA_PATH, campus_name, year)
            if os.path.exists(campus_year_path):
                analisar_campus_ano(campus_year_path, campus_name, year)

if __name__ == '__main__':
    main()