import os
import json

from config import (
    RAW_DATA_PATH, YEARS_TO_PROCESS, FINAL_MEDIA_JSON_PATH, 
    FINAL_ESTRUTURA_JSON_PATH
)

from utils import (
    load_json, get_relevant_grupos, 
    calculate_averages_competencia, save_json_safe
)

MAP_CE_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_competencias_final.json')
MAP_FG_JSON_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_fg_final.json')

BASE_CE_OUTPUT_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'CE', 'Medias_Agregadas')

BASE_FG_OUTPUT_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Desempenho_Topico', 'FG', 'Medias_Agregadas')


def run_calculation_br():
    print("Iniciando cálculo de médias NACIONAIS (BR)...")

    relevant_grupos = get_relevant_grupos()
    maps = {
        'ce': load_json(MAP_CE_JSON_PATH),
        'fg': load_json(MAP_FG_JSON_PATH)
    }

    for year in YEARS_TO_PROCESS:
        
        config_br = {
            "year": year,
            "year_path": os.path.join(RAW_DATA_PATH, f'enade_{year}'),
            "maps": maps,
            "json_suffix": "br",
            "group_by_curso": False,
            "filter_col": None,
            "filter_val": None,
            "info_col_variants": {},
            "relevant_grupos": relevant_grupos,
        }
        
        medias_ce_ano, medias_fg_ano = calculate_averages_competencia(config_br) 
        
        ano_str = str(year)
        if medias_ce_ano:
            data_to_save_ce = {str(k): v for k, v in medias_ce_ano.items()}
            output_path_ce = os.path.join(BASE_CE_OUTPUT_PATH, ano_str, 'medias_br_ce.json')
            save_json_safe(data_to_save_ce, output_path_ce, f"Médias CE (BR) de {year}")
        else:
            print(f"   -> Aviso: Não foram calculadas médias CE (BR) para {year}.")

        if medias_fg_ano:
            data_to_save_fg = {str(k): v for k, v in medias_fg_ano.items()}
            output_path_fg = os.path.join(BASE_FG_OUTPUT_PATH, ano_str, 'medias_br_fg.json')
            save_json_safe(data_to_save_fg, output_path_fg, f"Médias FG (BR) de {year}")
        else:
            print(f"   -> Aviso: Não foram calculadas médias FG (BR) para {year}.")

    print("\nProcesso de geração de médias Nacionais (BR) por ano concluído.")

if __name__ == '__main__':
    run_calculation_br()