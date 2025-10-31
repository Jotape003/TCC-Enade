import pandas as pd
import os
import glob
import json
from collections import defaultdict
import numpy as np # Para lidar com NaN de forma segura
from tqdm import tqdm

# Importa configurações
from config import PROCESSED_DATA_PATH, YEARS_TO_PROCESS, JSON_DATA_PATH, FINAL_CE_JSON_PATH

# Caminho para o JSON de mapeamento MANUAL
MAP_JSON_PATH = os.path.join(JSON_DATA_PATH, 'comp_especifico_grupo.json/estrutura_competencias_final.json')
# Caminho para o CSV de cursos (para mapear CO_CURSO -> CO_GRUPO)
CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv')

# --- Funções Auxiliares ---

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

def load_curso_grupo_map():
    """Cria um mapa de CO_CURSO (int) para CO_GRUPO (str)."""
    print(f"Carregando mapa CO_CURSO -> CO_GRUPO de '{os.path.basename(CURSOS_CSV_PATH)}'...")
    if not os.path.exists(CURSOS_CSV_PATH):
        print("  -> ERRO: Arquivo CSV de cursos não encontrado.")
        return None
    try:
        # Ajuste sep=',' ou sep=';'
        df_cursos = pd.read_csv(CURSOS_CSV_PATH, sep=';', usecols=['Código', 'CO_GRUPO'])
        df_cursos.columns = ['CO_CURSO', 'CO_GRUPO']
        df_cursos = df_cursos.dropna(subset=['CO_CURSO', 'CO_GRUPO'])
        df_cursos['CO_CURSO'] = pd.to_numeric(df_cursos['CO_CURSO'], errors='coerce').astype('Int64')
        df_cursos['CO_GRUPO'] = pd.to_numeric(df_cursos['CO_GRUPO'], errors='coerce').astype('Int64')
        df_cursos = df_cursos.drop_duplicates(subset=['CO_CURSO'], keep='first')
        # Retorna {106167: '4003', ...} (CO_GRUPO como string)
        mapa = pd.Series(df_cursos.CO_GRUPO.astype(str).values, index=df_cursos.CO_CURSO).to_dict()
        print(f"  -> Mapa CO_CURSO -> CO_GRUPO carregado para {len(mapa)} cursos.")
        return mapa
    except Exception as e:
         print(f"  -> Erro ao ler mapa de cursos: {e}")
         return None

# --- Função Principal de Análise ---

