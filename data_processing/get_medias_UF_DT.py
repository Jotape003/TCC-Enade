import pandas as pd
import os
import glob
import json
from collections import defaultdict
import numpy as np
from tqdm import tqdm

# Importa configurações (ajuste os nomes das variáveis do config se necessário)
from config import RAW_DATA_PATH, YEARS_TO_PROCESS, FINAL_MEDIA_JSON_PATH, FINAL_ESTRUTURA_JSON_PATH

# --- Caminhos de ENTRADA ---
MAP_CE_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_competencias_final.json')
MAP_FG_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_fg_final.json')
CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv') # Usado para pegar a lista de CO_GRUPOs relevantes

# --- Caminhos de SAÍDA ---
MEDIAS_UF_CE_BASE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'CE', 'Medias_agregadas')
MEDIAS_UF_FG_BASE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'FG', 'Medias_agregadas')

# --- Funções Auxiliares (Copie/Cole-as do seu script anterior ou do Colab) ---
def find_data_files(year_path):
    """Busca recursivamente os arquivos de dados (.txt ou .csv)."""
    print(f"--- Buscando arquivos em: {year_path}")
    if not os.path.exists(year_path):
        print(f"  -> ERRO: O caminho base não existe: {year_path}")
        return []
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

def load_json(file_path, description):
    print(f"Carregando {description} de '{os.path.basename(file_path)}'...")
    if not os.path.exists(file_path):
        print(f"  -> ERRO: Arquivo não encontrado em: {file_path}")
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
        df_cursos = pd.read_csv(CURSOS_CSV_PATH, sep=';', usecols=['CO_GRUPO']) # Ajuste 'sep'
        relevant_grupos = df_cursos['CO_GRUPO'].dropna().unique().tolist()
        relevant_grupos = [int(g) for g in relevant_grupos]
        print(f"CO_GRUPOs relevantes (base UFC): {relevant_grupos}")
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
# -----------------------------------------------------------------

