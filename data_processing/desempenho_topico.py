import pandas as pd
import os
import json
from collections import defaultdict

from config import (
    YEARS_TO_PROCESS, FINAL_MEDIA_JSON_PATH, 
    FINAL_DT_JSON_PATH,
    FINAL_ESTRUTURA_JSON_PATH, CURSOS_CSV_PATH
)

from utils import load_json, save_json_safe

MAP_CE_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_competencias_final.json')
MAP_FG_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_fg_final.json')

PATH_DISTRIBUICAO_CE = os.path.join(FINAL_MEDIA_JSON_PATH, 'Estatisticas_Prova', 'distribuicao_questoes_ce.json')
PATH_DISTRIBUICAO_FG = os.path.join(FINAL_MEDIA_JSON_PATH, 'Estatisticas_Prova', 'distribuicao_questoes_fg.json')

MEDIAS_AG_CE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'CE', 'Medias_agregadas')
MEDIAS_AG_FG_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'FG', 'Medias_agregadas')
MEDIAS_CURSO_CE_BASE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'CE', 'Medias_Curso')
MEDIAS_CURSO_FG_BASE_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'FG', 'Medias_Curso')

OUTPUT_BASE_PATH = FINAL_DT_JSON_PATH


def load_course_metadata():
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
        path_ce = os.path.join(MEDIAS_AG_CE_PATH, year_str, f'{filename}_ce.json')
        data['ce'][scope] = load_json(path_ce) or {}
        
        path_fg = os.path.join(MEDIAS_AG_FG_PATH, year_str, f'{filename}_fg.json')
        data['fg'][scope] = load_json(path_fg) or {}
        
    return data

def get_stats_for_comp(comp_name, scope_data, scope_suffix, is_course_level=False, dados_questoes=None):
    if not scope_data: return {}
    key_suffix = 'curso' if is_course_level else scope_suffix
    
    stats = {
        f"percentual_objetivas_{scope_suffix}": scope_data.get(f"percentual_objetivas_{key_suffix}"),
        f"media_discursivas_{scope_suffix}": scope_data.get(f"media_discursivas_{key_suffix}")
    }
    
    if is_course_level and dados_questoes:
        stats["quantidade_questoes_total"] = dados_questoes.get('total', 0)
        
        l_obj = dados_questoes.get('lista_obj', [])
        if l_obj: stats["lista_questoes_objetivas"] = l_obj
            
        l_disc = dados_questoes.get('lista_disc', [])
        if l_disc: stats["lista_questoes_discursivas"] = l_disc

    vals = [v for k, v in stats.items() if "questoes" not in k]
    if any(v is not None for v in vals):
        return stats
    return {}

