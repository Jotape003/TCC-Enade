import pandas as pd
import os
import glob
import json
import numpy as np
from collections import defaultdict

from config import PROCESSED_DATA_PATH, YEARS_TO_PROCESS, JSON_DATA_PATH, QUESTOES_MAP

OUTPUT_PERFIL_BASE_PATH = os.path.join(JSON_DATA_PATH, 'Analise_Perfil')

def load_course_names():
    curso_path = os.path.join('data', 'cursos_ufc.csv')
    if not os.path.exists(curso_path): return {}
    try:
        df = pd.read_csv(curso_path, sep=';', usecols=['Código', 'Curso'])
        return pd.Series(df.Curso.values, index=df['Código']).to_dict()
    except: return {}

def main():
    print("--- INICIANDO: Geração Unificada de Análise de Perfil ---")

    os.makedirs(OUTPUT_PERFIL_BASE_PATH, exist_ok=True)
    
    campus_folders = [d for d in os.listdir(PROCESSED_DATA_PATH) if os.path.isdir(os.path.join(PROCESSED_DATA_PATH, d))]
    colunas_interesse = list(QUESTOES_MAP.keys()) 
    nome_cursos_map = load_course_names()

    for campus_name in campus_folders:
        print(f"\nProcessando Campus: {campus_name}")
        
        dados_consolidados_campus = defaultdict(lambda: {"nome": "", "historico": {}})

        for year in YEARS_TO_PROCESS:
            campus_year_path = os.path.join(PROCESSED_DATA_PATH, campus_name, str(year))
            if not os.path.exists(campus_year_path): continue

            possible_files = glob.glob(os.path.join(campus_year_path, '*arq4.csv'))
            
            target_file = None
            found_cols = []

            for fpath in possible_files:
                try:
                    df_head = pd.read_csv(fpath, sep=';', encoding='utf-8', nrows=1)
                    cols_upper = [c.upper() for c in df_head.columns]
                    intersection = [c for c in colunas_interesse if c in cols_upper]
                    if len(intersection) > 5:
                        target_file = fpath
                        found_cols = intersection
                        break
                except: continue

            if not target_file:
                continue

            try:
                print(f"  -> Lendo {year}: {os.path.basename(target_file)}")
                cols_to_load = ['CO_CURSO'] + found_cols
                
                df = pd.read_csv(target_file, sep=';', encoding='utf-8', usecols=cols_to_load, low_memory=False)
                df.columns = [col.upper() for col in df.columns]

                for col in found_cols:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                
                if df['CO_CURSO'].dtype == 'float':
                    df['CO_CURSO'] = df['CO_CURSO'].fillna(0).astype(int)

                cursos_unicos = df['CO_CURSO'].unique()

                for co_curso in cursos_unicos:
                    df_curso = df[df['CO_CURSO'] == co_curso].copy()
                    curso_str = str(co_curso)
                    
                    if not dados_consolidados_campus[curso_str]["nome"]:
                         dados_consolidados_campus[curso_str]["nome"] = nome_cursos_map.get(co_curso, str(co_curso))

                    dados_ano = {
                        "didatica": [],
                        "infra": [],
                        "oportunidades": [],
                        "geral": []
                    }

                    total_alunos = len(df_curso)

                    for q_code in found_cols:
                        if q_code not in QUESTOES_MAP: continue
                        
                        respostas = df_curso[q_code]
                        validas = respostas[respostas.isin([1, 2, 3, 4, 5, 6])]
                        nao_sei = respostas[respostas.isin([7, 8])]
                        
                        media = validas.mean()
                        count_nao_sei = len(nao_sei)
                        perc_nao_sei = (count_nao_sei / total_alunos * 100) if total_alunos > 0 else 0

                        if pd.notna(media):
                            info = QUESTOES_MAP[q_code]
                            item = {
                                "codigo": q_code,
                                "pergunta": info["texto"],
                                "nota": round(media),
                                "nao_sei_perc": round(perc_nao_sei, 1)
                            }
                            dados_ano[info["cat"]].append(item)
                    
                    dados_consolidados_campus[curso_str]["historico"][str(year)] = dados_ano

            except Exception as e:
                print(f"  -> Erro em {campus_name}/{year}: {e}")

        if dados_consolidados_campus:
            output_dir = os.path.join(OUTPUT_PERFIL_BASE_PATH, campus_name)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, 'perfil_consolidado.json')
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(dados_consolidados_campus, f, ensure_ascii=False, indent=4)
            print(f"  -> Arquivo consolidado salvo em '{output_path}'")

if __name__ == '__main__':
    main()