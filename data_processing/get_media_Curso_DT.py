import pandas as pd
import os
import glob
import json
from collections import defaultdict
import numpy as np
from tqdm import tqdm

from config import PROCESSED_DATA_PATH, YEARS_TO_PROCESS, FINAL_JSON_PATH, FINAL_MEDIA_JSON_PATH, FINAL_ESTRUTURA_JSON_PATH

MAP_CE_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_competencias_final.json')
MAP_FG_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_fg_final.json')
CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv')

MEDIAS_CURSO_CE_BASE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'CE' , 'Medias_Curso')
MEDIAS_CURSO_FG_BASE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'FG', 'Medias_Curso')

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

def load_curso_grupo_map():
    print(f"Carregando mapa CO_CURSO -> CO_GRUPO de '{os.path.basename(CURSOS_CSV_PATH)}'...")
    if not os.path.exists(CURSOS_CSV_PATH):
        print("  -> ERRO: Arquivo CSV de cursos não encontrado.")
        return None
    try:
        df_cursos = pd.read_csv(CURSOS_CSV_PATH, sep=';', usecols=['Código', 'CO_GRUPO']) 

        df_cursos.columns = ['CO_CURSO', 'CO_GRUPO']
        df_cursos = df_cursos.dropna(subset=['CO_CURSO', 'CO_GRUPO'])
        df_cursos['CO_CURSO'] = pd.to_numeric(df_cursos['CO_CURSO'], errors='coerce').astype('Int64')
        df_cursos['CO_GRUPO'] = pd.to_numeric(df_cursos['CO_GRUPO'], errors='coerce').astype('Int64')
        df_cursos = df_cursos.drop_duplicates(subset=['CO_CURSO'], keep='first')
        mapa = pd.Series(df_cursos.CO_GRUPO.astype(str).values, index=df_cursos.CO_CURSO).to_dict()
        print(f"  -> Mapa CO_CURSO -> CO_GRUPO carregado para {len(mapa)} cursos.")
        return mapa
    except Exception as e:
         print(f"  -> Erro ao ler mapa de cursos: {e}")
         return None

