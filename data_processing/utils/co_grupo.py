import pandas as pd
import os
import glob
from config import RAW_DATA_PATH, YEARS_TO_PROCESS
from filter_data import find_data_files 

CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv')

def get_curso_grupo_map_from_raw_data():
    print("Buscando mapeamento CO_CURSO -> CO_GRUPO em todos os anos disponíveis...")
    
    curso_grupo_map_final = {}
    
    for year in sorted(YEARS_TO_PROCESS, reverse=True):
        print(f"  Processando ano: {year}")
        year_extract_path = os.path.join(RAW_DATA_PATH, f'enade_{year}')
        
        if not os.path.exists(year_extract_path):
            print(f"    -> Pasta de dados brutos não encontrada para {year}. Pulando.")
            continue

        all_raw_files = find_data_files(year_extract_path)
        arq1_path = next((f for f in all_raw_files if 'arq1' in os.path.basename(f).lower()), None)

        if not arq1_path:
            print(f"    -> Arquivo arq1 não encontrado para {year}. Pulando.")
            continue

        try:
            df_info_raw = pd.read_csv(
                arq1_path, 
                sep=';', 
                encoding='latin1', 
                low_memory=False, 
                usecols=['CO_CURSO', 'CO_GRUPO']
            )
            df_info_raw.columns = [col.upper() for col in df_info_raw.columns]

            numeric_cols = ['CO_CURSO', 'CO_GRUPO']
            for col in numeric_cols:
                df_info_raw[col] = pd.to_numeric(df_info_raw[col], errors='coerce')
            
            df_info_raw.dropna(subset=numeric_cols, inplace=True)
            
            for col in numeric_cols:
                df_info_raw[col] = df_info_raw[col].astype('Int64')

            df_map_year = df_info_raw.drop_duplicates(subset=['CO_CURSO'])
            mapa_ano_atual = pd.Series(df_map_year.CO_GRUPO.values, index=df_map_year.CO_CURSO).to_dict()
            
            novos_mapeamentos = 0
            for curso_cod, grupo_cod in mapa_ano_atual.items():
                if curso_cod not in curso_grupo_map_final:
                    curso_grupo_map_final[curso_cod] = grupo_cod
                    novos_mapeamentos += 1

        except Exception:
            continue

    if not curso_grupo_map_final:
        return None
    else:
        return curso_grupo_map_final

def main():
    curso_grupo_map = get_curso_grupo_map_from_raw_data()
    if curso_grupo_map is None:
        return
    
    try:
        df_cursos_ufc = pd.read_csv(CURSOS_CSV_PATH, sep=';', encoding='utf-8') 
        coluna_codigo = 'Código'
        df_cursos_ufc[coluna_codigo] = pd.to_numeric(df_cursos_ufc[coluna_codigo], errors='coerce')
        df_cursos_ufc.dropna(subset=[coluna_codigo], inplace=True)
        df_cursos_ufc[coluna_codigo] = df_cursos_ufc[coluna_codigo].astype('Int64')
    except Exception as e:
        print(f"ERRO ao ler {CURSOS_CSV_PATH}: {e}")
        return

    df_cursos_ufc['CO_GRUPO'] = df_cursos_ufc['Código'].map(curso_grupo_map)
    
    df_cursos_ufc['CO_GRUPO'] = df_cursos_ufc['CO_GRUPO'].astype('Int64')

    try:
        df_cursos_ufc.to_csv(CURSOS_CSV_PATH, sep=';', index=False, encoding='utf-8')
        print(f"\nSucesso! Arquivo '{CURSOS_CSV_PATH}' atualizado com a coluna 'CO_GRUPO'.")
    except Exception as e:
        print(f"ERRO ao salvar o arquivo atualizado: {e}")

if __name__ == '__main__':
    main()