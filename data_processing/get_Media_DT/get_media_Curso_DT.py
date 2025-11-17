import pandas as pd
import os
import glob
import json
from collections import defaultdict
import numpy as np

from config import (
    PROCESSED_DATA_PATH, YEARS_TO_PROCESS, FINAL_MEDIA_JSON_PATH, 
    FINAL_ESTRUTURA_JSON_PATH
)

from .utils import (
    load_json, get_curso_info_map_from_csv, save_json_safe
)

MAP_CE_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_competencias_final.json')
MAP_FG_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_fg_final.json')

BASE_CE_OUTPUT_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'CE', 'Medias_Curso')
BASE_FG_OUTPUT_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'FG', 'Medias_Curso')


def calculate_and_save_results(base_path, campus_name, year, results_dict, suffix):
    final_data = {}
    for curso_id, comps in results_dict.items():
        final_data[str(curso_id)] = {}
        for comp, data in comps.items():
            obj_pct = (data['obj_acertos'] / data['obj_validas'] * 100) if data['obj_validas'] > 0 else None
            disc_med = (data['disc_soma'] / data['disc_cont']) if data['disc_cont'] > 0 else None
            final_data[str(curso_id)][comp] = {
                "percentual_objetivas_curso": round(obj_pct, 2) if obj_pct is not None else None,
                "media_discursivas_curso": round(disc_med, 2) if disc_med is not None else None,
                "n_objetivas_validas_curso": data['obj_validas'],
                "n_discursivas_validas_curso": data['disc_cont']
            }
            
    if final_data:
        output_dir = os.path.join(base_path, campus_name, str(year))
        output_path = os.path.join(output_dir, f"medias_curso_{suffix}.json")
        save_json_safe(final_data, output_path, f"Médias ({suffix.upper()}) {campus_name} {year}")
    else:
        print(f"       -> Sem dados ({suffix.upper()}) para {campus_name} {year}")

