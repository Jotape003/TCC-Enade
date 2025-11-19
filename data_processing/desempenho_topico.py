import pandas as pd
import os
import json
from collections import defaultdict

# Importações de Configuração
from config import (
    YEARS_TO_PROCESS, FINAL_MEDIA_JSON_PATH, 
    FINAL_DT_JSON_PATH, # Caminho base de saída (Desempenho_Topico)
    FINAL_ESTRUTURA_JSON_PATH, CURSOS_CSV_PATH
)

# Importações do Utils
from data_processing.utils import load_json, save_json_safe

# --- Caminhos de ENTRADA de Estrutura ---
MAP_CE_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_competencias_final.json')
MAP_FG_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_fg_final.json')

# --- Caminhos de ENTRADA de Médias ---
MEDIAS_CE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'CE', 'Medias_agregadas')
MEDIAS_FG_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'FG', 'Medias_agregadas')
MEDIAS_CURSO_CE_BASE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'CE', 'Medias_Curso')
MEDIAS_CURSO_FG_BASE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'FG', 'Medias_Curso')

# --- Caminho de SAÍDA ---
OUTPUT_BASE_PATH = FINAL_DT_JSON_PATH


def load_course_metadata():
    if not os.path.exists(CURSOS_CSV_PATH):
        print(f"ERRO CRÍTICO: Arquivo '{CURSOS_CSV_PATH}' não encontrado.")
        return None
    try:
        use_cols = ['Código', 'CO_GRUPO', 'Município', 'Curso']
        df_cursos = pd.read_csv(CURSOS_CSV_PATH, sep=';', usecols=use_cols)
        df_cursos.dropna(subset=use_cols, inplace=True)
        
        df_cursos['Código'] = pd.to_numeric(df_cursos['Código'], errors='coerce').astype('Int64').astype(str)
        df_cursos['CO_GRUPO'] = pd.to_numeric(df_cursos['CO_GRUPO'], errors='coerce').astype(int).astype(str)
        df_cursos['Município'] = df_cursos['Município'].str.strip().str.title()
        df_cursos['Curso'] = df_cursos['Curso'].str.strip()
        
        df_cursos.dropna(subset=['Código', 'CO_GRUPO', 'Município', 'Curso'], inplace=True)
        df_cursos = df_cursos.drop_duplicates(subset=['Código'], keep='first')

        relevant_cursos_map = df_cursos.set_index('Código').to_dict(orient='index')
        print(f"Metadados carregados para {len(relevant_cursos_map)} cursos.")
        return relevant_cursos_map
    except Exception as e:
        print(f"Erro ao ler info dos cursos: {e}")
        return None

def load_all_media_data(year_str):
    data = {'ce': {}, 'fg': {}}
    files_map = {'ufc': 'medias_ufc', 'uf': 'medias_uf', 'regiao': 'medias_regiao', 'br': 'medias_br'}

    for scope, filename in files_map.items():
        path_ce = os.path.join(MEDIAS_CE_PATH, year_str, f'{filename}_ce.json')
        data['ce'][scope] = load_json(path_ce, f"{scope.upper()} CE") or {}
        
        path_fg = os.path.join(MEDIAS_FG_PATH, year_str, f'{filename}_fg.json')
        data['fg'][scope] = load_json(path_fg, f"{scope.upper()} FG") or {}
    return data

def get_stats_for_comp(comp_name, scope_data, scope_suffix, is_course_level=False):
    if not scope_data: return {}
    key_suffix = 'curso' if is_course_level else scope_suffix
    
    stats = {
        f"percentual_objetivas_{scope_suffix}": scope_data.get(f"percentual_objetivas_{key_suffix}"),
        f"media_discursivas_{scope_suffix}": scope_data.get(f"media_discursivas_{key_suffix}"),
        f"n_objetivas_validas_{scope_suffix}": scope_data.get(f"n_objetivas_validas_{key_suffix}"),
        f"n_discursivas_validas_{scope_suffix}": scope_data.get(f"n_discursivas_validas_{key_suffix}"),
    }
    # Retorna apenas se tiver algum valor válido
    if any(v is not None for v in stats.values()):
        return stats
    return {}

