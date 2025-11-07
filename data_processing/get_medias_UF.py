import pandas as pd
import os
import glob
import json
from collections import defaultdict
import numpy as np
from tqdm import tqdm

# Importa configurações
from config import RAW_DATA_PATH, YEARS_TO_PROCESS, FINAL_JSON_PATH, FINAL_CE_JSON_PATH

# Caminhos para os arquivos de mapeamento
MAP_JSON_PATH = os.path.join(FINAL_CE_JSON_PATH, 'estrutura_competencias_final.json') # Ajuste o nome se for o simplificado
CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv')
# Caminho de SAÍDA para este script
MEDIAS_UF_BASE_PATH = os.path.join(FINAL_JSON_PATH, 'Medias_UF_Competencia')

# --- Funções Auxiliares (Copie-as do seu script do Colab) ---
# (find_data_files, load_json, get_relevant_grupos, find_required_columns)
# ... (Cole as 4 funções auxiliares aqui) ...
# Exemplo (funções omitidas por brevidade, mas elas SÃO necessárias)

def find_data_files(year_path):
    search_patterns = [
        os.path.join(year_path, '**', '2.DADOS', '*.txt'),
        os.path.join(year_path, '**', '2. DADOS', '*.txt'),
        os.path.join(year_path, '**', 'DADOS', '*.txt')
    ]
    for pattern in search_patterns:
        files = glob.glob(pattern, recursive=True)
        if files:
            return files
    return []

def load_json(file_path, description):
    """Carrega um arquivo JSON com tratamento de erro."""
    print(f"Carregando {description} de '{os.path.basename(file_path)}'...")
    if not os.path.exists(file_path):
        print(f"  -> ERRO: Arquivo não encontrado.")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"  -> ERRO ao carregar JSON: {e}")
        return None
    
def get_relevant_grupos():
    """Lê o arquivo de cursos da UFC e retorna a lista de CO_GRUPOs únicos."""
    if not os.path.exists(CURSOS_CSV_PATH):
        print(f"ERRO: Arquivo '{CURSOS_CSV_PATH}' não encontrado.")
        return None
    try:
        # Ajuste sep=',' ou sep=';' conforme seu arquivo
        df_cursos = pd.read_csv(CURSOS_CSV_PATH, sep=';', usecols=['CO_GRUPO'])
        relevant_grupos = df_cursos['CO_GRUPO'].dropna().unique().tolist()
        relevant_grupos = [int(g) for g in relevant_grupos]
        print(f"CO_GRUPOs relevantes para a UFC: {relevant_grupos}")
        return relevant_grupos
    except Exception as e:
        print(f"Erro ao ler CO_GRUPOs do arquivo de cursos: {e}")
        return None
    
def find_required_columns(file_path, required_cols_variants):
    try:
        df_header = pd.read_csv(file_path, sep=';', encoding='latin1', low_memory=False, nrows=5)
        found_cols_map = {}
        all_found = True

        for standard_name, variants in required_cols_variants.items():
            found_variant = None
            for variant in variants:
                # Busca case-insensitive
                match = next((col for col in df_header.columns if col.upper() == variant.upper()), None)
                if match:
                    found_variant = match
                    break

            if found_variant:
                found_cols_map[standard_name] = found_variant
            else:
                all_found = False
                break # Se uma coluna essencial não for encontrada, não adianta continuar

        return found_cols_map if all_found else None

    except Exception as e:
        # print(f"    -> Aviso: Não foi possível ler cabeçalho de {os.path.basename(file_path)}: {e}")
        return None
# -------------------------------------------------------------

