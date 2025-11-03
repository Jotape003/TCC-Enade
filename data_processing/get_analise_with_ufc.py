import pandas as pd
import os
import glob
import json
from collections import defaultdict
import numpy as np
from tqdm import tqdm

# Importa configurações
from config import PROCESSED_DATA_PATH, YEARS_TO_PROCESS, FINAL_CE_GERAL_JSON_PATH

# Caminhos para os arquivos de mapeamento
MAP_JSON_PATH = os.path.join(FINAL_CE_GERAL_JSON_PATH, 'estrutura_competencias_final.json') # Ajuste o nome se for o simplificado
CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv')

# --- Funções Auxiliares (load_json, load_curso_grupo_map - como antes) ---
def load_json(file_path, description):
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

# --- Passagem 1: Pré-calcular Médias UFC por Competência ---
def pre_calcular_medias_ufc(map_competencias, curso_grupo_map):
    print("\n--- INICIANDO PASSAGEM 1: Calculando Médias de Competência da UFC (Geral) ---")
    results_ufc_agg = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {'obj_acertos': 0, 'obj_validas': 0, 'disc_soma': 0.0, 'disc_cont': 0})))

    campus_folders = [d for d in os.listdir(PROCESSED_DATA_PATH) if os.path.isdir(os.path.join(PROCESSED_DATA_PATH, d))]

    for year in YEARS_TO_PROCESS:
        print(f"Processando Ano: {year}")
        for campus_name in campus_folders:
            # ... (Lógica de leitura e loop de alunos como antes) ...
            campus_year_path = os.path.join(PROCESSED_DATA_PATH, campus_name, str(year))
            if not os.path.exists(campus_year_path): continue
            notas_file_path = glob.glob(os.path.join(campus_year_path, '*arq3.csv'))
            if not notas_file_path: continue

            try:
                df_notas = pd.read_csv(notas_file_path[0], sep=';', encoding='utf-8', low_memory=False)
                df_notas.columns = [col.upper() for col in df_notas.columns]
                disc_cols_ce = [col for col in df_notas.columns if col.startswith('NT_CE_D')]
                df_notas['CO_CURSO'] = pd.to_numeric(df_notas['CO_CURSO'], errors='coerce').astype('Int64')
                df_notas = df_notas.dropna(subset=['CO_CURSO'])
                for col in disc_cols_ce:
                    if df_notas[col].dtype == 'object':
                        df_notas[col] = df_notas[col].str.replace(',', '.', regex=False)
                    df_notas[col] = pd.to_numeric(df_notas[col], errors='coerce')
                
                for index, row in df_notas.iterrows():
                    curso_id = row['CO_CURSO']
                    co_grupo_str = curso_grupo_map.get(curso_id)
                    if not co_grupo_str or co_grupo_str not in map_competencias: continue
                    map_grupo = map_competencias.get(co_grupo_str, {})
                    lista_componentes = map_grupo.get('Componente_especifico', [])
                    map_ano = map_grupo.get('Anos', {}).get(str(year), {})
                    questoes_ce = map_ano.get('questoes_CE', {})
                    map_obj = questoes_ce.get('objetivas', {})
                    map_disc = questoes_ce.get('discursivas', {})

                    # Processa Objetivas (Agregado UFC)
                    respostas_obj = str(row['DS_VT_ACE_OCE']) if pd.notna(row['DS_VT_ACE_OCE']) else ''
                    if len(respostas_obj) >= 27: # Ajuste se necessário
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
                                            results_ufc_agg[year][co_grupo_str][comp]['obj_validas'] += 1
                                            if resp == '1':
                                                results_ufc_agg[year][co_grupo_str][comp]['obj_acertos'] += 1
                            except: continue

                    # Processa Discursivas (Agregado UFC)
                    for d_key, mapeamento in map_disc.items():
                        try:
                            suffix = int(d_key[1:]) - 2
                            col_name = f"NT_CE_D{suffix}"
                            indices = mapeamento if isinstance(mapeamento, list) else [mapeamento]
                            for idx_1 in indices:
                                idx_0 = int(idx_1) - 1
                                if 0 <= idx_0 < len(lista_componentes):
                                    comp = lista_componentes[idx_0]
                                    if col_name in row:
                                        nota = row[col_name]
                                        if pd.notna(nota):
                                            results_ufc_agg[year][co_grupo_str][comp]['disc_soma'] += nota
                                            results_ufc_agg[year][co_grupo_str][comp]['disc_cont'] += 1
                        except: continue
            except Exception as e:
                print(f"  -> ERRO ao processar campus {campus_name} para {year}: {e}")

    # Calcula as médias finais da UFC
    final_ufc_averages = {}
    print("  -> Calculando médias finais agregadas da UFC...")
    for year, grupos in results_ufc_agg.items():
        final_ufc_averages[year] = {}
        for grupo, comps in grupos.items():
            final_ufc_averages[year][grupo] = {}
            for comp, data in comps.items():
                percentual_obj = (data['obj_acertos'] / data['obj_validas'] * 100) if data['obj_validas'] > 0 else None
                media_disc = (data['disc_soma'] / data['disc_cont']) if data['disc_cont'] > 0 else None
                final_ufc_averages[year][grupo][comp] = {
                    "percentual_objetivas_ufc": round(percentual_obj, 2) if percentual_obj is not None else None,
                    "media_discursivas_ufc": round(media_disc, 2) if media_disc is not None else None,
                    # =====> ADIÇÃO AQUI (Passagem 1) <=====
                    "n_objetivas_validas_ufc": data['obj_validas'],
                    "n_discursivas_validas_ufc": data['disc_cont']
                }
    print("--- PASSAGEM 1 Concluída ---")
    return final_ufc_averages