def main():
    print("--- INICIANDO: Unificação Final de Resultados ---")
    
    curso_info_map = load_course_metadata()
    map_competencias_ce = load_json(MAP_CE_JSON_PATH, "Mapas CE")
    map_competencias_fg = load_json(MAP_FG_JSON_PATH, "Mapas FG")

    if not all([curso_info_map, map_competencias_ce, map_competencias_fg]):
        return

    # --- 1. PRÉ-CARREGAMENTO DE DADOS DE CURSO (O Cache Agora Define Quem Participou) ---
    print("   Pré-carregando dados de Curso (CE e FG)...")
    # Estrutura: curso_data_cache[year][curso_id] = {'ce': {...}, 'fg': {...}}
    curso_data_cache = defaultdict(lambda: defaultdict(lambda: {'ce': {}, 'fg': {}}))
    
    for year in YEARS_TO_PROCESS:
        y_str = str(year)
        
        # Carrega CE
        if os.path.exists(MEDIAS_CURSO_CE_BASE_PATH):
            for campus in os.listdir(MEDIAS_CURSO_CE_BASE_PATH):
                p_campus = os.path.join(MEDIAS_CURSO_CE_BASE_PATH, campus, y_str)
                ce_file = os.path.join(p_campus, 'medias_curso_ce.json')
                ce_content = load_json(ce_file, "")
                if ce_content:
                    for cid, data in ce_content.items():
                        curso_data_cache[y_str][cid]['ce'] = data # Guarda dados do curso
        
        # Carrega FG
        if os.path.exists(MEDIAS_CURSO_FG_BASE_PATH):
            for campus in os.listdir(MEDIAS_CURSO_FG_BASE_PATH):
                p_campus = os.path.join(MEDIAS_CURSO_FG_BASE_PATH, campus, y_str)
                fg_file = os.path.join(p_campus, 'medias_curso_fg.json')
                fg_content = load_json(fg_file, "")
                if fg_content:
                    for cid, data in fg_content.items():
                        curso_data_cache[y_str][cid]['fg'] = data

    # --- 2. LOOP PRINCIPAL (Por Ano) ---
    for year in YEARS_TO_PROCESS:
        print(f"\n=== Processando Ano: {year} ===")
        ano_str = str(year)
        
        # Verifica se temos algum curso neste ano no cache. Se não, pula o ano.
        cursos_neste_ano = curso_data_cache[ano_str]
        if not cursos_neste_ano:
            print(f"   -> Sem dados de curso encontrados para {year}. Pulando.")
            continue

        # Carrega dados Agregados (BR, NE, UF) apenas se houver cursos
        agg_data = load_all_media_data(ano_str)
        
        # Prepara lista de Competências FG do ano
        lista_fg_ano = []
        map_fg_ano_data = next((item for item in map_competencias_fg if str(item.get("ANO")) == ano_str), None)
        if map_fg_ano_data:
            lista_fg_ano = map_fg_ano_data.get("Formacao_geral", [])

        final_data_por_municipio = defaultdict(dict)
        count_processed = 0

        # --- INVERSÃO DA LÓGICA: Itera APENAS sobre cursos que existem no CACHE ---
        for co_curso_str in cursos_neste_ano.keys():
            
            # 1. Lookup de Metadados (Nome, Grupo, Município)
            info = curso_info_map.get(co_curso_str)
            if not info:
                # Se o curso não está no CSV de metadados, ignoramos (dado órfão)
                # print(f"Aviso: Curso {co_curso_str} com dados mas sem metadados.")
                continue

            co_grupo_str = info.get('CO_GRUPO')
            municipio = info.get('Município', 'Indefinido')
            nome_curso = info.get('Curso')

            # 2. Recupera dados brutos do curso (do Cache)
            raw_curso_ce = cursos_neste_ano[co_curso_str]['ce']
            raw_curso_fg = cursos_neste_ano[co_curso_str]['fg']

            res_ce = {}
            res_fg = {}

            # --- PROCESSA CE ---
            lista_ce = map_competencias_ce.get(co_grupo_str, {}).get('Componente_especifico', [])
            
            for comp in lista_ce:
                curso_data = raw_curso_ce.get(comp, {})
                
                # Busca dados agregados (usando o Grupo do curso)
                uf_data = agg_data['ce']['uf'].get(co_grupo_str, {}).get(comp, {})
                regiao_data = agg_data['ce']['regiao'].get(co_grupo_str, {}).get(comp, {})
                br_data = agg_data['ce']['br'].get(co_grupo_str, {}).get(comp, {})
                ufc_data = agg_data['ce']['ufc'].get(co_grupo_str, {}).get(comp, {})

                comp_stats = {}
                comp_stats.update(get_stats_for_comp(comp, curso_data, 'curso', is_course_level=True))
                # Só adiciona comparativos se tiver dado do curso OU dado agregado
                if comp_stats or uf_data or regiao_data or br_data: 
                    comp_stats.update(get_stats_for_comp(comp, uf_data, 'uf'))
                    comp_stats.update(get_stats_for_comp(comp, regiao_data, 'regiao'))
                    comp_stats.update(get_stats_for_comp(comp, br_data, 'br'))
                    comp_stats.update(get_stats_for_comp(comp, ufc_data, 'ufc'))
                    
                    if comp_stats: res_ce[comp] = comp_stats

            # --- PROCESSA FG ---
            for comp in lista_fg_ano:
                curso_data = raw_curso_fg.get(comp, {})
                
                uf_data = agg_data['fg']['uf'].get(comp, {})
                regiao_data = agg_data['fg']['regiao'].get(comp, {})
                br_data = agg_data['fg']['br'].get(comp, {})
                ufc_data = agg_data['fg']['ufc'].get(comp, {})

                comp_stats = {}
                comp_stats.update(get_stats_for_comp(comp, curso_data, 'curso', is_course_level=True))
                
                if comp_stats or uf_data or regiao_data or br_data:
                    comp_stats.update(get_stats_for_comp(comp, uf_data, 'uf'))
                    comp_stats.update(get_stats_for_comp(comp, regiao_data, 'regiao'))
                    comp_stats.update(get_stats_for_comp(comp, br_data, 'br'))
                    comp_stats.update(get_stats_for_comp(comp, ufc_data, 'ufc'))
                
                    if comp_stats: res_fg[comp] = comp_stats

            # Se montou algum objeto de resultado, adiciona ao município
            if res_ce or res_fg:
                final_data_por_municipio[municipio][co_curso_str] = {
                    "CO_GRUPO": co_grupo_str,
                    "NOME_CURSO": nome_curso,
                    "desempenho_CE": res_ce,
                    "desempenho_FG": res_fg
                }
                count_processed += 1

        print(f"   -> Processados {count_processed} cursos ativos em {year}.")

        # --- SALVAMENTO (Agrupado por Município) ---
        for municipio, cursos_data in final_data_por_municipio.items():
            municipio_safe = municipio.replace(" ", "_").replace("/", "_")
            
            # Opcional: Separar CE e FG em arquivos diferentes se desejar
            # Aqui estou salvando o UNIFICADO como no seu último pedido
            # Se quiser separado, basta filtrar o dict 'cursos_data'
            
            data_unificado = {}
            for cid, cdata in cursos_data.items():
                 entry = {
                     "CO_GRUPO": cdata["CO_GRUPO"],
                     "NOME_CURSO": cdata["NOME_CURSO"]
                 }
                 if cdata["desempenho_CE"]: entry["desempenho_CE"] = cdata["desempenho_CE"]
                 if cdata["desempenho_FG"]: entry["desempenho_FG"] = cdata["desempenho_FG"]
                 data_unificado[cid] = entry

            if data_unificado:
                # Caminho: .../Desempenho_Topico/{MUNICIPIO}/{ANO}/competencias_{ANO}.json
                path = os.path.join(OUTPUT_BASE_PATH, municipio_safe, ano_str, f'competencias_{ano_str}.json')
                save_json_safe(data_unificado, path, f"Unificado {municipio}")

    print("\n--- Unificação Final Concluída ---")

if __name__ == '__main__':
    main()