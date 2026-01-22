import os
import json
from config import FINAL_VG_JSON_PATH, FINAL_ESTRUTURA_JSON_PATH
from utils import load_json

OUTPUT_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_links_provas.json')
BACKUP_PATH = os.path.join('data', 'estrutura_links_provas_backup.json')

# NÃO PRECISA RODAR ESTE ARQUIVO 
def main():
    print("--- GERADOR DE TEMPLATE DE LINKS DE PROVAS ---")
    
    links_map = {}

    if not os.path.exists(FINAL_VG_JSON_PATH):
        print(f"Erro: Pasta de dados consolidados não encontrada: {FINAL_VG_JSON_PATH}")
        return

    # Itera sobre as pastas dos Campi
    campi_folders = [f for f in os.listdir(FINAL_VG_JSON_PATH) if os.path.isdir(os.path.join(FINAL_VG_JSON_PATH, f))]

    total_cursos = 0
    total_entradas = 0

    for campus in campi_folders:
        file_path = os.path.join(FINAL_VG_JSON_PATH, campus, 'visao_geral_consolidado.json')
        
        if os.path.exists(file_path):
            print(f"Lendo dados de: {campus}...")
            data = load_json(file_path)
            
            if data:
                for course_id, anos_data in data.items():
                    
                    # Se o curso ainda não está no mapa, inicializa
                    if course_id not in links_map:
                        links_map[course_id] = {}
                        total_cursos += 1
                        
                        # Tenta pegar o nome do curso para exibir no log
                        primeiro_ano = next(iter(anos_data.values()))
                        nome_curso = primeiro_ano.get('NO_CURSO', 'Desconhecido')
                        # print(f"   -> Encontrado: {course_id} - {nome_curso}")

                    # Para cada ano que esse curso tem dados
                    for year in anos_data.keys():
                        # Cria a chave do ano com valor vazio, apenas se ainda não existir
                        if year not in links_map[course_id]:
                            links_map[course_id][year] = "" 
                            total_entradas += 1

    # Ordena o JSON para ficar bonito (Curso ID -> Ano)
    sorted_links_map = {k: dict(sorted(v.items())) for k, v in sorted(links_map.items())}

    target_path = OUTPUT_PATH
    
    target_dir = os.path.dirname(target_path)
    if not os.path.exists(target_dir):
        print(f"Aviso: Diretório {target_dir} não encontrado. Salvando na pasta local.")
        target_path = BACKUP_PATH
    
    if os.path.exists(target_path):
        resp = input(f"O arquivo '{target_path}' já existe. Sobrescrever apaga todos os links preenchidos! Continuar? (s/n): ")
        if resp.lower() != 's':
            print("Operação cancelada.")
            return

    try:
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_links_map, f, indent=4)
        print(f"\nSucesso! Arquivo gerado em: {target_path}")
        print(f"Total de Cursos: {total_cursos}")
        print(f"Total de Campos para preencher: {total_entradas}")
        print("\nAgora abra o arquivo e cole os links das provas nos campos vazios (\"\").")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")

if __name__ == '__main__':
    main()