def analisar_competencias_campus_ano(campus_path, campus_name, year, map_competencias, curso_grupo_map):
    """
    Calcula o desempenho por competência, lidando com mapeamentos
    incompletos e mapeamentos de questões para múltiplos componentes (arrays de índices).
    """
    print(f"Analisando Competências: {campus_name} - {year}")

    notas_file_path = glob.glob(os.path.join(campus_path, '*arq3.csv'))
    notas_file_path = glob.glob(os.path.join(campus_path, '*arq3.csv'))
    if not notas_file_path:
        print(f"  -> Aviso: Arquivo arq3.csv não encontrado.")
        return {} # Retorna dicionário vazio se não há dados

    results = defaultdict(lambda: defaultdict(lambda: {'obj_acertos': 0, 'obj_validas': 0, 'disc_soma': 0.0, 'disc_cont': 0}))

    try:
        df_notas = pd.read_csv(notas_file_path[0], sep=';', encoding='utf-8', low_memory=False)
        df_notas.columns = [col.upper() for col in df_notas.columns]

        # Verifica e prepara colunas necessárias
        required_cols = ['CO_CURSO', 'DS_VT_ACE_OCE'] # Mínimo para objetivas
        # Adiciona colunas discursivas se existirem (nomes podem variar)
        disc_cols_ce = [col for col in df_notas.columns if col.startswith('NT_CE_D')]
        required_cols.extend(disc_cols_ce)

        if not 'CO_CURSO' in df_notas.columns or not 'DS_VT_ACE_OCE' in df_notas.columns:
             print(f"  -> ERRO: Colunas CO_CURSO ou DS_VT_ACE_OCE ausentes no arq3.")
             return {}

        # Converte CO_CURSO para Int64
        df_notas['CO_CURSO'] = pd.to_numeric(df_notas['CO_CURSO'], errors='coerce').astype('Int64')
        df_notas = df_notas.dropna(subset=['CO_CURSO'])
        for col in disc_cols_ce:
            if df_notas[col].dtype == 'object':
                 df_notas[col] = df_notas[col].str.replace(',', '.', regex=False)
            df_notas[col] = pd.to_numeric(df_notas[col], errors='coerce')


        print(f"  -> Processando {len(df_notas)} registros de alunos...")
        alunos_sem_mapeamento = 0

        for index, row in tqdm(df_notas.iterrows(), total=len(df_notas), desc="Processando Alunos"):
            curso_id = row['CO_CURSO']
            co_grupo_str = curso_grupo_map.get(curso_id)

            if not co_grupo_str or co_grupo_str not in map_competencias:
                alunos_sem_mapeamento += 1
                continue

            map_grupo = map_competencias.get(co_grupo_str, {})
            # ===> Pega a lista de nomes dos Componentes Específicos <===
            lista_componentes = map_grupo.get('Componente_especifico', []) 
            # ==========================================================
            map_ano = map_grupo.get('Anos', {}).get(str(year), {})
            questoes_ce = map_ano.get('questoes_CE', {})
            map_obj = questoes_ce.get('objetivas', {})
            map_disc = questoes_ce.get('discursivas', {})

            # --- Processa Objetivas CE (Lógica Modificada) ---
            respostas_obj = str(row['DS_VT_ACE_OCE']) if pd.notna(row['DS_VT_ACE_OCE']) else ''
            questoes_obj_mapeadas = list(map_obj.keys())

            if len(respostas_obj) >= 27: # Ajuste o 27 se o número de obj CE variar
                for q_key in questoes_obj_mapeadas:
                    try:
                        q_index = int(q_key[1:]) - 9
                        if 0 <= q_index < len(respostas_obj):
                            # ===> LÓGICA PARA ARRAY DE ÍNDICES <===
                            mapeamento = map_obj.get(q_key) # Pode ser [5, 6] ou [2] ou None

                            if mapeamento is None: continue # Pula se não mapeado

                            # Garante que seja sempre uma lista para iterar
                            indices_competencia = mapeamento if isinstance(mapeamento, list) else [mapeamento]
                            
                            for indice_1_based in indices_competencia:
                                try:
                                    # Converte índice 1-based para 0-based
                                    indice_0_based = int(indice_1_based) - 1 
                                    if 0 <= indice_0_based < len(lista_componentes):
                                        competencia_nome = lista_componentes[indice_0_based] # Pega o NOME
                                        
                                        # Atualiza estatísticas para esta competência
                                        resposta = respostas_obj[q_index]
                                        if resposta in ['0', '1']:
                                            results[curso_id][competencia_nome]['obj_validas'] += 1
                                            if resposta == '1':
                                                results[curso_id][competencia_nome]['obj_acertos'] += 1
                                    else:
                                         print(f"  -> Aviso: Índice de competência inválido ({indice_1_based}) para {q_key} no grupo {co_grupo_str}/{year}.")
                                except (ValueError, TypeError):
                                     print(f"  -> Aviso: Valor de mapeamento inválido ('{indice_1_based}') para {q_key} no grupo {co_grupo_str}/{year}. Esperado número(s).")
                            # =======================================
                    except (ValueError, IndexError):
                         continue

            # --- Processa Discursivas CE (Lógica Modificada) ---
            questoes_disc_mapeadas = list(map_disc.keys())

            for d_key in questoes_disc_mapeadas:
                try:
                    d_index_num = int(d_key[1:])
                    nota_col_suffix = d_index_num - 2
                    nota_col_name = f"NT_CE_D{nota_col_suffix}"

                    # ===> LÓGICA PARA ARRAY DE ÍNDICES <===
                    mapeamento = map_disc.get(d_key) # Pode ser [1] ou [1, 14] ou None
                    
                    if mapeamento is None: continue

                    indices_competencia = mapeamento if isinstance(mapeamento, list) else [mapeamento]

                    for indice_1_based in indices_competencia:
                         try:
                             indice_0_based = int(indice_1_based) - 1
                             if 0 <= indice_0_based < len(lista_componentes):
                                 competencia_nome = lista_componentes[indice_0_based] # Pega o NOME

                                 # Atualiza estatísticas para esta competência
                                 if nota_col_name in row:
                                     nota = row[nota_col_name]
                                     if pd.notna(nota):
                                         results[curso_id][competencia_nome]['disc_soma'] += nota
                                         results[curso_id][competencia_nome]['disc_cont'] += 1
                             else:
                                 print(f"  -> Aviso: Índice de competência inválido ({indice_1_based}) para {d_key} no grupo {co_grupo_str}/{year}.")
                         except (ValueError, TypeError):
                              print(f"  -> Aviso: Valor de mapeamento inválido ('{indice_1_based}') para {d_key} no grupo {co_grupo_str}/{year}. Esperado número(s).")
                    # =======================================
                except ValueError:
                    continue

        if alunos_sem_mapeamento > 0:
            print(f"  -> Aviso: {alunos_sem_mapeamento} alunos foram pulados por falta de mapeamento CO_GRUPO.")

        # --- Calcula Métricas Finais (sem alteração) ---
        final_results = {}
        print(f"  -> Calculando métricas finais por competência...")
        # ... (código para calcular percentual_obj e media_disc como antes) ...
        for curso_id_int, comps in results.items():
            curso_id_str = str(curso_id_int) 
            final_results[curso_id_str] = []
            for comp, data in comps.items():
                percentual_obj = (data['obj_acertos'] / data['obj_validas'] * 100) if data['obj_validas'] > 0 else None
                media_disc = (data['disc_soma'] / data['disc_cont']) if data['disc_cont'] > 0 else None

                percentual_obj_rounded = round(percentual_obj, 2) if percentual_obj is not None else None
                media_disc_rounded = round(media_disc, 2) if media_disc is not None else None

                final_results[curso_id_str].append({
                    "competencia": comp,
                    "percentual_objetivas": percentual_obj_rounded,
                    "media_discursivas": media_disc_rounded,
                    "n_objetivas_validas": data['obj_validas'],
                    "n_discursivas_validas": data['disc_cont']
                })
            final_results[curso_id_str].sort(key=lambda x: x['competencia'])


        return final_results

    except KeyError as e:
        print(f"  -> ERRO de Coluna (KeyError) em {campus_name}/{year}: A coluna {e} não foi encontrada. Verifique o arquivo arq3.csv.")
        return {}
    except Exception as e:
        print(f"  -> ERRO GERAL ao processar competências de {campus_name}/{year}: {e}")
        return {}

