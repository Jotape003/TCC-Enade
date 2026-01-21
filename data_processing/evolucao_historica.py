import os
import json
from collections import defaultdict
from config import YEARS_TO_PROCESS, FINAL_VG_JSON_PATH, FINAL_EH_JSON_PATH
from utils import load_json

def main():
    print("--- INICIANDO: Geração de Evolução Histórica ---")

    campus_folders = [
        d for d in os.listdir(FINAL_VG_JSON_PATH) 
        if os.path.isdir(os.path.join(FINAL_VG_JSON_PATH, d))
    ]

    for campus_name in campus_folders:
        print(f"\nProcessando Campus: {campus_name}")
        campus_path_vg = os.path.join(FINAL_VG_JSON_PATH, campus_name)
        
        historico_por_curso = defaultdict(list)

        for year in sorted(YEARS_TO_PROCESS):
            visao_geral_path = os.path.join(campus_path_vg, f'visao_geral_{year}.json')
            dados_ano = load_json(visao_geral_path)

            if not dados_ano:
                continue

            for curso in dados_ano:
                co_curso = str(curso['CO_CURSO'])
                
                entry = {
                    "ano": str(year),
                    "nota_geral": curso.get('nota_geral_media_curso'),
                    "nota_fg": curso.get('nota_fg_media_curso'),
                    "nota_ce": curso.get('nota_ce_media_curso'),

                    "ufc_geral": curso.get('media_ufc_geral'),
                    "ufc_fg": curso.get('media_ufc_fg'),
                    "ufc_ce": curso.get('media_ufc_ce'),

                    "nacional_geral": curso.get('media_nacional_geral'),
                    "nacional_fg": curso.get('media_nacional_fg'),
                    "nacional_ce": curso.get('media_nacional_ce'),

                    "regiao_geral": curso.get('media_regiao_geral'),
                    "regiao_fg": curso.get('media_regiao_fg'),
                    "regiao_ce": curso.get('media_regiao_ce'),

                    "uf_geral": curso.get('media_uf_geral'),
                    "uf_fg": curso.get('media_uf_fg'),
                    "uf_ce": curso.get('media_uf_ce')
                }
                
                historico_por_curso[co_curso].append(entry)

        if historico_por_curso:
            output_dir = os.path.join(FINAL_EH_JSON_PATH, campus_name)
            
            os.makedirs(output_dir, exist_ok=True)
            
            output_path = os.path.join(output_dir, 'evolucao_historica.json')
            
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(historico_por_curso, f, ensure_ascii=False, indent=4)
                print(f"  -> Histórico salvo em: {output_path}")
            except Exception as e:
                print(f"  -> ERRO ao salvar histórico: {e}")

    print("\nProcesso concluído.")

if __name__ == '__main__':
    main()