def main():
    print("--- INICIANDO: Unificação Final de Resultados (Refatorado) ---")
    
    curso_info_map = load_course_metadata()
    map_competencias_ce = load_json(MAP_CE_JSON_PATH) or {}
    map_competencias_fg = load_json(MAP_FG_JSON_PATH) or {}
    
    # Carrega Distribuição Detalhada de Questões
    dist_questoes_ce = load_json(PATH_DISTRIBUICAO_CE) or {}
    dist_questoes_fg = load_json(PATH_DISTRIBUICAO_FG) or {}

    if not all([curso_info_map, map_competencias_ce, map_competencias_fg]):
        print(" -> Faltando arquivos essenciais. Encerrando.")
        return

    print("   Pré-carregando dados de Curso (CE e FG)...")
    curso_data_cache = defaultdict(lambda: defaultdict(lambda: {'ce': {}, 'fg': {}}))
    
    for year in YEARS_TO_PROCESS:
        y_str = str(year)
        
        # Carrega caches de CE
        if os.path.exists(MEDIAS_CURSO_CE_BASE_PATH):
            for campus in os.listdir(MEDIAS_CURSO_CE_BASE_PATH):
                p_campus = os.path.join(MEDIAS_CURSO_CE_BASE_PATH, campus, y_str)
                ce_file = os.path.join(p_campus, 'medias_curso_ce.json')
                # Load JSON sem description
                ce_content = load_json(ce_file)
                if ce_content:
                    for cid, data in ce_content.items():
                        curso_data_cache[y_str][cid]['ce'] = data 
        
        # Carrega caches de FG
        if os.path.exists(MEDIAS_CURSO_FG_BASE_PATH):
            for campus in os.listdir(MEDIAS_CURSO_FG_BASE_PATH):
                p_campus = os.path.join(MEDIAS_CURSO_FG_BASE_PATH, campus, y_str)
                fg_file = os.path.join(p_campus, 'medias_curso_fg.json')
                # Load JSON sem description
                fg_content = load_json(fg_file)
                if fg_content:
                    for cid, data in fg_content.items():
                        curso_data_cache[y_str][cid]['fg'] = data

    # 3. LOOP PRINCIPAL (Por Ano)
    for year in YEARS_TO_PROCESS:
        print(f"\n=== Processando Ano: {year} ===")
        ano_str = str(year)
        
        # Verifica se existem cursos processados para este ano
        cursos_neste_ano = curso_data_cache[ano_str]
        if not cursos_neste_ano:
            print(f"   -> Sem dados de curso encontrados para {year}. Pulando.")
            continue

        # Carrega Agregados
        agg_data = load_all_media_data(ano_str)
        
        # Prepara lista FG
        lista_fg_ano = []
        # FG geralmente é uma lista de anos no JSON
        map_fg_ano_data = next((item for item in map_competencias_fg if str(item.get("ANO")) == ano_str), None)
        if map_fg_ano_data:
            lista_fg_ano = map_fg_ano_data.get("Formacao_geral", [])

        final_data_por_municipio = defaultdict(dict)
        count_processed = 0

        # --- Itera APENAS sobre cursos que existem no CACHE deste ano ---
        for co_curso_str in cursos_neste_ano.keys():
            
            # Lookup de Metadados
            info = curso_info_map.get(co_curso_str)
            if not info: 
                # Curso com nota mas sem metadados no CSV? Ignora.
                continue

            co_grupo_str = info.get('CO_GRUPO')
            municipio = info.get('Município', 'Indefinido')
            nome_curso = info.get('Curso')

            raw_curso_ce = cursos_neste_ano[co_curso_str]['ce']
            raw_curso_fg = cursos_neste_ano[co_curso_str]['fg']

            res_ce = {}
            res_fg = {}

            # --- PROCESSA CE ---
            lista_ce = map_competencias_ce.get(co_grupo_str, {}).get('Componente_especifico', [])
            
            contagem_ce_detalhada = dist_questoes_ce.get(str(co_grupo_str), {}).get(ano_str, {})

            for comp in lista_ce:
                c_data = raw_curso_ce.get(comp, {})
                uf_data = agg_data['ce']['uf'].get(co_grupo_str, {}).get(comp, {})
                regiao_data = agg_data['ce']['regiao'].get(co_grupo_str, {}).get(comp, {})
                br_data = agg_data['ce']['br'].get(co_grupo_str, {}).get(comp, {})
                ufc_data = agg_data['ce']['ufc'].get(co_grupo_str, {}).get(comp, {}) 

                # Pega dados das questões para este tópico específico
                dados_questoes = contagem_ce_detalhada.get(comp)

                comp_stats = {}
                # Injeta dados_questoes no nível do curso
                comp_stats.update(get_stats_for_comp(comp, c_data, 'curso', is_course_level=True, dados_questoes=dados_questoes))
                
                if comp_stats or uf_data or regiao_data or br_data: 
                    comp_stats.update(get_stats_for_comp(comp, uf_data, 'uf'))
                    comp_stats.update(get_stats_for_comp(comp, regiao_data, 'regiao'))
                    comp_stats.update(get_stats_for_comp(comp, br_data, 'br'))
                    comp_stats.update(get_stats_for_comp(comp, ufc_data, 'ufc'))
                    
                    if comp_stats: res_ce[comp] = comp_stats

            # --- PROCESSA FG ---
            # Busca distribuição FG (Nacional, chave é apenas o ano)
            contagem_fg_detalhada = dist_questoes_fg.get(ano_str, {})

            for comp in lista_fg_ano:
                c_data = raw_curso_fg.get(comp, {})
                uf_data = agg_data['fg']['uf'].get(comp, {})
                regiao_data = agg_data['fg']['regiao'].get(comp, {})
                br_data = agg_data['fg']['br'].get(comp, {})
                ufc_data = agg_data['fg']['ufc'].get(comp, {}) 

                # Pega dados das questões FG
                dados_questoes = contagem_fg_detalhada.get(comp)

                comp_stats = {}
                comp_stats.update(get_stats_for_comp(comp, c_data, 'curso', is_course_level=True, dados_questoes=dados_questoes))
                
                if comp_stats or uf_data or regiao_data or br_data:
                    comp_stats.update(get_stats_for_comp(comp, uf_data, 'uf'))
                    comp_stats.update(get_stats_for_comp(comp, regiao_data, 'regiao'))
                    comp_stats.update(get_stats_for_comp(comp, br_data, 'br'))
                    comp_stats.update(get_stats_for_comp(comp, ufc_data, 'ufc'))
                
                    if comp_stats: res_fg[comp] = comp_stats

            # Adiciona ao buffer do município se tiver dados
            if res_ce or res_fg:
                final_data_por_municipio[municipio][co_curso_str] = {
                    "CO_GRUPO": co_grupo_str,
                    "NOME_CURSO": nome_curso,
                    "desempenho_CE": res_ce,
                    "desempenho_FG": res_fg
                }
                count_processed += 1

        print(f"   -> Processados {count_processed} cursos ativos.")

        # --- SALVAMENTO ---
        for municipio, cursos_data in final_data_por_municipio.items():
            municipio_safe = municipio.replace(" ", "_").replace("/", "_")
            
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
                # Salva no caminho final
                path = os.path.join(OUTPUT_BASE_PATH, municipio_safe, ano_str, f'competencias_{ano_str}.json')
                save_json_safe(data_unificado, path, f"Unificado {municipio}")

    print("\n--- Unificação Final Concluída ---")

if __name__ == '__main__':
    main()