def main():
    print("--- INICIANDO: Calculando Médias de Competência por CURSO (CE e FG) ---")
    map_competencias_ce = load_json(MAP_CE_JSON_PATH, "Mapeamento de Competências CE")
    map_competencias_fg = load_json(MAP_FG_JSON_PATH, "Mapeamento de Competências FG")
    curso_grupo_map = load_curso_grupo_map()

    if not all([map_competencias_ce, map_competencias_fg, curso_grupo_map]):
        print("Encerrando script devido a erro no carregamento dos arquivos de mapeamento.")
        return

    os.makedirs(MEDIAS_CURSO_CE_BASE_PATH, exist_ok=True)
    os.makedirs(MEDIAS_CURSO_FG_BASE_PATH, exist_ok=True)

    for year in YEARS_TO_PROCESS:
        print(f"\n=== Processando Ano: {year} ===")

        map_fg_ano_obj, map_fg_ano_disc, lista_componentes_fg = {}, {}, []
        map_ano_fg_data = next((item for item in map_competencias_fg if str(item.get("ANO")) == str(year)), None)
        if map_ano_fg_data:
            lista_componentes_fg = map_ano_fg_data.get("Formacao_geral", [])
            map_fg_ano_obj = map_ano_fg_data.get("questoes", {}).get("objetivas", {})
            map_fg_ano_disc = map_ano_fg_data.get("questoes", {}).get("discursivas", {})
        else:
            print(f"  -> Aviso: Mapeamento de FG para {year} não encontrado.")

        campus_folders = [d for d in os.listdir(PROCESSED_DATA_PATH) if os.path.isdir(os.path.join(PROCESSED_DATA_PATH, d))]

        for campus_name in campus_folders:
            print(f"\n  >> Campus: {campus_name}")

            campus_year_path = os.path.join(PROCESSED_DATA_PATH, campus_name, str(year))
            if not os.path.exists(campus_year_path):
                continue

            notas_file_path = glob.glob(os.path.join(campus_year_path, '*arq3.csv'))
            if not notas_file_path:
                continue

            try:
                df_notas = pd.read_csv(notas_file_path[0], sep=';', encoding='utf-8', low_memory=False)
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
                        map_ano_ce = map_grupo.get('Anos', {}).get(str(year), {})
                        questoes_ce = map_ano_ce.get('questoes_CE', {})
                        map_obj_ce = questoes_ce.get('objetivas', {})
                        map_disc_ce = questoes_ce.get('discursivas', {})

                        respostas_obj_ce = str(row['DS_VT_ACE_OCE']) if pd.notna(row['DS_VT_ACE_OCE']) else ''
                        if len(respostas_obj_ce) >= 27:
                            for q_key, mapeamento in map_obj_ce.items():
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

                        for d_key, mapeamento in map_disc_ce.items():
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

                    if map_ano_fg_data:
                        respostas_obj_fg = str(row['DS_VT_ACE_OFG']) if pd.notna(row['DS_VT_ACE_OFG']) else ''
                        if len(respostas_obj_fg) >= 8:
                            for q_key, mapeamento in map_fg_ano_obj.items():
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

                        for d_key, mapeamento in map_fg_ano_disc.items():
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

                def save_results(base_path, prefix, results_dict):
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
                        os.makedirs(output_dir, exist_ok=True)
                        output_path = os.path.join(output_dir, f"medias_curso_{prefix}.json")
                        with open(output_path, 'w', encoding='utf-8') as f:
                            json.dump(final_data, f, ensure_ascii=False, indent=4)
                        print(f"      -> Médias ({prefix}) salvas em {output_path}")

                save_results(MEDIAS_CURSO_CE_BASE_PATH, "ce", results_curso_agg_ce)
                save_results(MEDIAS_CURSO_FG_BASE_PATH, "fg", results_curso_agg_fg)

            except Exception as e:
                print(f"  -> ERRO ao processar {campus_name} ({year}): {e}")

    
    print("  -> Calculando e salvando médias finais por CURSO (FG)...")
    final_curso_averages_fg = {}
    for curso_id, comps in results_curso_agg_fg.items():
        curso_id_str = str(curso_id)
        final_curso_averages_fg[curso_id_str] = {}
        for comp, data in comps.items():
            percentual_obj = (data['obj_acertos'] / data['obj_validas'] * 100) if data['obj_validas'] > 0 else None
            media_disc = (data['disc_soma'] / data['disc_cont']) if data['disc_cont'] > 0 else None
            final_curso_averages_fg[curso_id_str][comp] = {
                "percentual_objetivas_curso": round(percentual_obj, 2) if percentual_obj is not None else None,
                "media_discursivas_curso": round(media_disc, 2) if media_disc is not None else None,
                "n_objetivas_validas_curso": data['obj_validas'],
                "n_discursivas_validas_curso": data['disc_cont']
            }
        
    if final_curso_averages_fg:
        year_dir_fg = os.path.join(MEDIAS_CURSO_FG_BASE_PATH, str(year))
        os.makedirs(year_dir_fg, exist_ok=True)
        output_path_fg = os.path.join(year_dir_fg, 'medias_curso_fg.json')
        try:
            with open(output_path_fg, 'w', encoding='utf-8') as f:
                json.dump(final_curso_averages_fg, f, ensure_ascii=False, indent=4)
            print(f"    -> Médias FG (Curso) de {year} salvas em '{output_path_fg}'")
        except Exception as e:
            print(f"    -> ERRO ao salvar médias FG (Curso) de {year}: {e}")

    print("\n--- Cálculo de Médias por CURSO (CE e FG) Concluído ---")

if __name__ == '__main__':
    main()