# --- Passagem 2: Calcular Médias do Curso e Juntar com Médias UFC ---
def analisar_e_salvar_dados_por_curso(map_competencias, curso_grupo_map, ufc_avg_map):
    print("\n--- INICIANDO PASSAGEM 2: Calculando Médias por Curso e Juntando com Médias UFC ---")
    
    campus_folders = [d for d in os.listdir(PROCESSED_DATA_PATH) if os.path.isdir(os.path.join(PROCESSED_DATA_PATH, d))]

    for campus_name in campus_folders:
        for year in YEARS_TO_PROCESS:
            campus_year_path = os.path.join(PROCESSED_DATA_PATH, campus_name, str(year))
            if not os.path.exists(campus_year_path): continue

            print(f"Analisando: {campus_name} - {year}")
            
            notas_file_path = glob.glob(os.path.join(campus_year_path, '*arq3.csv'))
            if not notas_file_path: continue

            results_por_curso = defaultdict(lambda: defaultdict(lambda: {'obj_acertos': 0, 'obj_validas': 0, 'disc_soma': 0.0, 'disc_cont': 0}))

            try:
                df_notas = pd.read_csv(notas_file_path[0], sep=';', encoding='utf-8', low_memory=False)
                df_notas.columns = [col.upper() for col in df_notas.columns]
                # ... (Mesma limpeza de colunas e loop de alunos do Passo 1) ...
                disc_cols_ce = [col for col in df_notas.columns if col.startswith('NT_CE_D')]
                df_notas['CO_CURSO'] = pd.to_numeric(df_notas['CO_CURSO'], errors='coerce').astype('Int64')
                df_notas = df_notas.dropna(subset=['CO_CURSO'])
                for col in disc_cols_ce:
                    if df_notas[col].dtype == 'object':
                         df_notas[col] = df_notas[col].str.replace(',', '.', regex=False)
                    df_notas[col] = pd.to_numeric(df_notas[col], errors='coerce')
                
                for index, row in df_notas.iterrows(): 
                    curso_id = row['CO_CURSO']
                    co_grupo_str = curso_grupo_map.get(curso_id)
                    if not co_grupo_str or co_grupo_str not in map_competencias: continue
                    map_grupo = map_competencias.get(co_grupo_str, {})
                    lista_componentes = map_grupo.get('Componente_especifico', [])
                    map_ano = map_grupo.get('Anos', {}).get(str(year), {})
                    questoes_ce = map_ano.get('questoes_CE', {})
                    map_obj = questoes_ce.get('objetivas', {})
                    map_disc = questoes_ce.get('discursivas', {})
                    
                    # Processa Objetivas (Por Curso)
                    respostas_obj = str(row['DS_VT_ACE_OCE']) if pd.notna(row['DS_VT_ACE_OCE']) else ''
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
                                            results_por_curso[curso_id][comp]['obj_validas'] += 1
                                            if resp == '1':
                                                results_por_curso[curso_id][comp]['obj_acertos'] += 1
                            except: continue

                    # Processa Discursivas (Por Curso)
                    for d_key, mapeamento in map_disc.items():
                        try:
                            suffix = int(d_key[1:]) - 2
                            col_name = f"NT_CE_D{suffix}"
                            indices = mapeamento if isinstance(mapeamento, list) else [mapeamento]
                            for idx_1 in indices:
                                idx_0 = int(idx_1) - 1
                                if 0 <= idx_0 < len(lista_componentes):
                                    comp = lista_componentes[idx_0]
                                    if col_name in row:
                                        nota = row[col_name]
                                        if pd.notna(nota):
                                            results_por_curso[curso_id][comp]['disc_soma'] += nota
                                            results_por_curso[curso_id][comp]['disc_cont'] += 1
                        except: continue
                
                # --- Calcula Métricas Finais e Junta com Médias UFC ---
                final_results_campus = {}
                for curso_id_int, comps in results_por_curso.items():
                    curso_id_str = str(curso_id_int)
                    co_grupo_str = curso_grupo_map.get(curso_id_int)
                    final_results_campus[curso_id_str] = []
                    
                    for comp_nome, data in comps.items():
                        percentual_obj_curso = (data['obj_acertos'] / data['obj_validas'] * 100) if data['obj_validas'] > 0 else None
                        media_disc_curso = (data['disc_soma'] / data['disc_cont']) if data['disc_cont'] > 0 else None
                        
                        media_ufc_comp = ufc_avg_map.get(str(year), {}).get(co_grupo_str, {}).get(comp_nome, {})
                        
                        final_results_campus[curso_id_str].append({
                            "competencia": comp_nome,
                            "percentual_objetivas_curso": round(percentual_obj_curso, 2) if percentual_obj_curso is not None else None,
                            "media_discursivas_curso": round(media_disc_curso, 2) if media_disc_curso is not None else None,
                            "percentual_objetivas_ufc": media_ufc_comp.get('percentual_objetivas_ufc'),
                            "media_discursivas_ufc": media_ufc_comp.get('media_discursivas_ufc'),
                            # =====> ADIÇÃO AQUI (Passagem 2) <=====
                            "n_objetivas_validas_curso": data['obj_validas'],
                            "n_discursivas_validas_curso": data['disc_cont'],
                            "n_objetivas_validas_ufc": media_ufc_comp.get('n_objetivas_validas_ufc'),
                            "n_discursivas_validas_ufc": media_ufc_comp.get('n_discursivas_validas_ufc')
                        })
                    final_results_campus[curso_id_str].sort(key=lambda x: x['competencia'])

                # Salva o arquivo JSON final
                if final_results_campus:
                    output_dir = os.path.join(FINAL_CE_GERAL_JSON_PATH, campus_name)
                    os.makedirs(output_dir, exist_ok=True)
                    output_path = os.path.join(output_dir, f'competencias_{year}.json')
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(final_results_campus, f, ensure_ascii=False, indent=4)
                    print(f"  -> Sucesso! Análise de competência COM MÉDIA UFC salva em '{output_path}'")

            except Exception as e:
                print(f"  -> ERRO GERAL ao processar {campus_name}/{year}: {e}")

# --- Função Principal de Orquestração ---
def main():
    map_competencias = load_json(MAP_JSON_PATH, "Mapeamento de Competências")
    curso_grupo_map = load_curso_grupo_map()

    if not map_competencias or not curso_grupo_map:
        print("Encerrando script devido a erro no carregamento dos arquivos de mapeamento.")
        return

    # PASSAGEM 1: Calcular todas as médias da UFC primeiro
    ufc_avg_map = pre_calcular_medias_ufc(map_competencias, curso_grupo_map)

    # PASSAGEM 2: Calcular médias por curso e juntar com as médias da UFC
    if ufc_avg_map:
        analisar_e_salvar_dados_por_curso(map_competencias, curso_grupo_map, ufc_avg_map)
    else:
        print("ERRO: Não foi possível calcular as médias da UFC. Encerrando.")

if __name__ == '__main__':
    main()