def calculate_regional_averages(year, year_path, relevant_grupos, map_competencias):
    """Calcula médias da Região (Nordeste) por competência (com chunks)."""
    print(f"\nCalculando médias da UF (23) para {year} (chunks)...")
    
    all_raw_files = find_data_files(year_path)
    if not all_raw_files: return None

    # --- Identificação dos Arquivos e Nomes de Colunas ---
    info_file_path = None
    notas_file_path = None
    info_cols_map = None 
    notas_cols_map = None 

    # Colunas que precisamos (INFO)
    info_required = {
        'CO_CURSO': ['CO_CURSO', '"CO_CURSO"'],
        'CO_GRUPO': ['CO_GRUPO', '"CO_GRUPO"'],
        'CO_UF_CURSO': ['CO_UF_CURSO', '"CO_UF_CURSO"'] # <-- FILTRO NOVO
    }
    # Colunas que precisamos (NOTAS)
    disc_note_cols_std = [f'NT_CE_D{i}' for i in range(1, 6)]
    notas_required = {
        'CO_CURSO': ['CO_CURSO', '"CO_CURSO"'],
        'DS_VT_ACE_OCE': ['DS_VT_ACE_OCE', '"DS_VT_ACE_OCE"']
    }

    # ... (Loop de busca pelos arquivos - como no script do Colab) ...
    for file in all_raw_files:
        if not info_file_path:
            found_map = find_required_columns(file, info_required)
            if found_map:
                info_file_path, info_cols_map = file, found_map
                print(f"    -> Arquivo de Info (23) encontrado: {os.path.basename(info_file_path)}")
        if not notas_file_path and 'arq3' in os.path.basename(file).lower():
             found_map = find_required_columns(file, notas_required)
             if found_map:
                 df_header_notas = pd.read_csv(file, sep=';', encoding='latin1', nrows=5)
                 for std_col in disc_note_cols_std:
                     match = next((col for col in df_header_notas.columns if col.upper() == std_col), None)
                     if match: found_map[std_col] = match
                 notas_file_path, notas_cols_map = file, found_map
                 print(f"    -> Arquivo de Notas encontrado: {os.path.basename(notas_file_path)}")
        if info_file_path and notas_file_path: break
            
    if not info_file_path or not notas_file_path: return None
        
    # Extrai os nomes reais das colunas
    real_info_col_curso = info_cols_map['CO_CURSO']
    real_info_col_grupo = info_cols_map['CO_GRUPO']
    real_info_col_uf = info_cols_map['CO_UF_CURSO'] # <-- FILTRO NOVO
    real_notas_col_curso = notas_cols_map['CO_CURSO']
    real_notas_col_respostas = notas_cols_map['DS_VT_ACE_OCE']
    real_disc_cols = [notas_cols_map[std] for std in disc_note_cols_std if std in notas_cols_map]

    try:
        # 1. Carrega df_info filtrado
        print(f"  -> Lendo arquivo de info: {os.path.basename(info_file_path)}...")
        df_info = pd.read_csv(info_file_path, sep=';', encoding='latin1', low_memory=False,
                              usecols=[real_info_col_curso, real_info_col_grupo, real_info_col_uf])
        
        # Converte tipos
        df_info[real_info_col_uf] = pd.to_numeric(df_info[real_info_col_uf], errors='coerce') # <-- FILTRO NOVO
        df_info[real_info_col_grupo] = pd.to_numeric(df_info[real_info_col_grupo], errors='coerce')
        df_info[real_info_col_curso] = pd.to_numeric(df_info[real_info_col_curso], errors='coerce')
        df_info.dropna(subset=[real_info_col_curso, real_info_col_grupo, real_info_col_uf], inplace=True)
        
        # Converte para int
        df_info[real_info_col_uf] = df_info[real_info_col_uf].astype(int) # <-- FILTRO NOVO
        df_info[real_info_col_grupo] = df_info[real_info_col_grupo].astype(int)
        df_info[real_info_col_curso] = df_info[real_info_col_curso].astype('Int64')

        df_info_regiao = df_info[df_info[real_info_col_uf] == 23] 
        # 2. Filtra pelos Grupos Relevantes
        df_info_filtered = df_info_regiao[df_info_regiao[real_info_col_grupo].isin(relevant_grupos)]
        
        relevant_cursos = df_info_filtered[real_info_col_curso].unique().tolist()
        curso_para_grupo_map = pd.Series(df_info_filtered[real_info_col_grupo].astype(str).values, index=df_info_filtered[real_info_col_curso]).to_dict()

        if not relevant_cursos:
             print(f"  -> Aviso: Nenhum curso relevante encontrado para UF 23 em {year}.")
             return None

        # 2. Processa df_notas em chunks
        chunk_size = 500000 
        results_agg = defaultdict(lambda: defaultdict(lambda: {'obj_acertos': 0, 'obj_validas': 0, 'disc_soma': 0.0, 'disc_cont': 0}))
        cols_to_read_notas = [real_notas_col_curso, real_notas_col_respostas] + real_disc_cols
        
        print(f"  -> Lendo {os.path.basename(notas_file_path)} em chunks (filtrando para {len(relevant_cursos)} cursos da UF 23)...")
        reader = pd.read_csv(
            notas_file_path, sep=';', encoding='latin1', low_memory=False, 
            usecols=cols_to_read_notas, iterator=True, chunksize=chunk_size
        )

        for chunk in tqdm(reader, desc=f"Processando Chunks {year} UF 23"):
            chunk.columns = [col.upper() for col in chunk.columns]
            real_notas_col_curso_chunk = next(c for c in chunk.columns if c.upper() == real_notas_col_curso.upper())
            real_notas_col_respostas_chunk = next(c for c in chunk.columns if c.upper() == real_notas_col_respostas.upper())
            real_disc_cols_chunk = [next(c for c in chunk.columns if c.upper() == real_col.upper()) for real_col in real_disc_cols]
            chunk[real_notas_col_curso_chunk] = pd.to_numeric(chunk[real_notas_col_curso_chunk], errors='coerce')
            chunk.dropna(subset=[real_notas_col_curso_chunk], inplace=True)
            chunk[real_notas_col_curso_chunk] = chunk[real_notas_col_curso_chunk].astype('Int64')
            chunk_filtered = chunk[chunk[real_notas_col_curso_chunk].isin(relevant_cursos)].copy()
            if chunk_filtered.empty: continue
            chunk_filtered['CO_GRUPO_str'] = chunk_filtered[real_notas_col_curso_chunk].map(curso_para_grupo_map)
            chunk_filtered.dropna(subset=['CO_GRUPO_str'], inplace=True)
            for col in real_disc_cols_chunk:
                if chunk_filtered[col].dtype == 'object':
                    chunk_filtered.loc[:, col] = chunk_filtered[col].str.replace(',', '.', regex=False)
                chunk_filtered.loc[:, col] = pd.to_numeric(chunk_filtered[col], errors='coerce')
            for index, row in chunk_filtered.iterrows():
                 co_grupo_str = row['CO_GRUPO_str']
                 map_grupo = map_competencias.get(co_grupo_str, {})
                 lista_componentes = map_grupo.get('Componente_especifico', [])
                 map_ano = map_grupo.get('Anos', {}).get(str(year), {})
                 questoes_ce = map_ano.get('questoes_CE', {})
                 map_obj = questoes_ce.get('objetivas', {})
                 map_disc = questoes_ce.get('discursivas', {})
                 respostas_obj = str(row[real_notas_col_respostas_chunk]) if pd.notna(row[real_notas_col_respostas_chunk]) else ''
                 if len(respostas_obj) >= 27:
                     for q_key, mapeamento in map_obj.items():
                         try:
                             q_index = int(q_key[1:]) - 9
                             indices = mapeamento if isinstance(mapeamento, list) else [mapeamento]
                             for idx_1 in indices:
                                 idx_0 = int(idx_1) - 1
                                 if 0 <= idx_0 < len(lista_componentes):
                                     comp = lista_componentes[idx_0]
                                     resp = respostas_obj[q_index]
                                     if resp in ['0', '1']:
                                         results_agg[co_grupo_str][comp]['obj_validas'] += 1
                                         if resp == '1':
                                             results_agg[co_grupo_str][comp]['obj_acertos'] += 1
                         except: continue
                 for d_key, mapeamento in map_disc.items():
                     try:
                         suffix = int(d_key[1:]) - 2
                         col_name = f"NT_CE_D{suffix}".upper()
                         real_col_name_found = next((c for c in real_disc_cols_chunk if c.upper() == col_name), None)
                         if not real_col_name_found: continue
                         indices = mapeamento if isinstance(mapeamento, list) else [mapeamento]
                         for idx_1 in indices:
                             idx_0 = int(idx_1) - 1
                             if 0 <= idx_0 < len(lista_componentes):
                                 comp = lista_componentes[idx_0]
                                 nota = row[real_col_name_found]
                                 if pd.notna(nota):
                                     results_agg[co_grupo_str][comp]['disc_soma'] += nota
                                     results_agg[co_grupo_str][comp]['disc_cont'] += 1
                     except: continue

        # 3. Calcula a média final
        if not results_agg: return None
             
        final_means = {}
        for grupo, comps in results_agg.items():
            final_means[grupo] = {}
            for comp, data in comps.items():
                percentual_obj = (data['obj_acertos'] / data['obj_validas'] * 100) if data['obj_validas'] > 0 else None
                media_disc = (data['disc_soma'] / data['disc_cont']) if data['disc_cont'] > 0 else None
                # Renomeia as chaves para 'regiao'
                final_means[grupo][comp] = {
                    "percentual_objetivas_uf": round(percentual_obj, 2) if percentual_obj is not None else None,
                    "media_discursivas_uf": round(media_disc, 2) if media_disc is not None else None,
                    "n_objetivas_validas_uf": data['obj_validas'],
                    "n_discursivas_validas_uf": data['disc_cont']
                }
        
        print(f"  -> Médias da UF 23 (chunks) calculadas para {year}.")
        return final_means # Retorna { "4003": { "Algoritmos": {...}, ... }, ... }

    except Exception as e:
        print(f"  -> ERRO GERAL ao processar médias da UF 23 de {year}: {e}")
        return None

