import os
import json
from config import FINAL_VG_JSON_PATH, FINAL_ESTRUTURA_JSON_PATH
from utils import load_json

OUTPUT_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_links_provas.json')

def main():
    print("--- GERADOR DE TEMPLATE DE LINKS DE PROVAS ---")
    
    links_map = {}
    
    # 1. Verifica se o diretório base existe
    if not os.path.exists(FINAL_VG_JSON_PATH):
        print(f"Erro: Pasta de dados consolidados não encontrada: {FINAL_VG_JSON_PATH}")
        return

    # 2. Itera sobre as pastas dos Campi (Crateus, Fortaleza, etc.)
    campi_folders = [f for f in os.listdir(FINAL_VG_JSON_PATH) if os.path.isdir(os.path.join(FINAL_VG_JSON_PATH, f))]

    total_cursos = 0
    total_entradas = 0

    for campus in campi_folders:
        file_path = os.path.join(FINAL_VG_JSON_PATH, campus, 'visao_geral_consolidado.json')
        
        if os.path.exists(file_path):
            print(f"Lendo dados de: {campus}...")
            data = load_json(file_path)
            
            if data:
                # data estrutura: { "ID_CURSO": { "ANO": { ...dados... }, "ANO2": ... } }
                for course_id, anos_data in data.items():
                    
                    # Se o curso ainda não está no mapa, inicializa
                    if course_id not in links_map:
                        links_map[course_id] = {}
                        total_cursos += 1
                        
                        # (Opcional) Tenta pegar o nome do curso para exibir no log
                        # Isso ajuda você a saber qual ID é qual curso enquanto roda o script
                        primeiro_ano = next(iter(anos_data.values()))
                        nome_curso = primeiro_ano.get('NO_CURSO', 'Desconhecido')
                        # print(f"   -> Encontrado: {course_id} - {nome_curso}")

                    # Para cada ano que esse curso tem dados
                    for year in anos_data.keys():
                        # Cria a chave do ano com valor vazio, APENAS se ainda não existir
                        # Isso preserva links se você rodar o script novamente em cima de um arquivo já preenchido
                        if year not in links_map[course_id]:
                            links_map[course_id][year] = "" 
                            total_entradas += 1

    # 3. Ordena o JSON para ficar bonito (Curso ID -> Ano)
    # A ordenação das chaves ajuda muito na hora de preencher manualmente
    sorted_links_map = {k: dict(sorted(v.items())) for k, v in sorted(links_map.items())}

    # 4. Salva o arquivo
    target_path = OUTPUT_PATH
    
    # Verifica se o diretório de destino existe, senão salva na pasta local
    target_dir = os.path.dirname(target_path)
    if not os.path.exists(target_dir):
        print(f"Aviso: Diretório {target_dir} não encontrado. Salvando na pasta local.")
        target_path = BACKUP_PATH

    # Modo de escrita: 'w' sobrescreve. 
    # DICA: Se você já tiver preenchido alguns links e quiser apenas ATUALIZAR
    # novos cursos sem apagar os antigos, precisaria carregar o json existente antes.
    # Por segurança, este script cria um NOVO arquivo ou sobrescreve se você confirmar.
    
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