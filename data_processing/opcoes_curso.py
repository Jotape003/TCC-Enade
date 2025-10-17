import os
import json
from config import FINAL_JSON_PATH, YEARS_TO_PROCESS

def main():
    opcoes_filtro = {
        "anos": YEARS_TO_PROCESS,
        "campi": {}
    }

    campus_folders = [d for d in os.listdir(FINAL_JSON_PATH) if os.path.isdir(os.path.join(FINAL_JSON_PATH, d))]

    for campus_name in campus_folders:
        opcoes_filtro["campi"][campus_name] = {"cursos": []}

        for year in YEARS_TO_PROCESS:
            json_path = os.path.join(FINAL_JSON_PATH, campus_name, f'visao_geral_{year}.json')
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    dados_analise = json.load(f)
                    
                # Extrai a lista de cursos (código e nome) para este campus
                cursos_do_campus = [
                    {"codigo": curso["CO_CURSO"], "nome": curso["NO_CURSO"]}
                    for curso in dados_analise
                ]
                opcoes_filtro["campi"][campus_name]["cursos"] = sorted(cursos_do_campus, key=lambda c: c['nome'])
                break 

    output_path = os.path.join(FINAL_JSON_PATH, 'opcoes_filtro.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(opcoes_filtro, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()