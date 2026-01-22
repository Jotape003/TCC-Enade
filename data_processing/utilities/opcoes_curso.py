import os
import json
from config import FINAL_VG_JSON_PATH, YEARS_TO_PROCESS, CAMPUS_MAP

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

    for campus_name in opcoes_filtro["campi"]:
        json_path = os.path.join(FINAL_VG_JSON_PATH, campus_name, 'visao_geral_consolidado.json')
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    dados_consolidado = json.load(f)
                
                for co_curso, anos_data in dados_consolidado.items():
                    primeiro_ano_disponivel = next(iter(anos_data.values()))
                    nome_curso = primeiro_ano_disponivel.get("NO_CURSO", "Nome Desconhecido")

                    for year in anos_data.keys():
                        if year in YEARS_TO_PROCESS:
                            opcoes_filtro["cursosPorAnoECampus"][str(year)][campus_name].append({
                                "codigo": co_curso, 
                                "nome": nome_curso
                            })
            
            except Exception as e:
                print(f"  -> Erro ao processar {campus_name}: {e}")
        else:
            print(f"  -> Aviso: Arquivo não encontrado para {campus_name}: {json_path}")

    for year in opcoes_filtro["cursosPorAnoECampus"]:
        for campus in opcoes_filtro["cursosPorAnoECampus"][year]:
            lista = opcoes_filtro["cursosPorAnoECampus"][year][campus]
            opcoes_filtro["cursosPorAnoECampus"][year][campus] = sorted(lista, key=lambda c: c['nome'])

    from config import JSON_DATA_PATH 
    output_path = os.path.join(JSON_DATA_PATH, 'opcoes_filtro.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(opcoes_filtro, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()