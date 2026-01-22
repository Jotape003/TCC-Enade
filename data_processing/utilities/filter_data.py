import pandas as pd
import os
import glob
from tqdm import tqdm
from utils import find_data_files 
from config import YEARS_TO_PROCESS, RAW_DATA_PATH, PROCESSED_DATA_PATH, UFC_IES_CODE, CAMPUS_MAP

def get_ufc_courses_by_campus(year, year_path):
    # Busca recursiva com os múltiplos padrões de nomenclatura dos microdados
    files = find_data_files(year_path)
    if not files:
        return {}
        
    course_info_file = files[0]

    try:
        # Leitura e padronização dos dados
        df_info = pd.read_csv(course_info_file, sep=';', encoding='latin1', low_memory=False)
        df_info.columns = [col.upper() for col in df_info.columns]

        # Convertendo para numérico e removendo nulos
        numeric_cols = ['CO_IES', 'CO_MUNIC_CURSO']
        for col in numeric_cols:
            df_info[col] = pd.to_numeric(df_info[col], errors='coerce')

        df_info.dropna(subset=numeric_cols, inplace=True)
        
        for col in numeric_cols:
            df_info[col] = df_info[col].astype('Int64')
        
        # Filtrando apenas os cursos da UFC
        df_ufc = df_info[df_info['CO_IES'] == UFC_IES_CODE]

        if df_ufc.empty:
            print(f"Diagnóstico {year}: O DataFrame 'df_ufc' está vazio após o filtro de IES.")
            return {}

        # Criando o mapeamento por campus
        campus_map = df_ufc.groupby('CO_MUNIC_CURSO')['CO_CURSO'].apply(list).to_dict()
        return campus_map

    except Exception as e:
        print(f"Erro ao ler o arquivo de informações de curso '{course_info_file}': {e}")
        return {}

def process_year(year):
    year_extract_path = os.path.join(RAW_DATA_PATH, f'enade_{year}')

    campus_to_courses_map = get_ufc_courses_by_campus(year, year_extract_path)
    if not campus_to_courses_map:
        return

    # Criando os diretórios de saída
    for campus_code in campus_to_courses_map.keys():
        campus_name = CAMPUS_MAP.get(campus_code, f'campus_desconhecido_{int(campus_code)}')
        year_output_dir = os.path.join(PROCESSED_DATA_PATH, campus_name, str(year))
        os.makedirs(year_output_dir, exist_ok=True)
    
    # Varrendo os arquivos de dados
    all_source_files = find_data_files(year_extract_path)

    for source_file_path in tqdm(all_source_files, desc=f"Filtrando arquivos de {year}"):
        try:
            df_source = pd.read_csv(source_file_path, sep=';', encoding='latin1', low_memory=False)
            df_source.columns = [col.upper() for col in df_source.columns]

            if 'CO_CURSO' not in df_source.columns:
                continue

            # Pegando apenas as linhas dos cursos da UFC por campus
            for campus_code, course_list in campus_to_courses_map.items():
                df_filtered = df_source[df_source['CO_CURSO'].isin(course_list)]

                if not df_filtered.empty:
                    base_filename = os.path.basename(source_file_path)
                    
                    csv_filename = os.path.splitext(base_filename)[0] + '.csv'
                    
                    campus_name = CAMPUS_MAP.get(campus_code, f'campus_desconhecido_{int(campus_code)}')
                    output_dir = os.path.join(PROCESSED_DATA_PATH, campus_name, str(year))
                    output_path = os.path.join(output_dir, csv_filename)
                    
                    # Salvando em UTF-8
                    df_filtered.to_csv(output_path, sep=';', index=False, encoding='utf-8')

        except Exception as e:
            print(f"\nErro ao processar o arquivo '{os.path.basename(source_file_path)}': {e}")
            continue

def main():
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    for year in YEARS_TO_PROCESS:
        process_year(year)

if __name__ == '__main__':
    main()