# --- Função Principal de Orquestração ---
def main():
    map_competencias = load_json(MAP_JSON_PATH, "Mapeamento de Competências")
    curso_grupo_map = load_curso_grupo_map()

    if not map_competencias or not curso_grupo_map:
        print("Encerrando script devido a erro no carregamento dos arquivos de mapeamento.")
        return

    os.makedirs(JSON_DATA_PATH, exist_ok=True)
    campus_folders = [d for d in os.listdir(PROCESSED_DATA_PATH) if os.path.isdir(os.path.join(PROCESSED_DATA_PATH, d))]

    for campus_name in campus_folders:
        for year_str in YEARS_TO_PROCESS:
            campus_year_path = os.path.join(PROCESSED_DATA_PATH, campus_name, str(year_str))
            if os.path.exists(campus_year_path):
                # Calcula os resultados para o campus/ano
                resultados_competencia = analisar_competencias_campus_ano(
                    campus_year_path, campus_name, str(year_str),
                    map_competencias, curso_grupo_map
                )

                # Salva os resultados se não estiverem vazios
                if resultados_competencia:
                    output_dir = os.path.join(FINAL_CE_JSON_PATH, campus_name)
                    os.makedirs(output_dir, exist_ok=True)
                    output_path = os.path.join(output_dir, f'competencias_{year_str}.json')
                    try:
                        with open(output_path, 'w', encoding='utf-8') as f:
                            json.dump(resultados_competencia, f, ensure_ascii=False, indent=4)
                        print(f"  -> Sucesso! Análise de competência salva em '{output_path}'")
                    except Exception as e:
                        print(f"  -> ERRO ao salvar JSON de competências para {campus_name}/{year_str}: {e}")

if __name__ == '__main__':
    main()