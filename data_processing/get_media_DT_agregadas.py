import pandas as pd
import os
import glob
import json
from collections import defaultdict
import numpy as np
from tqdm import tqdm

# Importa configurações
from config import PROCESSED_DATA_PATH, YEARS_TO_PROCESS, FINAL_JSON_PATH, FINAL_MEDIA_JSON_PATH, FINAL_DT_JSON_PATH, FINAL_ESTRUTURA_JSON_PATH

# --- Caminhos de ENTRADA ---
MAP_CE_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_competencias_final.json')
MAP_FG_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_fg_final.json')
CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv')

# --- Caminhos para Médias Pré-Calculadas (CE e FG) ---
MEDIAS_CE_CURSOS_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'CE', 'Medias_Curso')
MEDIAS_FG_CURSOS_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'FG', 'Medias_Curso')

MEDIAS_CE_AGREGADAS_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'CE', 'Medias_Agregadas')
MEDIAS_FG_AGREGADAS_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'FG', 'Medias_Agregadas')

# --- Caminhos de SAÍDA ---
OUTPUT_DT_BASE_PATH = os.path.join(FINAL_DT_JSON_PATH)

# --- Funções Auxiliares de Carregamento ---
def load_json_safe(file_path, default_val=None):
    """Carrega JSON, retornando default_val (vazio dict) se o arquivo não existir ou falhar."""
    if default_val is None:
        default_val = {}
    if not os.path.exists(file_path):
        return default_val
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"   -> ERRO ao carregar JSON: {file_path}. Erro: {e}")
        return default_val

def get_curso_info_map():
    """Retorna um mapa {CO_CURSO_str: {'CO_GRUPO': '...', 'Município': '...', 'Curso': '...'}}."""
    if not os.path.exists(CURSOS_CSV_PATH):
        print(f"ERRO CRÍTICO: Arquivo '{CURSOS_CSV_PATH}' não encontrado.")
        return None
    try:
        use_cols = ['Código', 'CO_GRUPO', 'Município', 'Curso']
        df_cursos = pd.read_csv(CURSOS_CSV_PATH, sep=';', usecols=[c for c in use_cols if c in pd.read_csv(CURSOS_CSV_PATH, nrows=0, sep=';').columns])
        # Padroniza nomes (se faltar colunas, lidamos)
        for col in ['Código', 'CO_GRUPO', 'Município', 'Curso']:
            if col not in df_cursos.columns:
                df_cursos[col] = None

        df_cursos.dropna(subset=['Código'], inplace=True)
        df_cursos['Código'] = pd.to_numeric(df_cursos['Código'], errors='coerce').astype('Int64').astype(str)
        df_cursos['CO_GRUPO'] = pd.to_numeric(df_cursos['CO_GRUPO'], errors='coerce').astype('Int64').astype(str)
        df_cursos['Município'] = df_cursos['Município'].fillna('Sem_Municipio').astype(str).str.strip().str.title()
        df_cursos['Curso'] = df_cursos['Curso'].fillna('Desconhecido').astype(str).str.strip()

        df_cursos = df_cursos.drop_duplicates(subset=['Código'], keep='first')
        relevant_cursos_map = df_cursos.set_index('Código').to_dict(orient='index')

        print(f"Mapeamento de {len(relevant_cursos_map)} cursos para grupos, municípios e nomes carregado.")
        return relevant_cursos_map
    except Exception as e:
        print(f"Erro ao ler info dos cursos: {e}")
        return None

