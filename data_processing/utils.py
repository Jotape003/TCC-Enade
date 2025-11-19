import pandas as pd
import os
import glob
import json
from collections import defaultdict
import numpy as np
from tqdm import tqdm
from config import CURSOS_CSV_PATH

def find_data_files(year_path):
    print(f"--- Buscando arquivos em: {year_path}")
    if not os.path.exists(year_path):
        print(f"   -> ERRO: O caminho base não existe: {year_path}")
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
    if not found_files: print(f"   -> AVISO: Nenhum arquivo de dados encontrado para {year_path}.")
    return found_files


def load_json(file_path):
    if not os.path.exists(file_path):
        print(f"   -> ERRO: Arquivo não encontrado em: {file_path}")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"   -> ERRO ao carregar JSON: {e}")
        return None


def find_required_columns(file_path, required_cols_variants):
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


def save_json_safe(data, output_path, description):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"   -> {description} salvos em '{output_path}'")
    except Exception as e:
        print(f"   -> ERRO ao salvar {description}: {e}")


def get_relevant_grupos():
    if not os.path.exists(CURSOS_CSV_PATH):
        print(f"ERRO: Arquivo '{CURSOS_CSV_PATH}' não encontrado.")
        return None
    try:
        df_cursos = pd.read_csv(CURSOS_CSV_PATH, sep=';', usecols=['CO_GRUPO'])
        relevant_grupos = df_cursos['CO_GRUPO'].dropna().unique().tolist()
        relevant_grupos = [int(g) for g in relevant_grupos]
        print(f"CO_GRUPOs relevantes (base UFC): {relevant_grupos}")
        return relevant_grupos
    except Exception as e:
        print(f"Erro ao ler CO_GRUPOs do arquivo de cursos: {e}")
        return None


def get_filtered_student_map_from_microdados(all_raw_files, info_cols, filter_col, filter_val, relevant_grupos):
    info_file_path, info_cols_map = None, None
    
    for file in all_raw_files:
        found_map = find_required_columns(file, info_cols)
        if found_map:
            info_file_path, info_cols_map = file, found_map
            print(f"     -> Arquivo de Info encontrado: {os.path.basename(info_file_path)}")
            break
            
    if not info_file_path:
        print(f"   -> ERRO CRÍTICO: Não foi possível encontrar arquivo de info.")
        return None, None

    real_col = lambda key: info_cols_map.get(key)
    col_info_curso = real_col('CO_CURSO')
    col_info_grupo = real_col('CO_GRUPO')
    col_filter_real = real_col(filter_col)
    
    usecols_info = [col_info_curso, col_info_grupo]
    if col_filter_real:
        usecols_info.append(col_filter_real)

    try:
        df_info = pd.read_csv(info_file_path, sep=';', encoding='latin1', low_memory=False, usecols=usecols_info)
        
        df_info[col_info_curso] = pd.to_numeric(df_info[col_info_curso], errors='coerce')
        df_info[col_info_grupo] = pd.to_numeric(df_info[col_info_grupo], errors='coerce')
        if col_filter_real:
            df_info[col_filter_real] = pd.to_numeric(df_info[col_filter_real], errors='coerce')

        df_info.dropna(subset=[col_info_curso, col_info_grupo], inplace=True)
        
        if col_filter_real and filter_val is not None:
            df_info_filtered_geo = df_info[df_info[col_filter_real] == filter_val]
        else:
            df_info_filtered_geo = df_info

        df_info_filtered = df_info_filtered_geo[df_info_filtered_geo[col_info_grupo].isin(relevant_grupos)]

        df_info_map = df_info_filtered.rename(columns={
            col_info_curso: 'CO_CURSO',
            col_info_grupo: 'CO_GRUPO'
        })
        df_info_map = df_info_map.drop_duplicates(subset=['CO_CURSO'], keep='first')[['CO_CURSO', 'CO_GRUPO']]
        
        relevant_cursos_list = df_info_map['CO_CURSO'].astype('Int64').unique().tolist()
        curso_para_grupo_map = pd.Series(df_info_map.CO_GRUPO.astype(int).astype(str).values, index=df_info_map.CO_CURSO).to_dict()

        return curso_para_grupo_map, relevant_cursos_list

    except Exception as e:
        print(f"   -> ERRO ao ler e filtrar arquivo de info: {e}")
        return None, None