def main():
    relevant_grupos = get_relevant_grupos()
    map_competencias = load_json(MAP_JSON_PATH, "Mapeamento de Competências")
    if relevant_grupos is None or map_competencias is None:
        print("Encerrando script devido a erro ao obter arquivos de mapeamento.")
        return

    os.makedirs(MEDIAS_UF_BASE_PATH, exist_ok=True)
    print(f"\nSalvando médias da UF 23 em subpastas anuais dentro de '{MEDIAS_UF_BASE_PATH}'...")

    for year in YEARS_TO_PROCESS:
        year_extract_path = os.path.join(RAW_DATA_PATH, f'enade_{year}')
        medias_ano = calculate_regional_averages(year, year_extract_path, relevant_grupos, map_competencias) 
        
        if medias_ano:
            data_to_save = {str(k): v for k, v in medias_ano.items()}
            year_dir = os.path.join(MEDIAS_UF_BASE_PATH, str(year))
            os.makedirs(year_dir, exist_ok=True)
            output_path = os.path.join(year_dir, 'medias_uf_competencia.json') # Nome do arquivo
            
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data_to_save, f, ensure_ascii=False, indent=4)
                print(f"  -> Médias de {year} salvas em '{output_path}'")
            except Exception as e:
                print(f"  -> ERRO ao salvar médias de {year}: {e}")
        else:
             print(f"  -> Aviso: Não foram calculadas médias de competência para {year}.")

    print("\nProcesso de geração de médias da UF 23 por ano concluído.")

if __name__ == '__main__':
    main()