def calculate_uf_averages(year, year_path, relevant_grupos, map_competencias_ce, map_competencias_fg):
    """Calcula médias da UF (Ceará=23) por competência (com chunks) para CE e FG."""
    print(f"\nCalculando médias da UF (Ceará) por Competência para {year} (chunks)...")
    
    all_raw_files = find_data_files(year_path)
    if not all_raw_files: return None, None

    # --- Identificação dos Arquivos e Nomes de Colunas ---
    info_file_path, notas_file_path, info_cols_map, notas_cols_map = None, None, None, None

    info_required = {
        'CO_CURSO': ['CO_CURSO', '"CO_CURSO"'],
        'CO_GRUPO': ['CO_GRUPO', '"CO_GRUPO"'],
        'CO_UF_CURSO': ['CO_UF_CURSO', '"CO_UF_CURSO"'] # <-- Filtro UF
    }
    disc_note_cols_std_ce = [f'NT_CE_D{i}' for i in range(1, 6)]
    disc_note_cols_std_fg = [f'NT_FG_D{i}' for i in range(1, 3)]
    notas_required = {
        'CO_CURSO': ['CO_CURSO', '"CO_CURSO"'],
        'DS_VT_ACE_OCE': ['DS_VT_ACE_OCE', '"DS_VT_ACE_OCE"'],
        'DS_VT_ACE_OFG': ['DS_VT_ACE_OFG', '"DS_VT_ACE_OFG"']
    }

    for file in all_raw_files:
        if not info_file_path:
            found_map = find_required_columns(file, info_required)
            if found_map:
                info_file_path, info_cols_map = file, found_map
                print(f"    -> Arquivo de Info (UF) encontrado: {os.path.basename(info_file_path)}")
        
        if not notas_file_path and 'arq3' in os.path.basename(file).lower():
             found_map = find_required_columns(file, notas_required)
             if found_map:
                 df_header_notas = pd.read_csv(file, sep=';', encoding='latin1', nrows=5)
                 for std_col in disc_note_cols_std_ce + disc_note_cols_std_fg:
                     match = next((col for col in df_header_notas.columns if col.upper() == std_col), None)
                     if match: found_map[std_col] = match
                 notas_file_path, notas_cols_map = file, found_map
                 print(f"    -> Arquivo de Notas encontrado: {os.path.basename(notas_file_path)}")
        
        if info_file_path and notas_file_path: break
            
    if not info_file_path or not notas_file_path:
        print(f"  -> ERRO CRÍTICO: Não foi possível encontrar arquivos/colunas essenciais para {year}.")
        return None, None
        
    real_col = lambda map, key: map.get(key)
    col_info_curso = real_col(info_cols_map, 'CO_CURSO')
    col_info_grupo = real_col(info_cols_map, 'CO_GRUPO')
    col_info_uf = real_col(info_cols_map, 'CO_UF_CURSO')
    
    col_notas_curso = real_col(notas_cols_map, 'CO_CURSO')
    col_notas_res_ce = real_col(notas_cols_map, 'DS_VT_ACE_OCE')
    col_notas_res_fg = real_col(notas_cols_map, 'DS_VT_ACE_OFG')
    
    real_disc_cols_ce = [notas_cols_map[std] for std in disc_note_cols_std_ce if std in notas_cols_map]
    real_disc_cols_fg = [notas_cols_map[std] for std in disc_note_cols_std_fg if std in notas_cols_map]
    
    if not all([col_info_curso, col_info_grupo, col_info_uf, col_notas_curso, col_notas_res_ce, col_notas_res_fg]):
        print(f"  -> ERRO CRÍTICO: Mapeamento de colunas essenciais falhou para {year}.")
        return None, None

    try:
        # 1. Carrega df_info filtrado (para Ceará e grupos relevantes)
        print(f"  -> Lendo arquivo de info: {os.path.basename(info_file_path)}...")
        df_info = pd.read_csv(info_file_path, sep=';', encoding='latin1', low_memory=False,
                              usecols=[col_info_curso, col_info_grupo, col_info_uf])
        
        for col in [col_info_grupo, col_info_uf]:
             df_info[col] = pd.to_numeric(df_info[col], errors='coerce')
        df_info[col_info_curso] = pd.to_numeric(df_info[col_info_curso], errors='coerce')
        df_info.dropna(subset=[col_info_curso, col_info_grupo, col_info_uf], inplace=True)
        
        for col in [col_info_grupo, col_info_uf]:
             df_info[col] = df_info[col].astype(int)
        df_info[col_info_curso] = df_info[col_info_curso].astype('Int64')

        # === APLICA OS DOIS FILTROS ===
        df_info_uf_ceara = df_info[df_info[col_info_uf] == 23] # Filtro UF Ceará
        df_info_filtered = df_info_uf_ceara[df_info_uf_ceara[col_info_grupo].isin(relevant_grupos)]
        
        df_info_map = df_info_filtered.rename(columns={
            col_info_curso: 'CO_CURSO',
            col_info_grupo: 'CO_GRUPO'
        })
        df_info_map = df_info_map.drop_duplicates(subset=['CO_CURSO'], keep='first')[['CO_CURSO', 'CO_GRUPO']]
        
        relevant_cursos_uf_ceara = df_info_map['CO_CURSO'].unique().tolist()
        if not relevant_cursos_uf_ceara:
             print(f"  -> Aviso: Nenhum curso relevante encontrado para UF 23 em {year}.")
             return None, None

        curso_para_grupo_map = pd.Series(df_info_map.CO_GRUPO.astype(str).values, index=df_info_map.CO_CURSO).to_dict()

        # 2. Processa df_notas em chunks
        chunk_size = 500000 
        results_agg_ce = defaultdict(lambda: defaultdict(lambda: {'obj_acertos': 0, 'obj_validas': 0, 'disc_soma': 0.0, 'disc_cont': 0}))
        results_agg_fg = defaultdict(lambda: {'obj_acertos': 0, 'obj_validas': 0, 'disc_soma': 0.0, 'disc_cont': 0})
        
        cols_to_read_notas = [col_notas_curso, col_notas_res_ce, col_notas_res_fg] + real_disc_cols_ce + real_disc_cols_fg
        
        print(f"  -> Lendo {os.path.basename(notas_file_path)} em chunks (filtrando para {len(relevant_cursos_uf_ceara)} cursos da UF)...")
        reader = pd.read_csv(
            notas_file_path, sep=';', encoding='latin1', low_memory=False, 
            usecols=cols_to_read_notas, iterator=True, chunksize=chunk_size
        )

        for chunk in tqdm(reader, desc=f"Processando Chunks {year} UF"):
            # Renomeia colunas do chunk para nomes padrão
            chunk_rename_map = {
                col_notas_curso: 'CO_CURSO',
                col_notas_res_ce: 'DS_VT_ACE_OCE',
                col_notas_res_fg: 'DS_VT_ACE_OFG',
                **{real: std for std, real in notas_cols_map.items() if std.startswith('NT_')}
            }
            chunk.rename(columns=chunk_rename_map, inplace=True, errors='ignore')

            chunk['CO_CURSO'] = pd.to_numeric(chunk['CO_CURSO'], errors='coerce').astype('Int64')
            chunk.dropna(subset=['CO_CURSO'], inplace=True)
            
            chunk_filtered = chunk[chunk['CO_CURSO'].isin(relevant_cursos_uf_ceara)].copy()
            if chunk_filtered.empty: continue
            
            chunk_filtered['CO_GRUPO_str'] = chunk_filtered['CO_CURSO'].map(curso_para_grupo_map)
            chunk_filtered.dropna(subset=['CO_GRUPO_str'], inplace=True)
            
            for col in disc_note_cols_std_ce + disc_note_cols_std_fg:
                if col in chunk_filtered.columns:
                    if chunk_filtered[col].dtype == 'object':
                        chunk_filtered.loc[:, col] = chunk_filtered[col].str.replace(',', '.', regex=False)
                    chunk_filtered.loc[:, col] = pd.to_numeric(chunk_filtered[col], errors='coerce')

            # Carrega mapeamento FG do ano
            map_fg_ano_obj, map_fg_ano_disc, lista_componentes_fg = {}, {}, []
            if map_competencias_fg:
                map_ano_fg_data = next((item for item in map_competencias_fg if str(item.get("ANO")) == str(year)), None)
                if map_ano_fg_data:
                    lista_componentes_fg = map_ano_fg_data.get("Formacao_geral", [])
                    map_fg_ano_obj = map_ano_fg_data.get("questoes", {}).get("objetivas", {})
                    map_fg_ano_disc = map_ano_fg_data.get("questoes", {}).get("discursivas", {})

            for index, row in chunk_filtered.iterrows():
                 co_grupo_str = row['CO_GRUPO_str']
                 map_grupo_ce = map_competencias_ce.get(co_grupo_str, {})
                 lista_componentes_ce = map_grupo_ce.get('Componente_especifico', [])
                 map_ano_ce = map_grupo_ce.get('Anos', {}).get(str(year), {})
                 questoes_ce = map_ano_ce.get('questoes_CE', {})
                 map_obj_ce = questoes_ce.get('objetivas', {})
                 map_disc_ce = questoes_ce.get('discursivas', {})
                 
                 # Processa CE
                 respostas_obj_ce = str(row['DS_VT_ACE_OCE']) if pd.notna(row['DS_VT_ACE_OCE']) else ''
                 if len(respostas_obj_ce) >= 27:
                     for q_key, mapeamento in map_obj_ce.items():
                         try:
                             q_index = int(q_key[1:]) - 9
                             indices = mapeamento if isinstance(mapeamento, list) else [mapeamento]
                             for idx_1 in indices:
                                 idx_0 = int(idx_1) - 1
                                 if 0 <= idx_0 < len(lista_componentes_ce) and 0 <= q_index < len(respostas_obj_ce):
                                     comp = lista_componentes_ce[idx_0]
                                     resp = respostas_obj_ce[q_index]
                                     if resp in ['0', '1']:
                                         results_agg_ce[co_grupo_str][comp]['obj_validas'] += 1
                                         if resp == '1':
                                             results_agg_ce[co_grupo_str][comp]['obj_acertos'] += 1
                         except: continue
                 for d_key, mapeamento in map_disc_ce.items():
                     try:
                         suffix = int(d_key[1:]) - 2
                         col_name = f"NT_CE_D{suffix}"
                         if col_name in row:
                             indices = mapeamento if isinstance(mapeamento, list) else [mapeamento]
                             for idx_1 in indices:
                                 idx_0 = int(idx_1) - 1
                                 if 0 <= idx_0 < len(lista_componentes_ce):
                                     comp = lista_componentes_ce[idx_0]
                                     nota = row[col_name]
                                     if pd.notna(nota):
                                         results_agg_ce[co_grupo_str][comp]['disc_soma'] += nota
                                         results_agg_ce[co_grupo_str][comp]['disc_cont'] += 1
                     except: continue
                
                 # Processa FG
                 if map_ano_fg_data:
                    respostas_obj_fg = str(row['DS_VT_ACE_OFG']) if pd.notna(row['DS_VT_ACE_OFG']) else ''
                    if len(respostas_obj_fg) >= 8:
                        for q_key, mapeamento in map_fg_ano_obj.items():
                            try:
                                q_index = int(q_key[1:]) - 1
                                indices = mapeamento if isinstance(mapeamento, list) else [mapeamento]
                                for idx_1 in indices:
                                    idx_0 = int(idx_1) - 1
                                    if 0 <= idx_0 < len(lista_componentes_fg) and 0 <= q_index < len(respostas_obj_fg):
                                        comp = lista_componentes_fg[idx_0]
                                        resp = respostas_obj_fg[q_index]
                                        if resp in ['0', '1']:
                                            results_agg_fg[comp]['obj_validas'] += 1
                                            if resp == '1':
                                                results_agg_fg[comp]['obj_acertos'] += 1
                            except: continue
                    for d_key, mapeamento in map_fg_ano_disc.items():
                        try:
                            suffix = int(d_key[1:])
                            col_name = f"NT_FG_D{suffix}"
                            if col_name in row:
                                indices = mapeamento if isinstance(mapeamento, list) else [mapeamento]
                                for idx_1 in indices:
                                    idx_0 = int(idx_1) - 1
                                    if 0 <= idx_0 < len(lista_componentes_fg):
                                        comp = lista_componentes_fg[idx_0]
                                        nota = row[col_name]
                                        if pd.notna(nota):
                                            results_agg_fg[comp]['disc_soma'] += nota
                                            results_agg_fg[comp]['disc_cont'] += 1
                        except: continue

        # 3. Calcula as médias finais
        final_means_ce = {}
        for grupo, comps in results_agg_ce.items():
            final_means_ce[grupo] = {}
            for comp, data in comps.items():
                percentual_obj = (data['obj_acertos'] / data['obj_validas'] * 100) if data['obj_validas'] > 0 else None
                media_disc = (data['disc_soma'] / data['disc_cont']) if data['disc_cont'] > 0 else None
                final_means_ce[grupo][comp] = {
                    "percentual_objetivas_uf": round(percentual_obj, 2) if percentual_obj is not None else None,
                    "media_discursivas_uf": round(media_disc, 2) if media_disc is not None else None,
                    "n_objetivas_validas_uf": data['obj_validas'],
                    "n_discursivas_validas_uf": data['disc_cont']
                }
        
        final_means_fg = {}
        for comp, data in results_agg_fg.items():
            percentual_obj = (data['obj_acertos'] / data['obj_validas'] * 100) if data['obj_validas'] > 0 else None
            media_disc = (data['disc_soma'] / data['disc_cont']) if data['disc_cont'] > 0 else None
            final_means_fg[comp] = {
                "percentual_objetivas_uf": round(percentual_obj, 2) if percentual_obj is not None else None,
                "media_discursivas_uf": round(media_disc, 2) if media_disc is not None else None,
                "n_objetivas_validas_uf": data['obj_validas'],
                "n_discursivas_validas_uf": data['disc_cont']
            }
        
        print(f"  -> Médias da UF (chunks) calculadas para {year}.")
        return final_means_ce, final_means_fg

    except Exception as e:
        print(f"  -> ERRO GERAL ao processar médias da UF de {year}: {e}")
        return None, None