def get_curso_info_map_from_csv():
    if not os.path.exists(CURSOS_CSV_PATH):
        print(f"ERRO: Arquivo '{CURSOS_CSV_PATH}' não encontrado.")
        return None, None
    try:
        df_cursos = pd.read_csv(CURSOS_CSV_PATH, sep=';', usecols=['Código', 'CO_GRUPO']) 
        df_cursos.rename(columns={'Código': 'CO_CURSO'}, inplace=True)
        df_cursos.dropna(subset=['CO_CURSO', 'CO_GRUPO'], inplace=True)
        
        df_cursos['CO_CURSO'] = pd.to_numeric(df_cursos['CO_CURSO'], errors='coerce').astype('Int64')
        df_cursos['CO_GRUPO'] = pd.to_numeric(df_cursos['CO_GRUPO'], errors='coerce').astype(int).astype(str)
        df_cursos.dropna(subset=['CO_CURSO', 'CO_GRUPO'], inplace=True)

        relevant_cursos_map = pd.Series(df_cursos.CO_GRUPO.values, index=df_cursos.CO_CURSO).to_dict()
        relevant_cursos_list = list(relevant_cursos_map.keys())
        
        print(f"Encontrados {len(relevant_cursos_list)} cursos relevantes (base UFC).")
        return relevant_cursos_map, relevant_cursos_list
    except Exception as e:
        print(f"Erro ao ler CO_CURSOs do arquivo de cursos: {e}")
        return None, None


