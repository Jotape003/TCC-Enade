import pandas as pd
import os
import json

from ..config import YEARS_TO_PROCESS, FINAL_JSON_PATH

# Caminhos e nomes de colunas
CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv')
COLUNA_CODIGO_CURSO = 'Código'
COLUNA_CO_GRUPO = 'CO_GRUPO'
COLUNA_NOME_CURSO = 'Curso'
COLUNA_GRAU = 'Grau'
OUTPUT_JSON_FILENAME = 'estrutura_competencias_final.json' # Novo nome

# --- Placeholders (Ajustados para CE) ---
# Contagem das questões FG (usaremos para saber onde começam as CE)
FG_DISC_COUNT = 2
FG_OBJ_COUNT = 8
# Contagem das questões CE
CE_DISC_COUNT = 3
CE_OBJ_COUNT = 27

def gerar_placeholders_ce(prefixo, inicio_num, count):
    """Gera placeholders apenas para questões CE."""
    # Ex: prefixo='d', inicio_num=3, count=3 => {'d3': '', 'd4': '', 'd5': ''}
    # Ex: prefixo='q', inicio_num=9, count=27 => {'q9': '', ..., 'q35': ''}
    return {f"{prefixo}{i}": 1 for i in range(inicio_num, inicio_num + count)}

def main():
    """
    Gera JSON esqueleto simplificado com mapeamento de questões CE
    no nível do CO_GRUPO e ano.
    """
    if not os.path.exists(CURSOS_CSV_PATH):
        print(f"ERRO: Arquivo '{CURSOS_CSV_PATH}' não encontrado.")
        return

    try:
        # Lê o CSV (ajuste o separador se necessário)
        df_cursos = pd.read_csv(CURSOS_CSV_PATH, sep=';', encoding='utf-8')
        print(f"Arquivo '{CURSOS_CSV_PATH}' lido com sucesso.")

        required_cols = [COLUNA_CODIGO_CURSO, COLUNA_CO_GRUPO, COLUNA_NOME_CURSO, COLUNA_GRAU]
        if not all(col in df_cursos.columns for col in required_cols):
            missing = [col for col in required_cols if col not in df_cursos.columns]
            print(f"ERRO: Colunas ausentes no CSV: {missing}. Verifique o arquivo.")
            return

        # Limpa e garante tipos
        df_cursos[COLUNA_CODIGO_CURSO] = pd.to_numeric(df_cursos[COLUNA_CODIGO_CURSO], errors='coerce').astype('Int64')
        df_cursos[COLUNA_CO_GRUPO] = pd.to_numeric(df_cursos[COLUNA_CO_GRUPO], errors='coerce').astype('Int64')
        df_cursos = df_cursos.dropna(subset=[COLUNA_CODIGO_CURSO, COLUNA_CO_GRUPO, COLUNA_NOME_CURSO, COLUNA_GRAU])
        df_cursos[COLUNA_NOME_CURSO] = df_cursos[COLUNA_NOME_CURSO].astype(str)
        df_cursos[COLUNA_GRAU] = df_cursos[COLUNA_GRAU].astype(str).str.strip().str.capitalize()

    except Exception as e:
         print(f"Erro ao ler ou processar o arquivo CSV: {e}")
         return

    output_data = {}
    grupos = df_cursos.groupby(COLUNA_CO_GRUPO)

    print("Agrupando cursos por CO_GRUPO e gerando estrutura simplificada...")
    for co_grupo, cursos_do_grupo in grupos:
        co_grupo_int = int(co_grupo)
        co_grupo_str = str(co_grupo_int)

        # Cria a estrutura de anos usando TODOS os anos da lista global
        anos_estrutura_grupo = {}
        anos_ordenados_global = sorted(YEARS_TO_PROCESS)
        for year in anos_ordenados_global:
            anos_estrutura_grupo[str(year)] = {
                "questoes_CE": { # Renomeado para clareza
                    # Placeholders apenas para questões CE
                    "discursivas": gerar_placeholders_ce("d", FG_DISC_COUNT + 1, CE_DISC_COUNT),
                    "objetivas": gerar_placeholders_ce("q", FG_OBJ_COUNT + 1, CE_OBJ_COUNT)
                }
            }

        # Cria a estrutura principal para o CO_GRUPO
        output_data[co_grupo_str] = {
            "Nome_Area": f"Área CO_GRUPO {co_grupo_str}",
            "Componente_especifico": [], # Lista de Tópicos (manual)
            "Cursos": [], # Lista simples de cursos
            "Anos": anos_estrutura_grupo # Mapeamento de questões CE por ano
        }

        # Adiciona a lista de cursos (código, nome, grau)
        for index, row in cursos_do_grupo.iterrows():
            output_data[co_grupo_str]["Cursos"].append({
                "codigo": int(row[COLUNA_CODIGO_CURSO]),
                "nome": row[COLUNA_NOME_CURSO],
                "grau": row[COLUNA_GRAU]
            })
        output_data[co_grupo_str]["Cursos"].sort(key=lambda x: x['nome'])

    # Salva o JSON final
    os.makedirs(FINAL_JSON_PATH, exist_ok=True)
    output_path = os.path.join(FINAL_JSON_PATH, OUTPUT_JSON_FILENAME)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)
        print(f"\nSucesso! Estrutura JSON simplificada salva em '{output_path}'")
        print("Edite este arquivo para adicionar:")
        print("  - 'Nome_Area'.")
        print("  - A lista 'Componente_especifico' para cada grupo.")
        print("  - Substitua os placeholders em 'Anos' -> 'questoes_CE' pelo nome do tópico.")
        print("  - Remova/ignore os objetos de ano não aplicáveis a cada CO_GRUPO.")
    except Exception as e:
        print(f"ERRO ao salvar o JSON: {e}")

if __name__ == '__main__':
    main()