import pandas as pd
import os
import glob
import json
from collections import defaultdict
import numpy as np
from tqdm import tqdm

from config import PROCESSED_DATA_PATH, YEARS_TO_PROCESS, FINAL_ESTRUTURA_JSON_PATH, FINAL_MEDIA_JSON_PATH

MAP_CE_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_competencias_final.json') 
MAP_FG_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_fg_final.json')
CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv')

MEDIAS_UFC_CE_BASE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'CE', 'Medias_agregadas')
MEDIAS_UFC_FG_BASE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'FG', 'Medias_agregadas')

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
        df_cursos = pd.read_csv(CURSOS_CSV_PATH, sep=';', usecols=['Código', 'CO_GRUPO']) # Ajuste 'sep'
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

def calcular_e_salvar_medias_ufc(map_competencias_ce, map_competencias_fg, curso_grupo_map):
    print("\n--- INICIANDO: Calculando Médias de Competência da UFC (Geral) para CE e FG ---")
    
    results_ufc_agg_ce = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {'obj_acertos': 0, 'obj_validas': 0, 'disc_soma': 0.0, 'disc_cont': 0})))
    results_ufc_agg_fg = defaultdict(lambda: defaultdict(lambda: {'obj_acertos': 0, 'obj_validas': 0, 'disc_soma': 0.0, 'disc_cont': 0}))

    campus_folders = [d for d in os.listdir(PROCESSED_DATA_PATH) if os.path.isdir(os.path.join(PROCESSED_DATA_PATH, d))]

    for year in YEARS_TO_PROCESS:
        print(f"Processando Ano: {year}")
        
        map_fg_ano_obj, map_fg_ano_disc, lista_componentes_fg = {}, {}, []
        if map_competencias_fg:
            map_ano_fg_data = next((item for item in map_competencias_fg if str(item.get("ANO")) == str(year)), None)
            if map_ano_fg_data:
                lista_componentes_fg = map_ano_fg_data.get("Formacao_geral", [])
                map_fg_ano_obj = map_ano_fg_data.get("questoes", {}).get("objetivas", {})
                map_fg_ano_disc = map_ano_fg_data.get("questoes", {}).get("discursivas", {})
            else:
                print(f"  -> Aviso: Mapeamento de FG para o ano {year} não encontrado no JSON.")
        
        for campus_name in campus_folders:
            campus_year_path = os.path.join(PROCESSED_DATA_PATH, campus_name, str(year))
            if not os.path.exists(campus_year_path): continue
            notas_file_path = glob.glob(os.path.join(campus_year_path, '*arq3.csv'))
            if not notas_file_path: continue

            try:
                df_notas = pd.read_csv(notas_file_path[0], sep=';', encoding='utf-8', low_memory=False)
                df_notas.columns = [col.upper() for col in df_notas.columns]
                
                disc_cols_ce = [col for col in df_notas.columns if col.startswith('NT_CE_D')]
                disc_cols_fg = [col for col in df_notas.columns if col.startswith('NT_FG_D')]
                df_notas['CO_CURSO'] = pd.to_numeric(df_notas['CO_CURSO'], errors='coerce').astype('Int64')
                df_notas = df_notas.dropna(subset=['CO_CURSO'])
                for col in disc_cols_ce + disc_cols_fg:
                    if col in df_notas.columns:
                        if df_notas[col].dtype == 'object':
                            df_notas[col] = df_notas[col].str.replace(',', '.', regex=False)
                        df_notas[col] = pd.to_numeric(df_notas[col], errors='coerce')
                
                for index, row in tqdm(df_notas.iterrows(), total=len(df_notas), desc=f"  Lendo {campus_name}", leave=False):
                    curso_id = row['CO_CURSO']
                    co_grupo_str = curso_grupo_map.get(curso_id)
                    
                    if co_grupo_str and co_grupo_str in map_competencias_ce:
                        map_grupo = map_competencias_ce.get(co_grupo_str, {})
                        lista_componentes_ce = map_grupo.get('Componente_especifico', [])
                        map_ano_ce = map_grupo.get('Anos', {}).get(str(year), {})
                        questoes_ce = map_ano_ce.get('questoes_CE', {})
                        map_obj_ce = questoes_ce.get('objetivas', {})
                        map_disc_ce = questoes_ce.get('discursivas', {})
                        
                        respostas_obj_ce = str(row['DS_VT_ACE_OCE']) if pd.notna(row['DS_VT_ACE_OCE']) else ''
                        if len(respostas_obj_ce) >= len(map_obj_ce): 
                            for q_key, mapeamento in map_obj_ce.items():
                                try:
                                    q_index = int(q_key[1:]) - 9 # q9 -> índice 0
                                    indices = mapeamento if isinstance(mapeamento, list) else [mapeamento]
                                    for idx_1 in indices:
                                        idx_0 = int(idx_1) - 1
                                        if 0 <= idx_0 < len(lista_componentes_ce) and 0 <= q_index < len(respostas_obj_ce):
                                            comp = lista_componentes_ce[idx_0]
                                            resp = respostas_obj_ce[q_index]
                                            if resp in ['0', '1']:
                                                results_ufc_agg_ce[year][co_grupo_str][comp]['obj_validas'] += 1
                                                if resp == '1':
                                                    results_ufc_agg_ce[year][co_grupo_str][comp]['obj_acertos'] += 1
                                except: continue

                        for d_key, mapeamento in map_disc_ce.items():
                            try:
                                suffix = int(d_key[1:]) - 2
                                col_name = f"NT_CE_D{suffix}"
                                indices = mapeamento if isinstance(mapeamento, list) else [mapeamento]
                                for idx_1 in indices:
                                    idx_0 = int(idx_1) - 1
                                    if 0 <= idx_0 < len(lista_componentes_ce):
                                        comp = lista_componentes_ce[idx_0]
                                        if col_name in row:
                                            nota = row[col_name]
                                            if pd.notna(nota):
                                                results_ufc_agg_ce[year][co_grupo_str][comp]['disc_soma'] += nota
                                                results_ufc_agg_ce[year][co_grupo_str][comp]['disc_cont'] += 1
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
                                                results_ufc_agg_fg[year][comp]['obj_validas'] += 1
                                                if resp == '1':
                                                    results_ufc_agg_fg[year][comp]['obj_acertos'] += 1
                                except: continue
                        
                        for d_key, mapeamento in map_fg_ano_disc.items():
                            try:
                                suffix = int(d_key[1:])
                                col_name = f"NT_FG_D{suffix}"
                                indices = mapeamento if isinstance(mapeamento, list) else [mapeamento]
                                for idx_1 in indices:
                                    idx_0 = int(idx_1) - 1
                                    if 0 <= idx_0 < len(lista_componentes_fg):
                                        comp = lista_componentes_fg[idx_0]
                                        if col_name in row:
                                            nota = row[col_name]
                                            if pd.notna(nota):
                                                results_ufc_agg_fg[year][comp]['disc_soma'] += nota
                                                results_ufc_agg_fg[year][comp]['disc_cont'] += 1
                            except: continue
            except Exception as e:
                print(f"  -> ERRO ao processar campus {campus_name} para {year}: {e}")

    print("  -> Calculando e salvando médias finais agregadas da UFC (CE)...")
    for year, grupos in results_ufc_agg_ce.items():
        final_ufc_averages_ce = {}
        for grupo, comps in grupos.items():
            final_ufc_averages_ce[grupo] = {}
            for comp, data in comps.items():
                percentual_obj = (data['obj_acertos'] / data['obj_validas'] * 100) if data['obj_validas'] > 0 else None
                media_disc = (data['disc_soma'] / data['disc_cont']) if data['disc_cont'] > 0 else None
                final_ufc_averages_ce[grupo][comp] = {
                    "percentual_objetivas_ufc": round(percentual_obj, 2) if percentual_obj is not None else None,
                    "media_discursivas_ufc": round(media_disc, 2) if media_disc is not None else None,
                    "n_objetivas_validas_ufc": data['obj_validas'],
                    "n_discursivas_validas_ufc": data['disc_cont']
                }
        
        year_dir = os.path.join(MEDIAS_UFC_CE_BASE_PATH, str(year))
        os.makedirs(year_dir, exist_ok=True)
        output_path = os.path.join(year_dir, 'medias_ufc_ce.json')
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(final_ufc_averages_ce, f, ensure_ascii=False, indent=4)
            print(f"    -> Médias CE de {year} salvas em '{output_path}'")
        except Exception as e:
            print(f"    -> ERRO ao salvar médias CE de {year}: {e}")
    
    print("  -> Calculando e salvando médias finais agregadas da UFC (FG)...")
    for year, comps in results_ufc_agg_fg.items():
        final_ufc_averages_fg = {}
        for comp, data in comps.items():
            percentual_obj = (data['obj_acertos'] / data['obj_validas'] * 100) if data['obj_validas'] > 0 else None
            media_disc = (data['disc_soma'] / data['disc_cont']) if data['disc_cont'] > 0 else None
            final_ufc_averages_fg[comp] = {
                "percentual_objetivas_ufc": round(percentual_obj, 2) if percentual_obj is not None else None,
                "media_discursivas_ufc": round(media_disc, 2) if media_disc is not None else None,
                "n_objetivas_validas_ufc": data['obj_validas'],
                "n_discursivas_validas_ufc": data['disc_cont']
            }
        
        year_dir = os.path.join(MEDIAS_UFC_FG_BASE_PATH, str(year))
        os.makedirs(year_dir, exist_ok=True)
        output_path = os.path.join(year_dir, 'medias_ufc_fg.json')
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(final_ufc_averages_fg, f, ensure_ascii=False, indent=4)
            print(f"    -> Médias FG de {year} salvas em '{output_path}'")
        except Exception as e:
            print(f"    -> ERRO ao salvar médias FG de {year}: {e}")

    print("\n--- Cálculo de Médias UFC (CE e FG) Concluído ---")

def main():
    map_competencias_ce = load_json(MAP_CE_JSON_PATH, "Mapeamento de Competências CE")
    map_competencias_fg = load_json(MAP_FG_JSON_PATH, "Mapeamento de Competências FG")
    curso_grupo_map = load_curso_grupo_map()

    if not all([map_competencias_ce, map_competencias_fg, curso_grupo_map]):
        print("Encerrando script devido a erro no carregamento dos arquivos de mapeamento.")
        print(f"  Mapa CE: {'OK' if map_competencias_ce else 'FALHOU'}")
        print(f"  Mapa FG: {'OK' if map_competencias_fg else 'FALHOU'}")
        print(f"  Mapa Cursos: {'OK' if curso_grupo_map else 'FALHOU'}")
        return

    calcular_e_salvar_medias_ufc(map_competencias_ce, map_competencias_fg, curso_grupo_map)
    
    print("\nScript 'gerar_medias_ufc_competencia.py' concluído.")

if __name__ == '__main__':
    main()