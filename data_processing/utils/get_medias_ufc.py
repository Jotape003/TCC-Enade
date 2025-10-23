import pandas as pd
import os
import glob
import json
from tqdm import tqdm
from config import PROCESSED_DATA_PATH, YEARS_TO_PROCESS, FINAL_MEDIA_JSON_PATH, CURSOS_CSV_PATH

MEDIAS_UFC_BASE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Medias_UFC')

def get_relevant_grupos():
    if not os.path.exists(CURSOS_CSV_PATH):
        return None
    try:
        df_cursos = pd.read_csv(CURSOS_CSV_PATH, sep=';', usecols=['CO_GRUPO'])
        relevant_grupos = df_cursos['CO_GRUPO'].dropna().unique().tolist()
        relevant_grupos = [int(grupos) for grupos in relevant_grupos]
        return relevant_grupos
    except Exception as e:
        return None
    
def calculate_ufc_averages_for_year(year, relevant_grupos):
    print(f"\nCalculando médias da UFC para {year} (apenas grupos relevantes)...")
    
    all_campus_dfs_info = []
    all_campus_dfs_notas = []
    
    campus_folders_year = glob.glob(os.path.join(PROCESSED_DATA_PATH, '*', str(year)))

    if not campus_folders_year:
        print(f"  -> Aviso: Nenhuma pasta de campus encontrada para {year}.")
        return None

    print(f"  -> Lendo dados de {len(campus_folders_year)} campi...")
    for campus_path in campus_folders_year:
        arq1_path = glob.glob(os.path.join(campus_path, '*arq1.csv'))
        arq3_path = glob.glob(os.path.join(campus_path, '*arq3.csv'))

        if arq1_path and arq3_path:
            try:
                df_info_campus = pd.read_csv(arq1_path[0], sep=';', encoding='utf-8', usecols=['CO_CURSO', 'CO_GRUPO'])
                df_notas_campus = pd.read_csv(arq3_path[0], sep=';', encoding='utf-8', usecols=['CO_CURSO', 'NT_GER', 'NT_FG', 'NT_CE'])
                all_campus_dfs_info.append(df_info_campus)
                all_campus_dfs_notas.append(df_notas_campus)
            except Exception as e:
                print(f"  -> Aviso: Erro ao ler arquivos de {os.path.basename(campus_path)}: {e}")
        else:
            print(f"  -> Aviso: Arquivos arq1.csv ou arq3.csv ausentes em {os.path.basename(campus_path)}.")

    if not all_campus_dfs_info or not all_campus_dfs_notas:
        print(f"  -> Erro: Não foi possível ler dados suficientes para calcular médias da UFC em {year}.")
        return None

    df_info_ufc = pd.concat(all_campus_dfs_info, ignore_index=True)
    df_notas_ufc = pd.concat(all_campus_dfs_notas, ignore_index=True)

    try:
        df_info_ufc['CO_GRUPO'] = pd.to_numeric(df_info_ufc['CO_GRUPO'], errors='coerce')
        df_info_ufc.dropna(subset=['CO_GRUPO'], inplace=True)
        df_info_ufc['CO_GRUPO'] = df_info_ufc['CO_GRUPO'].astype(int)
        df_info_filtered = df_info_ufc[df_info_ufc['CO_GRUPO'].isin(relevant_grupos)]
        
        relevant_cursos_ufc = df_info_filtered['CO_CURSO'].unique().tolist()
        df_notas_filtered = df_notas_ufc[df_notas_ufc['CO_CURSO'].isin(relevant_cursos_ufc)].copy()

        colunas_notas = ['NT_GER', 'NT_FG', 'NT_CE']
        for col in colunas_notas:
            if df_notas_filtered[col].dtype == 'object':
                df_notas_filtered.loc[:, col] = df_notas_filtered[col].str.replace(',', '.', regex=False).astype(float)
            df_notas_filtered.loc[:, col] = pd.to_numeric(df_notas_filtered[col], errors='coerce')
        df_notas_filtered.dropna(subset=colunas_notas, inplace=True)

        df_merged_ufc = pd.merge(df_notas_filtered, df_info_filtered, on='CO_CURSO')

        medias_ufc = df_merged_ufc.groupby('CO_GRUPO').agg(
            media_ufc_geral=('NT_GER', 'mean'),
            media_ufc_fg=('NT_FG', 'mean'),
            media_ufc_ce=('NT_CE', 'mean')
        ).reset_index()

        medias_ufc = medias_ufc.round(2)
        print(f"  -> Médias da UFC calculadas para {year}.")
        return medias_ufc.set_index('CO_GRUPO').to_dict(orient='index')

    except Exception as e:
        print(f"  -> ERRO ao processar médias da UFC de {year}: {e}")
        return None

def main():
    relevant_grupos = get_relevant_grupos()

    os.makedirs(MEDIAS_UFC_BASE_PATH, exist_ok=True)
    

    for year in YEARS_TO_PROCESS:
        medias_ano = calculate_ufc_averages_for_year(year, relevant_grupos)
        
        if medias_ano:
            data_to_save = {str(key): v for key, v in medias_ano.items()}
            
            year_dir = os.path.join(MEDIAS_UFC_BASE_PATH, str(year))
            os.makedirs(year_dir, exist_ok=True)
            
            output_path = os.path.join(year_dir, 'medias_ufc.json')
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()