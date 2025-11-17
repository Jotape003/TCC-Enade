import os
import json

from config import (
    RAW_DATA_PATH, YEARS_TO_PROCESS, FINAL_MEDIA_JSON_PATH, 
    FINAL_ESTRUTURA_JSON_PATH, REGIAO_CODE
)

from .utils import (
    load_json, get_relevant_grupos, 
    calculate_averages_competencia, save_json_safe
)

MAP_CE_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_competencias_final.json')
MAP_FG_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_fg_final.json')

BASE_CE_OUTPUT_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'CE', 'Medias_Agregadas')
BASE_FG_OUTPUT_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'FG', 'Medias_Agregadas')


def run_calculation_regiao():
    print("Iniciando cálculo de médias REGIONAIS (NE)...")
    
    relevant_grupos = get_relevant_grupos()
    maps = {
        'ce': load_json(MAP_CE_JSON_PATH, "Mapeamento de Competências CE"),
        'fg': load_json(MAP_FG_JSON_PATH, "Mapeamento de Competências FG")
    }
    
    if relevant_grupos is None or not maps['ce'] or not maps['fg']:
        print("Encerrando script devido a erro ao obter arquivos de mapeamento.")
        return

    for year in YEARS_TO_PROCESS:
        config_ne = {
            "year": year,
            "year_path": os.path.join(RAW_DATA_PATH, f'enade_{year}'),
            "maps": maps,
            "json_suffix": "regiao",     # Sufixo do seu script original
            "group_by_curso": False,     # Agrega por CO_GRUPO
            "filter_col": "CO_REGIAO_CURSO", # Coluna para filtrar
            "filter_val": REGIAO_CODE,                 # Valor (2 = Nordeste)
            "info_col_variants": {'CO_REGIAO_CURSO': ['CO_REGIAO_CURSO', '"CO_REGIAO_CURSO"']},
            "relevant_grupos": relevant_grupos,
        }
        
        medias_ce_ano, medias_fg_ano = calculate_averages_competencia(config_ne) 
        
        ano_str = str(year)
        if medias_ce_ano:
            data_to_save_ce = {str(k): v for k, v in medias_ce_ano.items()}
            output_path_ce = os.path.join(BASE_CE_OUTPUT_PATH, ano_str, 'medias_regiao_ce.json')
            save_json_safe(data_to_save_ce, output_path_ce, f"Médias CE (NE) de {year}")
        else:
            print(f"   -> Aviso: Não foram calculadas médias CE (NE) para {year}.")

        if medias_fg_ano:
            data_to_save_fg = {str(k): v for k, v in medias_fg_ano.items()}
            output_path_fg = os.path.join(BASE_FG_OUTPUT_PATH, ano_str, 'medias_regiao_fg.json')
            save_json_safe(data_to_save_fg, output_path_fg, f"Médias FG (NE) de {year}")
        else:
            print(f"   -> Aviso: Não foram calculadas médias FG (NE) para {year}.")

    print("\nProcesso de geração de médias Regionais (NE) por ano concluído.")

if __name__ == '__main__':
    run_calculation_regiao()