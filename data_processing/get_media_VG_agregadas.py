import pandas as pd
import os
import glob
import json
from collections import defaultdict
import numpy as np
from tqdm import tqdm

# Importa configurações
from config import RAW_DATA_PATH, YEARS_TO_PROCESS, FINAL_JSON_PATH

# Caminhos
CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv')
OUTPUT_PATH = os.path.join(FINAL_JSON_PATH, 'medias_agregadas_geral.json')

# --- Funções Auxiliares (find_data_files, get_relevant_grupos, find_required_columns) ---
# (Estas são as funções robustas que já desenvolvemos)

def find_data_files(year_path):
    """Busca recursivamente os arquivos de dados (.txt ou .csv)."""
    search_patterns = [
        os.path.join(year_path, '**', '2.DADOS', '*.txt'),
        os.path.join(year_path, '**', '2.DADOS', '*.csv'),
        os.path.join(year_path, '**', '2. DADOS', '*.txt'),
        os.path.join(year_path, '**', '2. DADOS', '*.csv'),
        os.path.join(year_path, '**', 'DADOS', '*.txt'),
        os.path.join(year_path, '**', 'DADOS', '*.csv')
    ]
    found_files = []
    for pattern in search_patterns:
        files = glob.glob(pattern, recursive=True)
        if files: found_files.extend(files)
    if not found_files: print(f"  -> AVISO: Nenhum arquivo de dados encontrado para {year_path}.")
    return found_files

def get_relevant_grupos():
    """Lê o arquivo de cursos da UFC e retorna a lista de CO_GRUPOs únicos."""
    if not os.path.exists(CURSOS_CSV_PATH):
        print(f"ERRO: Arquivo '{CURSOS_CSV_PATH}' não encontrado.")
        return None
    try:
        df_cursos = pd.read_csv(CURSOS_CSV_PATH, sep=';', usecols=['CO_GRUPO']) # Ajuste 'sep'
        relevant_grupos = df_cursos['CO_GRUPO'].dropna().unique().tolist()
        relevant_grupos = [int(g) for g in relevant_grupos]
        print(f"CO_GRUPOs relevantes para a UFC: {relevant_grupos}")
        return relevant_grupos
    except Exception as e:
        print(f"Erro ao ler CO_GRUPOs do arquivo de cursos: {e}")
        return None

def find_required_columns(file_path, required_cols_variants):
    """Lê o cabeçalho e verifica a presença de colunas necessárias."""
    try:
        df_header = pd.read_csv(file_path, sep=';', encoding='latin1', low_memory=False, nrows=5)
        found_cols_map = {}
        all_found = True
        for standard_name, variants in required_cols_variants.items():
            found_variant = next((col for col in df_header.columns if col.upper() in [v.upper() for v in variants]), None)
            if found_variant:
                found_cols_map[standard_name] = found_variant
            else:
                all_found = False
                break
        return found_cols_map if all_found else None
    except Exception as e:
        return None

# --- Função Principal de Cálculo ---