# --- Função Main (Orquestração) ---
def main():
    relevant_grupos = get_relevant_grupos()
    map_competencias_ce = load_json(MAP_CE_JSON_PATH, "Mapeamento de Competências CE")
    map_competencias_fg = load_json(MAP_FG_JSON_PATH, "Mapeamento de Competências FG")
    
    if relevant_grupos is None or map_competencias_ce is None or map_competencias_fg is None:
        print("Encerrando script due to error loading mapping files.")
        return

    os.makedirs(MEDIAS_UF_CE_BASE_PATH, exist_ok=True)
    os.makedirs(MEDIAS_UF_FG_BASE_PATH, exist_ok=True)
    
    print(f"\nSalvando médias da UF (Ceará) em subpastas anuais...")

    for year in YEARS_TO_PROCESS:
        year_extract_path = os.path.join(RAW_DATA_PATH, f'enade_{year}')
        medias_ce_ano, medias_fg_ano = calculate_uf_averages(year, year_extract_path, relevant_grupos, map_competencias_ce, map_competencias_fg) 
        
        # Salva arquivo CE
        if medias_ce_ano:
            data_to_save_ce = {str(k): v for k, v in medias_ce_ano.items()}
            year_dir_ce = os.path.join(MEDIAS_UF_CE_BASE_PATH, str(year))
            os.makedirs(year_dir_ce, exist_ok=True)
            output_path_ce = os.path.join(year_dir_ce, 'medias_uf_ce.json') # Nome do arquivo
            try:
                with open(output_path_ce, 'w', encoding='utf-8') as f:
                    json.dump(data_to_save_ce, f, ensure_ascii=False, indent=4)
                print(f"  -> Médias CE de {year} salvas em '{output_path_ce}'")
            except Exception as e:
                print(f"  -> ERRO ao salvar médias CE de {year}: {e}")
        else:
             print(f"  -> Aviso: Não foram calculadas médias CE para {year}.")

        # Salva arquivo FG
        if medias_fg_ano:
            data_to_save_fg = {str(k): v for k, v in medias_fg_ano.items()} # FG não é por grupo, chaves já são strings
            year_dir_fg = os.path.join(MEDIAS_UF_FG_BASE_PATH, str(year))
            os.makedirs(year_dir_fg, exist_ok=True)
            output_path_fg = os.path.join(year_dir_fg, 'medias_uf_fg.json') # Nome do arquivo
            try:
                with open(output_path_fg, 'w', encoding='utf-8') as f:
                    json.dump(data_to_save_fg, f, ensure_ascii=False, indent=4)
                print(f"  -> Médias FG de {year} salvas em '{output_path_fg}'")
            except Exception as e:
                print(f"  -> ERRO ao salvar médias FG de {year}: {e}")
        else:
            print(f"  -> Aviso: Não foram calculadas médias FG para {year}.")

    print("\nProcesso de geração de médias da UF (Ceará) por ano concluído.")

if __name__ == '__main__':
    main()