def calculate_averages_competencia(config):
    year = config['year']
    year_path = config['year_path']
    maps = config['maps']
    json_suffix = config['json_suffix']
    
    print(f"\nCalculando médias para [ {json_suffix.upper()} ] de {year}...")
    
    all_raw_files = find_data_files(year_path)
    if not all_raw_files: 
        return None, None

    info_cols = {
        'CO_CURSO': ['CO_CURSO', '"CO_CURSO"'],
        'CO_GRUPO': ['CO_GRUPO', '"CO_GRUPO"'],
    }
    if config.get('filter_col'):
        info_cols[config['filter_col']] = config['info_col_variants']

    notas_cols = {
        'CO_CURSO': ['CO_CURSO', '"CO_CURSO"'],
        'DS_VT_ACE_OCE': ['DS_VT_ACE_OCE', '"DS_VT_ACE_OCE"'],
        'DS_VT_ACE_OFG': ['DS_VT_ACE_OFG', '"DS_VT_ACE_OFG"']
    }
    disc_note_cols_std_ce = [f'NT_CE_D{i}' for i in range(1, 6)]
    disc_note_cols_std_fg = [f'NT_FG_D{i}' for i in range(1, 3)]

    if config['group_by_curso']:
        curso_para_grupo_map = config['curso_info_map']
        relevant_cursos_list = config['relevant_cursos_list']
    else:
        curso_para_grupo_map, relevant_cursos_list = get_filtered_student_map_from_microdados(
            all_raw_files, info_cols, 
            config['filter_col'], config['filter_val'], 
            config['relevant_grupos']
        )
    
    if not relevant_cursos_list or not curso_para_grupo_map:
        print(f"   -> Aviso: Nenhum curso relevante encontrado para [ {json_suffix.upper()} ] em {year}.")
        return None, None

    notas_file_path, notas_cols_map = None, None
    for file in all_raw_files:
        if 'arq3' in os.path.basename(file).lower():
            found_map = find_required_columns(file, notas_cols)
            if found_map:
                df_header_notas = pd.read_csv(file, sep=';', encoding='latin1', nrows=5)
                for std_col in disc_note_cols_std_ce + disc_note_cols_std_fg:
                    match = next((col for col in df_header_notas.columns if col.upper() == std_col), None)
                    if match: found_map[std_col] = match
                notas_file_path, notas_cols_map = file, found_map
                print(f"     -> Arquivo de Notas encontrado: {os.path.basename(notas_file_path)}")
                break
                
    if not notas_file_path:
        print(f"   -> ERRO CRÍTICO: Não foi possível encontrar arquivo/colunas de Notas para {year}.")
        return None, None

    if config['group_by_curso']:
        results_agg_ce = defaultdict(lambda: defaultdict(lambda: {'obj_acertos': 0, 'obj_validas': 0, 'disc_soma': 0.0, 'disc_cont': 0}))
        results_agg_fg = defaultdict(lambda: defaultdict(lambda: {'obj_acertos': 0, 'obj_validas': 0, 'disc_soma': 0.0, 'disc_cont': 0}))
    else:
        results_agg_ce = defaultdict(lambda: defaultdict(lambda: {'obj_acertos': 0, 'obj_validas': 0, 'disc_soma': 0.0, 'disc_cont': 0}))
        results_agg_fg = defaultdict(lambda: {'obj_acertos': 0, 'obj_validas': 0, 'disc_soma': 0.0, 'disc_cont': 0})
        
    try:
        col_notas_curso = notas_cols_map.get('CO_CURSO')
        col_notas_res_ce = notas_cols_map.get('DS_VT_ACE_OCE')
        col_notas_res_fg = notas_cols_map.get('DS_VT_ACE_OFG')
        
        cols_to_read_notas = [col_notas_curso, col_notas_res_ce, col_notas_res_fg] + \
                             [notas_cols_map[std] for std in disc_note_cols_std_ce if std in notas_cols_map] + \
                             [notas_cols_map[std] for std in disc_note_cols_std_fg if std in notas_cols_map]
        
        print(f"   -> Lendo {os.path.basename(notas_file_path)} em chunks (filtrando para {len(relevant_cursos_list)} cursos)...")
        reader = pd.read_csv(
            notas_file_path, sep=';', encoding='latin1', low_memory=False, 
            usecols=cols_to_read_notas, iterator=True, chunksize=500000
        )

        for chunk in tqdm(reader, desc=f"Processando Chunks {year} [{json_suffix.upper()}]"):
            chunk_rename_map = {
                col_notas_curso: 'CO_CURSO',
                col_notas_res_ce: 'DS_VT_ACE_OCE',
                col_notas_res_fg: 'DS_VT_ACE_OFG',
                **{real: std for std, real in notas_cols_map.items() if std.startswith('NT_')}
            }
            chunk.rename(columns=chunk_rename_map, inplace=True, errors='ignore')

            chunk['CO_CURSO'] = pd.to_numeric(chunk['CO_CURSO'], errors='coerce').astype('Int64')
            chunk.dropna(subset=['CO_CURSO'], inplace=True)
            
            chunk_filtered = chunk[chunk['CO_CURSO'].isin(relevant_cursos_list)].copy()
            if chunk_filtered.empty: continue
            
            chunk_filtered['CO_GRUPO_str'] = chunk_filtered['CO_CURSO'].map(curso_para_grupo_map)
            chunk_filtered.dropna(subset=['CO_GRUPO_str'], inplace=True)
            
            for col in disc_note_cols_std_ce + disc_note_cols_std_fg:
                if col in chunk_filtered.columns:
                    if chunk_filtered[col].dtype == 'object':
                        chunk_filtered.loc[:, col] = chunk_filtered[col].str.replace(',', '.', regex=False)
                    chunk_filtered.loc[:, col] = pd.to_numeric(chunk_filtered[col], errors='coerce')

            map_fg_ano_obj, map_fg_ano_disc, lista_componentes_fg = {}, {}, []
            map_ano_fg_data = next((item for item in maps['fg'] if str(item.get("ANO")) == str(year)), None)
            if map_ano_fg_data:
                lista_componentes_fg = map_ano_fg_data.get("Formacao_geral", [])
                map_fg_ano_obj = map_ano_fg_data.get("questoes", {}).get("objetivas", {})
                map_fg_ano_disc = map_ano_fg_data.get("questoes", {}).get("discursivas", {})

            for index, row in chunk_filtered.iterrows():
                co_grupo_str = row['CO_GRUPO_str']
                map_grupo_ce = maps['ce'].get(co_grupo_str, {})
                lista_componentes_ce = map_grupo_ce.get('Componente_especifico', [])
                map_ano_ce = map_grupo_ce.get('Anos', {}).get(str(year), {})
                questoes_ce = map_ano_ce.get('questoes_CE', {})
                map_obj_ce = questoes_ce.get('objetivas', {})
                map_disc_ce = questoes_ce.get('discursivas', {})
                
                if config['group_by_curso']:
                    agg_key = row['CO_CURSO']
                else:
                    agg_key = co_grupo_str
                
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
                                        results_agg_ce[agg_key][comp]['obj_validas'] += 1
                                        if resp == '1':
                                            results_agg_ce[agg_key][comp]['obj_acertos'] += 1
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
                                        results_agg_ce[agg_key][comp]['disc_soma'] += nota
                                        results_agg_ce[agg_key][comp]['disc_cont'] += 1
                    except: continue
                
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
                                            if config['group_by_curso']:
                                                results_agg_fg[agg_key][comp]['obj_validas'] += 1
                                                if resp == '1': results_agg_fg[agg_key][comp]['obj_acertos'] += 1
                                            else:
                                                results_agg_fg[comp]['obj_validas'] += 1
                                                if resp == '1': results_agg_fg[comp]['obj_acertos'] += 1
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
                                            if config['group_by_curso']:
                                                results_agg_fg[agg_key][comp]['disc_soma'] += nota
                                                results_agg_fg[agg_key][comp]['disc_cont'] += 1
                                            else:
                                                results_agg_fg[comp]['disc_soma'] += nota
                                                results_agg_fg[comp]['disc_cont'] += 1
                        except: continue

        final_means_ce = {}
        for key, comps in results_agg_ce.items():
            final_means_ce[str(key)] = {}
            for comp, data in comps.items():
                perc_obj = (data['obj_acertos'] / data['obj_validas'] * 100) if data['obj_validas'] > 0 else None
                media_disc = (data['disc_soma'] / data['disc_cont']) if data['disc_cont'] > 0 else None
                final_means_ce[str(key)][comp] = {
                    f"percentual_objetivas_{json_suffix}": round(perc_obj, 2) if perc_obj is not None else None,
                    f"media_discursivas_{json_suffix}": round(media_disc, 2) if media_disc is not None else None,
                    f"n_objetivas_validas_{json_suffix}": data['obj_validas'],
                    f"n_discursivas_validas_{json_suffix}": data['disc_cont']
                }
        
        final_means_fg = {}
        if config['group_by_curso']:
             for key, comps in results_agg_fg.items():
                final_means_fg[str(key)] = {}
                for comp, data in comps.items():
                    perc_obj = (data['obj_acertos'] / data['obj_validas'] * 100) if data['obj_validas'] > 0 else None
                    media_disc = (data['disc_soma'] / data['disc_cont']) if data['disc_cont'] > 0 else None
                    final_means_fg[str(key)][comp] = {
                        f"percentual_objetivas_{json_suffix}": round(perc_obj, 2) if perc_obj is not None else None,
                        f"media_discursivas_{json_suffix}": round(media_disc, 2) if media_disc is not None else None,
                        f"n_objetivas_validas_{json_suffix}": data['obj_validas'],
                        f"n_discursivas_validas_{json_suffix}": data['disc_cont']
                    }
        else:
            for comp, data in results_agg_fg.items():
                perc_obj = (data['obj_acertos'] / data['obj_validas'] * 100) if data['obj_validas'] > 0 else None
                media_disc = (data['disc_soma'] / data['disc_cont']) if data['disc_cont'] > 0 else None
                final_means_fg[comp] = {
                    f"percentual_objetivas_{json_suffix}": round(perc_obj, 2) if perc_obj is not None else None,
                    f"media_discursivas_{json_suffix}": round(media_disc, 2) if media_disc is not None else None,
                    f"n_objetivas_validas_{json_suffix}": data['obj_validas'],
                    f"n_discursivas_validas_{json_suffix}": data['disc_cont']
                }
        
        print(f"   -> Médias [ {json_suffix.upper()} ] (chunks) calculadas para {year}.")
        return final_means_ce, final_means_fg

    except Exception as e:
        print(f"   -> ERRO GERAL ao processar médias [ {json_suffix.upper()} ] de {year}: {e}")
        return None, None