def calculate_all_averages(year, year_path, relevant_grupos):
    """Calcula médias Nacionais, Regionais, UF e UFC para os grupos relevantes."""
    print(f"\nCalculando médias agregadas para {year} (chunks)...")
    
    all_raw_files = find_data_files(year_path)
    
    # Colunas que precisamos (INFO)
    info_required = {
        'CO_CURSO': ['CO_CURSO', '"CO_CURSO"'],
        'CO_GRUPO': ['CO_GRUPO', '"CO_GRUPO"'],
        'CO_IES': ['CO_IES', '"CO_IES"'],
        'CO_REGIAO_CURSO': ['CO_REGIAO_CURSO', '"CO_REGIAO_CURSO"'],
        'CO_UF_CURSO': ['CO_UF_CURSO', '"CO_UF_CURSO"']
    }
    # Colunas que precisamos (NOTAS)
    notas_required = {
        'CO_CURSO': ['CO_CURSO', '"CO_CURSO"'],
        'NT_GER': ['NT_GER', '"NT_GER"'],
        'NT_FG': ['NT_FG', '"NT_FG"'],
        'NT_CE': ['NT_CE', '"NT_CE"']
    }

    # --- Identificação dos Arquivos e Nomes de Colunas ---
    info_file_path, notas_file_path, info_cols_map, notas_cols_map = None, None, None, None
    for file in all_raw_files:
        if not info_file_path:
            found_map = find_required_columns(file, info_required)
            if found_map:
                info_file_path, info_cols_map = file, found_map
                print(f"    -> Arquivo de Info encontrado: {os.path.basename(info_file_path)}")
        if not notas_file_path and 'arq3' in os.path.basename(file).lower():
             found_map = find_required_columns(file, notas_required)
             if found_map:
                 notas_file_path, notas_cols_map = file, found_map
                 print(f"    -> Arquivo de Notas encontrado: {os.path.basename(notas_file_path)}")
        if info_file_path and notas_file_path: break
            
    if not info_file_path or not notas_file_path:
        print(f"  -> ERRO CRÍTICO: Não foi possível encontrar arquivos/colunas essenciais para {year}.")
        return None
        
    # Extrai os nomes reais das colunas
    real_col = lambda map, key: map[key]
    col_info_curso = real_col(info_cols_map, 'CO_CURSO')
    col_info_grupo = real_col(info_cols_map, 'CO_GRUPO')
    col_info_ies = real_col(info_cols_map, 'CO_IES')
    col_info_regiao = real_col(info_cols_map, 'CO_REGIAO_CURSO')
    col_info_uf = real_col(info_cols_map, 'CO_UF_CURSO')
    
    col_notas_curso = real_col(notas_cols_map, 'CO_CURSO')
    col_notas_ger = real_col(notas_cols_map, 'NT_GER')
    col_notas_fg = real_col(notas_cols_map, 'NT_FG')
    col_notas_ce = real_col(notas_cols_map, 'NT_CE')
    notas_cols_real_list = [col_notas_curso, col_notas_ger, col_notas_fg, col_notas_ce]
    notas_num_cols_real_list = [col_notas_ger, col_notas_fg, col_notas_ce]

    try:
        # 1. Carrega df_info filtrado
        print(f"  -> Lendo arquivo de info: {os.path.basename(info_file_path)}...")
        df_info = pd.read_csv(info_file_path, sep=';', encoding='latin1', low_memory=False,
                              usecols=[col_info_curso, col_info_grupo, col_info_ies, col_info_regiao, col_info_uf])
        
        # Converte tipos (necessário para filtros e merge)
        for col in [col_info_grupo, col_info_ies, col_info_regiao, col_info_uf]:
             df_info[col] = pd.to_numeric(df_info[col], errors='coerce')
        df_info[col_info_curso] = pd.to_numeric(df_info[col_info_curso], errors='coerce')
        df_info.dropna(subset=[col_info_curso, col_info_grupo, col_info_ies, col_info_regiao, col_info_uf], inplace=True)
        for col in [col_info_grupo, col_info_ies, col_info_regiao, col_info_uf]:
             df_info[col] = df_info[col].astype(int)
        df_info[col_info_curso] = df_info[col_info_curso].astype('Int64')

        # Filtra apenas pelos grupos relevantes (ECONOMIZA MUITA MEMÓRIA)
        df_info_filtered = df_info[df_info[col_info_grupo].isin(relevant_grupos)]
        
        # Cria o mapa de curso para {grupo, ies, regiao, uf}
        # Renomeia colunas para o merge
        df_info_map = df_info_filtered.rename(columns={
            col_info_curso: 'CO_CURSO',
            col_info_grupo: 'CO_GRUPO',
            col_info_ies: 'CO_IES',
            col_info_regiao: 'CO_REGIAO_CURSO',
            col_info_uf: 'CO_UF_CURSO'
        })
        # Remove cursos duplicados, mantendo um mapa limpo
        df_info_map = df_info_map.drop_duplicates(subset=['CO_CURSO'], keep='first')


        # 2. Processa df_notas em chunks
        chunk_size = 500000 
        # Acumuladores para somas e contagens
        levels = ['nacional', 'regiao', 'uf', 'ufc']
        accumulators_sum = {level: defaultdict(lambda: defaultdict(float)) for level in levels}
        accumulators_count = {level: defaultdict(lambda: defaultdict(int)) for level in levels}
        
        print(f"  -> Lendo {os.path.basename(notas_file_path)} em chunks...")
        reader = pd.read_csv(
            notas_file_path, sep=';', encoding='latin1', low_memory=False, 
            usecols=notas_cols_real_list, iterator=True, chunksize=chunk_size
        )

        for chunk in tqdm(reader, desc=f"Processando Chunks {year}"):
            chunk.columns = [col.upper() for col in chunk.columns]
            real_notas_col_curso_chunk = next(c for c in chunk.columns if c.upper() == col_notas_curso.upper())
            
            # Converte CO_CURSO no chunk
            chunk[real_notas_col_curso_chunk] = pd.to_numeric(chunk[real_notas_col_curso_chunk], errors='coerce')
            chunk.dropna(subset=[real_notas_col_curso_chunk], inplace=True)
            chunk[real_notas_col_curso_chunk] = chunk[real_notas_col_curso_chunk].astype('Int64')
            
            # Renomeia colunas de notas para padrão
            chunk.rename(columns={
                real_notas_col_curso_chunk: 'CO_CURSO',
                real_col(notas_cols_map, 'NT_GER'): 'NT_GER',
                real_col(notas_cols_map, 'NT_FG'): 'NT_FG',
                real_col(notas_cols_map, 'NT_CE'): 'NT_CE',
            }, inplace=True)

            # Junta o chunk com o mapa de infos (operação rápida)
            chunk_merged = pd.merge(chunk, df_info_map, on='CO_CURSO', how='inner') # inner join filtra pelos cursos relevantes
            if chunk_merged.empty: continue
            
            # Limpa notas
            colunas_notas_std = ['NT_GER', 'NT_FG', 'NT_CE']
            for col in colunas_notas_std:
                if chunk_merged[col].dtype == 'object':
                    chunk_merged.loc[:, col] = chunk_merged[col].str.replace(',', '.', regex=False).astype(float)
                chunk_merged.loc[:, col] = pd.to_numeric(chunk_merged[col], errors='coerce')
            chunk_merged.dropna(subset=colunas_notas_std, inplace=True)
            
            # Agrega para cada nível
            for col_nota in colunas_notas_std:
                # 1. Nacional (todos no chunk)
                sum_nacional = chunk_merged.groupby('CO_GRUPO')[col_nota].sum()
                count_nacional = chunk_merged.groupby('CO_GRUPO')[col_nota].count()
                for grupo, val in sum_nacional.items(): accumulators_sum['nacional'][grupo][col_nota] += val
                for grupo, val in count_nacional.items(): accumulators_count['nacional'][grupo][col_nota] += val
                
                # 2. Região (Nordeste = 2)
                chunk_regiao = chunk_merged[chunk_merged['CO_REGIAO_CURSO'] == 2]
                sum_regiao = chunk_regiao.groupby('CO_GRUPO')[col_nota].sum()
                count_regiao = chunk_regiao.groupby('CO_GRUPO')[col_nota].count()
                for grupo, val in sum_regiao.items(): accumulators_sum['regiao'][grupo][col_nota] += val
                for grupo, val in count_regiao.items(): accumulators_count['regiao'][grupo][col_nota] += val
                
                # 3. UF (Ceará = 23)
                chunk_uf = chunk_merged[chunk_merged['CO_UF_CURSO'] == 23]
                sum_uf = chunk_uf.groupby('CO_GRUPO')[col_nota].sum()
                count_uf = chunk_uf.groupby('CO_GRUPO')[col_nota].count()
                for grupo, val in sum_uf.items(): accumulators_sum['uf'][grupo][col_nota] += val
                for grupo, val in count_uf.items(): accumulators_count['uf'][grupo][col_nota] += val
                
                # 4. UFC (IES = 583)
                chunk_ufc = chunk_merged[chunk_merged['CO_IES'] == 583]
                sum_ufc = chunk_ufc.groupby('CO_GRUPO')[col_nota].sum()
                count_ufc = chunk_ufc.groupby('CO_GRUPO')[col_nota].count()
                for grupo, val in sum_ufc.items(): accumulators_sum['ufc'][grupo][col_nota] += val
                for grupo, val in count_ufc.items(): accumulators_count['ufc'][grupo][col_nota] += val

        # 3. Calcula as médias finais
        final_means_year = {}
        all_grupos = accumulators_sum['nacional'].keys() # Pega todos os grupos processados
        
        for grupo in all_grupos:
            grupo_str = str(grupo)
            final_means_year[grupo_str] = {}
            for col_nota in colunas_notas_std:
                # Renomeia colunas para o JSON final
                col_sufixo = col_nota.split('_')[1].lower() # 'ger', 'fg', 'ce'
                
                for level in levels:
                    soma = accumulators_sum[level].get(grupo, {}).get(col_nota, 0)
                    cont = accumulators_count[level].get(grupo, {}).get(col_nota, 0)
                    media = (soma / cont) if cont > 0 else None
                    
                    chave_json = f"media_{level}_{col_sufixo}" # ex: media_nacional_ger
                    final_means_year[grupo_str][chave_json] = round(media, 2) if media is not None else None

        print(f"  -> Médias agregadas (chunks) calculadas para {year}.")
        return final_means_year # Retorna { "4003": { "media_nacional_ger": 55.2, ... }, ... }

    except Exception as e:
        print(f"  -> ERRO GERAL ao processar médias agregadas de {year}: {e}")
        return None

# --- Função Main (Orquestração) ---
def main():
    relevant_grupos = get_relevant_grupos()
    if relevant_grupos is None:
        print("Encerrando script devido a erro ao obter CO_GRUPOs.")
        return

    os.makedirs(FINAL_JSON_PATH, exist_ok=True)
    medias_totais_todos_anos = {}

    for year in YEARS_TO_PROCESS:
        year_extract_path = os.path.join(RAW_DATA_PATH, f'enade_{year}')
        medias_ano = calculate_all_averages(year, year_extract_path, relevant_grupos) 
        if medias_ano:
            medias_totais_todos_anos[str(year)] = medias_ano

    # Salva um único arquivo JSON com as médias de todos os anos e níveis
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(medias_totais_todos_anos, f, ensure_ascii=False, indent=4)
    
    print(f"\nSucesso! Médias agregadas salvas em '{OUTPUT_PATH}'")

if __name__ == '__main__':
    main()