def run_calculation_curso():
    print("--- INICIANDO: Calculando Médias de Competência por CURSO (CE e FG) ---")
    
    map_competencias_ce = load_json(MAP_CE_JSON_PATH, "Mapeamento de Competências CE")
    map_competencias_fg = load_json(MAP_FG_JSON_PATH, "Mapeamento de Competências FG")
    curso_grupo_map, _ = get_curso_info_map_from_csv() 

    if not all([map_competencias_ce, map_competencias_fg, curso_grupo_map]):
        print("Encerrando script devido a erro no carregamento dos arquivos de mapeamento.")
        return

    for year in YEARS_TO_PROCESS:
        print(f"\n=== Processando Ano: {year} ===")
        ano_str = str(year)

        map_fg_ano_obj, map_fg_ano_disc, lista_componentes_fg = {}, {}, []
        map_ano_fg_data = next((item for item in map_competencias_fg if str(item.get("ANO")) == ano_str), None)
        if map_ano_fg_data:
            lista_componentes_fg = map_ano_fg_data.get("Formacao_geral", [])
            map_fg_ano_obj = map_ano_fg_data.get("questoes", {}).get("objetivas", {})
            map_fg_ano_disc = map_ano_fg_data.get("questoes", {}).get("discursivas", {})
        else:
            print(f"   -> Aviso: Mapeamento de FG para {year} não encontrado.")

        try:
            campus_folders = [d for d in os.listdir(PROCESSED_DATA_PATH) if os.path.isdir(os.path.join(PROCESSED_DATA_PATH, d))]
        except FileNotFoundError:
            print(f"   -> ERRO CRÍTICO: O diretório de dados processados não foi encontrado: {PROCESSED_DATA_PATH}")
            continue

        for campus_name in campus_folders:
            print(f"\n   >> Processando Campus: {campus_name}")

            campus_year_path = os.path.join(PROCESSED_DATA_PATH, campus_name, ano_str)
            if not os.path.exists(campus_year_path):
                print(f"     -> Pasta do ano {year} não encontrada para o campus {campus_name}. Pulando.")
                continue

            notas_file_path_list = glob.glob(os.path.join(campus_year_path, '*arq3.csv'))
            if not notas_file_path_list:
                print(f"     -> Arquivo *arq3.csv não encontrado em {campus_year_path}. Pulando.")
                continue
            
            notas_file_path = notas_file_path_list[0]

            try:
                df_notas = pd.read_csv(notas_file_path, sep=';', encoding='utf-8', low_memory=False)
                df_notas.columns = [col.upper() for col in df_notas.columns]
                
                df_notas['CO_CURSO'] = pd.to_numeric(df_notas['CO_CURSO'], errors='coerce').astype('Int64')
                df_notas = df_notas.dropna(subset=['CO_CURSO'])

                disc_cols = [col for col in df_notas.columns if col.startswith(('NT_CE_D', 'NT_FG_D'))]
                for col in disc_cols:
                    if df_notas[col].dtype == 'object':
                        df_notas[col] = df_notas[col].str.replace(',', '.', regex=False)
                    df_notas[col] = pd.to_numeric(df_notas[col], errors='coerce')
                
                results_curso_agg_ce = defaultdict(lambda: defaultdict(lambda: {'obj_acertos': 0, 'obj_validas': 0, 'disc_soma': 0.0, 'disc_cont': 0}))
                results_curso_agg_fg = defaultdict(lambda: defaultdict(lambda: {'obj_acertos': 0, 'obj_validas': 0, 'disc_soma': 0.0, 'disc_cont': 0}))

                for _, row in df_notas.iterrows():
                    curso_id = row['CO_CURSO']
                    co_grupo_str = curso_grupo_map.get(curso_id)

                    if co_grupo_str and co_grupo_str in map_competencias_ce:
                        map_grupo = map_competencias_ce[co_grupo_str]
                        lista_componentes_ce = map_grupo.get('Componente_especifico', [])
                        map_ano_ce = map_grupo.get('Anos', {}).get(ano_str, {})
                        questoes_ce = map_ano_ce.get('questoes_CE', {})
                        map_obj_ce = questoes_ce.get('objetivas', {})
                        map_disc_ce = questoes_ce.get('discursivas', {})

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
                                                results_curso_agg_ce[curso_id][comp]['obj_validas'] += 1
                                                if resp == '1':
                                                    results_curso_agg_ce[curso_id][comp]['obj_acertos'] += 1
                                except Exception:
                                    continue 

                        for d_key, mapeamento in map_disc_ce.items():
                            try:
                                suffix = int(d_key[1:]) - 2
                                col_name = f"NT_CE_D{suffix}"
                                indices = mapeamento if isinstance(mapeamento, list) else [mapeamento]
                                for idx_1 in indices:
                                    idx_0 = int(idx_1) - 1
                                    if 0 <= idx_0 < len(lista_componentes_ce):
                                        comp = lista_componentes_ce[idx_0]
                                        nota = row.get(col_name)
                                        if pd.notna(nota):
                                            results_curso_agg_ce[curso_id][comp]['disc_soma'] += nota
                                            results_curso_agg_ce[curso_id][comp]['disc_cont'] += 1
                            except Exception:
                                continue

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
                                                results_curso_agg_fg[curso_id][comp]['obj_validas'] += 1
                                                if resp == '1':
                                                    results_curso_agg_fg[curso_id][comp]['obj_acertos'] += 1
                                except Exception:
                                    continue

                        for d_key, mapeamento in map_fg_ano_disc.items():
                            try:
                                suffix = int(d_key[1:])
                                col_name = f"NT_FG_D{suffix}"
                                indices = mapeamento if isinstance(mapeamento, list) else [mapeamento]
                                for idx_1 in indices:
                                    idx_0 = int(idx_1) - 1
                                    if 0 <= idx_0 < len(lista_componentes_fg):
                                        comp = lista_componentes_fg[idx_0]
                                        nota = row.get(col_name)
                                        if pd.notna(nota):
                                            results_curso_agg_fg[curso_id][comp]['disc_soma'] += nota
                                            results_curso_agg_fg[curso_id][comp]['disc_cont'] += 1
                            except Exception:
                                continue

                calculate_and_save_results(BASE_CE_OUTPUT_PATH, campus_name, year, results_curso_agg_ce, "ce")
                calculate_and_save_results(BASE_FG_OUTPUT_PATH, campus_name, year, results_curso_agg_fg, "fg")

            except Exception as e:
                print(f"   -> ERRO GERAL ao processar o arquivo {notas_file_path}: {e}")
    
    print("\n--- Cálculo de Médias por CURSO (CE e FG) Concluído ---")

if __name__ == '__main__':
    run_calculation_curso()