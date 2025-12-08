import os
import json
from ..config import FINAL_JSON_PATH, YEARS_TO_PROCESS, CAMPUS_MAP

def main():
    opcoes_filtro = {
        "anos": sorted(YEARS_TO_PROCESS, reverse=True),
        "campi": sorted(list(CAMPUS_MAP.values())),
        "cursosPorAnoECampus": {}
    }

    for year in YEARS_TO_PROCESS:
        opcoes_filtro["cursosPorAnoECampus"][year] = {}
        for campus_name in opcoes_filtro["campi"]:
            opcoes_filtro["cursosPorAnoECampus"][year][campus_name] = []
            
            json_path = os.path.join(FINAL_JSON_PATH, campus_name, f'visao_geral_{year}.json')
            
            if os.path.exists(json_path):
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        dados_ano_campus = json.load(f)
                    
                    cursos_do_ano = []
                    for curso in dados_ano_campus:
                        cursos_do_ano.append({
                            "codigo": curso["CO_CURSO"],
                            "nome": curso["NO_CURSO"]
                        })
                    
                    opcoes_filtro["cursosPorAnoECampus"][year][campus_name] = sorted(cursos_do_ano, key=lambda c: c['nome'])

                except Exception as e:
                    print(f"  -> Aviso: Erro ao ler {json_path}. Erro: {e}")

    output_path = os.path.join(FINAL_JSON_PATH, 'opcoes_filtro.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(opcoes_filtro, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()