# --- Função Principal de Unificação ---
def main():
    print("Iniciando script de unificação de resultados (iterando por campus/ano)...")

    curso_info_map = get_curso_info_map()
    map_competencias_ce = load_json_safe(MAP_CE_JSON_PATH)
    map_competencias_fg = load_json_safe(MAP_FG_JSON_PATH)

    if not curso_info_map or not map_competencias_ce or not map_competencias_fg:
        print("ERRO CRÍTICO: Não foi possível carregar os mapas de curso ou competência. Encerrando.")
        return

    # Lista de campi disponíveis na pasta de Medias de Curso (CE)
    if not os.path.exists(MEDIAS_CE_CURSOS_PATH):
        print(f"ERRO: Pasta de médias por curso não encontrada: {MEDIAS_CE_CURSOS_PATH}")
        return

    campus_dirs = sorted([d for d in os.listdir(MEDIAS_CE_CURSOS_PATH) if os.path.isdir(os.path.join(MEDIAS_CE_CURSOS_PATH, d))])
    if not campus_dirs:
        print("Aviso: nenhum campus encontrado em MEDIAS_CE_CURSOS_PATH. Encerrando.")
        return

    for year in YEARS_TO_PROCESS:
        print(f"\n--- Processando Ano: {year} ---")
        ano_str = str(year)
        final_data_por_municipio_ANO = defaultdict(dict)

        # Carrega médias agregadas (UFC / UF / Região / Brasil) para o ano
        ufc_ce_data = load_json_safe(os.path.join(MEDIAS_CE_AGREGADAS_PATH, ano_str, 'medias_ufc_ce.json'))
        uf_ce_data = load_json_safe(os.path.join(MEDIAS_CE_AGREGADAS_PATH, ano_str, 'medias_uf_ce.json'))
        regiao_ce_data = load_json_safe(os.path.join(MEDIAS_CE_AGREGADAS_PATH, ano_str, 'medias_regiao_ce.json'))
        br_ce_data = load_json_safe(os.path.join(MEDIAS_CE_AGREGADAS_PATH, ano_str, 'medias_br_ce.json'))

        ufc_fg_data = load_json_safe(os.path.join(MEDIAS_FG_AGREGADAS_PATH, ano_str, 'medias_ufc_fg.json'))
        uf_fg_data = load_json_safe(os.path.join(MEDIAS_FG_AGREGADAS_PATH, ano_str, 'medias_uf_fg.json'))
        regiao_fg_data = load_json_safe(os.path.join(MEDIAS_FG_AGREGADAS_PATH, ano_str, 'medias_regiao_fg.json'))
        br_fg_data = load_json_safe(os.path.join(MEDIAS_FG_AGREGADAS_PATH, ano_str, 'medias_br_fg.json'))

        # carrega lista FG para o ano (uma vez)
        lista_fg_ano = []
        map_fg_ano_data = next((item for item in map_competencias_fg if str(item.get("ANO")) == ano_str), None)
        if map_fg_ano_data:
            lista_fg_ano = map_fg_ano_data.get("Formacao_geral", [])

        # Itera sobre os campi que têm pasta de médias de curso
        cursos_totais_no_ano = 0
        for campus_nome in campus_dirs:
            campus_path_ce = os.path.join(MEDIAS_CE_CURSOS_PATH, campus_nome, ano_str)
            campus_path_fg = os.path.join(MEDIAS_FG_CURSOS_PATH, campus_nome, ano_str)

            # verifica existência dos arquivos de medias do campus/ano
            curso_ce_file = os.path.join(campus_path_ce, 'medias_curso_ce.json')
            curso_fg_file = os.path.join(campus_path_fg, 'medias_curso_fg.json')

            if not os.path.exists(curso_ce_file) and not os.path.exists(curso_fg_file):
                # nada para esse campus neste ano
                # print(f"   → {campus_nome}: sem médias para {ano_str}, pulando.")
                continue

            # carrega (padrão: dict vazio)
            curso_ce_data = load_json_safe(curso_ce_file, {})
            curso_fg_data = load_json_safe(curso_fg_file, {})

            # junta chaves de CO_CURSO disponíveis (nas duas fontes)
            cursos_presentes = set(list(curso_ce_data.keys()) + list(curso_fg_data.keys()))
            if not cursos_presentes:
                continue

            final_data_por_municipio_ANO[campus_nome] = {}
            cursos_processados_campus = 0

            # Para cada CO_CURSO presente neste campus/ano, monta o objeto final
            for co_curso_str in sorted(cursos_presentes):
                # busca metadados do curso (município, CO_GRUPO, nome)
                curso_meta = curso_info_map.get(str(co_curso_str))
                if not curso_meta:
                    # se não tiver metadata, ainda assim podemos tentar incluir com CO_GRUPO desconhecido
                    # opcional: pular ou registrar aviso
                    print(f"   -> Aviso: CO_CURSO {co_curso_str} presente em {campus_nome}/{ano_str} mas não encontrado em cursos_ufc.csv. Pulando.")
                    continue

                co_grupo_str = str(curso_meta.get('CO_GRUPO'))
                nome_curso = curso_meta.get('Curso', 'Desconhecido')

                # --- CE ---
                desempenho_ce_final = {}
                lista_ce_ano = map_competencias_ce.get(co_grupo_str, {}).get('Componente_especifico', [])
                for comp_ce in lista_ce_ano:
                    c_data = curso_ce_data.get(co_curso_str, {}).get(comp_ce, {}) if curso_ce_data else {}
                    u_data = ufc_ce_data.get(co_grupo_str, {}).get(comp_ce, {}) if ufc_ce_data else {}
                    uf_data = uf_ce_data.get(co_grupo_str, {}).get(comp_ce, {}) if uf_ce_data else {}
                    r_data = regiao_ce_data.get(co_grupo_str, {}).get(comp_ce, {}) if regiao_ce_data else {}
                    b_data = br_ce_data.get(co_grupo_str, {}).get(comp_ce, {}) if br_ce_data else {}

                    comp_stats = {
                        "percentual_objetivas_curso": c_data.get("percentual_objetivas_curso"),
                        "media_discursivas_curso": c_data.get("media_discursivas_curso"),
                        "n_objetivas_validas_curso": c_data.get("n_objetivas_validas_curso"),
                        "n_discursivas_validas_curso": c_data.get("n_discursivas_validas_curso"),

                        "percentual_objetivas_ufc": u_data.get("percentual_objetivas_ufc"),
                        "media_discursivas_ufc": u_data.get("media_discursivas_ufc"),
                        "n_objetivas_validas_ufc": u_data.get("n_objetivas_validas_ufc"),
                        "n_discursivas_validas_ufc": u_data.get("n_discursivas_validas_ufc"),

                        "percentual_objetivas_uf": uf_data.get("percentual_objetivas_uf"),
                        "media_discursivas_uf": uf_data.get("media_discursivas_uf"),
                        "n_objetivas_validas_uf": uf_data.get("n_objetivas_validas_uf"),
                        "n_discursivas_validas_uf": uf_data.get("n_discursivas_validas_uf"),

                        "percentual_objetivas_regiao": r_data.get("percentual_objetivas_regiao"),
                        "media_discursivas_regiao": r_data.get("media_discursivas_regiao"),
                        "n_objetivas_validas_regiao": r_data.get("n_objetivas_validas_regiao"),
                        "n_discursivas_validas_regiao": r_data.get("n_discursivas_validas_regiao"),

                        "percentual_objetivas_br": b_data.get("percentual_objetivas_br"),
                        "media_discursivas_br": b_data.get("media_discursivas_br"),
                        "n_objetivas_validas_br": b_data.get("n_objetivas_validas_br"),
                        "n_discursivas_validas_br": b_data.get("n_discursivas_validas_br"),
                    }

                    final_comp_stats = {k: v for k, v in comp_stats.items() if v is not None}
                    if final_comp_stats:
                        desempenho_ce_final[comp_ce] = final_comp_stats

                # --- FG ---
                desempenho_fg_final = {}
                for comp_fg in lista_fg_ano:
                    c_data = curso_fg_data.get(co_curso_str, {}).get(comp_fg, {}) if curso_fg_data else {}
                    u_data = ufc_fg_data.get(comp_fg, {}) if ufc_fg_data else {}
                    uf_data = uf_fg_data.get(comp_fg, {}) if uf_fg_data else {}
                    r_data = regiao_fg_data.get(comp_fg, {}) if regiao_fg_data else {}
                    b_data = br_fg_data.get(comp_fg, {}) if br_fg_data else {}

                    comp_stats = {
                        "percentual_objetivas_curso": c_data.get("percentual_objetivas_curso"),
                        "media_discursivas_curso": c_data.get("media_discursivas_curso"),
                        "n_objetivas_validas_curso": c_data.get("n_objetivas_validas_curso"),
                        "n_discursivas_validas_curso": c_data.get("n_discursivas_validas_curso"),

                        "percentual_objetivas_ufc": u_data.get("percentual_objetivas_ufc"),
                        "media_discursivas_ufc": u_data.get("media_discursivas_ufc"),
                        "n_objetivas_validas_ufc": u_data.get("n_objetivas_validas_ufc"),
                        "n_discursivas_validas_ufc": u_data.get("n_discursivas_validas_ufc"),

                        "percentual_objetivas_uf": uf_data.get("percentual_objetivas_uf"),
                        "media_discursivas_uf": uf_data.get("media_discursivas_uf"),
                        "n_objetivas_validas_uf": uf_data.get("n_objetivas_validas_uf"),
                        "n_discursivas_validas_uf": uf_data.get("n_discursivas_validas_uf"),

                        "percentual_objetivas_regiao": r_data.get("percentual_objetivas_regiao"),
                        "media_discursivas_regiao": r_data.get("media_discursivas_regiao"),
                        "n_objetivas_validas_regiao": r_data.get("n_objetivas_validas_regiao"),
                        "n_discursivas_validas_regiao": r_data.get("n_discursivas_validas_regiao"),

                        "percentual_objetivas_br": b_data.get("percentual_objetivas_br"),
                        "media_discursivas_br": b_data.get("media_discursivas_br"),
                        "n_objetivas_validas_br": b_data.get("n_objetivas_validas_br"),
                        "n_discursivas_validas_br": b_data.get("n_discursivas_validas_br"),
                    }

                    final_comp_stats = {k: v for k, v in comp_stats.items() if v is not None}
                    if final_comp_stats:
                        desempenho_fg_final[comp_fg] = final_comp_stats

                if desempenho_ce_final or desempenho_fg_final:
                    final_data_por_municipio_ANO[campus_nome][co_curso_str] = {
                        "CO_GRUPO": co_grupo_str,
                        "NOME_CURSO": nome_curso,
                        "desempenho_CE": desempenho_ce_final,
                        "desempenho_FG": desempenho_fg_final
                    }
                    cursos_processados_campus += 1
                    cursos_totais_no_ano += 1

            print(f"   → Campus {campus_nome}: {cursos_processados_campus} cursos com dados em {ano_str}")

        print(f"   => Total de cursos processados no ano {ano_str}: {cursos_totais_no_ano}")

        # --- 4. Salvando arquivos de saída por campus (mesma lógica anterior) ---
        for campus_nome, cursos_data in final_data_por_municipio_ANO.items():
            campus_safe = campus_nome.replace(" ", "_").replace("/", "_")
            ce_outdir = os.path.join(OUTPUT_DT_BASE_PATH, campus_safe, ano_str)
            os.makedirs(ce_outdir, exist_ok=True)

            ce_path = os.path.join(ce_outdir, f'competencias_ce_{ano_str}.json')

            ce_data = {cid: d for cid, d in cursos_data.items() if d.get("desempenho_CE")}
            fg_data = {cid: d for cid, d in cursos_data.items() if d.get("desempenho_FG")}

            if ce_data:
                with open(ce_path, 'w', encoding='utf-8') as f:
                    json.dump(ce_data, f, ensure_ascii=False, indent=4)
                print(f"      -> CE salvo: {ce_path}")

    print("\nProcesso de unificação final por [campus/ano] concluído.")

if __name__ == '__main__':
    main()
