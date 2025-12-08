import pandas as pd
import os
import glob

from ..config import PROCESSED_DATA_PATH, YEARS_TO_PROCESS, CURSOS_CSV_PATH

def get_cursos_avaliados():
    codigos_avaliados = set()

    campus_folders = [d for d in os.listdir(PROCESSED_DATA_PATH) if os.path.isdir(os.path.join(PROCESSED_DATA_PATH, d))]

    for campus_name in campus_folders:
        for year in YEARS_TO_PROCESS:
            campus_year_path = os.path.join(PROCESSED_DATA_PATH, campus_name, str(year))
            if os.path.exists(campus_year_path):
                info_file = glob.glob(os.path.join(campus_year_path, '*arq1.csv'))
                if info_file:
                    try:
                        df = pd.read_csv(info_file[0], sep=';', usecols=['CO_CURSO'])
                        codigos_avaliados.update(df['CO_CURSO'].unique())
                    except Exception as e:
                        print(f"Não foi possível ler {info_file[0]}. Erro: {e}")
    return list(codigos_avaliados)

def main():
    if not os.path.exists(CURSOS_CSV_PATH):
        return

    cursos_com_dados = get_cursos_avaliados()

    try:
        df_cursos_geral = pd.read_csv(CURSOS_CSV_PATH, sep=',')

    except Exception as e:
        print(f"ERRO ao ler o arquivo CSV: {e}")
        return

    df_cursos_geral['Nome Detalhado'] = df_cursos_geral['Curso']
    
    df_cursos_filtrados = df_cursos_geral[df_cursos_geral['Código'].isin(cursos_com_dados)]

    curso_map = pd.Series(df_cursos_filtrados['Nome Detalhado'].values, index=df_cursos_filtrados['Código']).to_dict()

    print("CURSO_MAP = {")
    for codigo, nome in sorted(curso_map.items()):
        print(f"    {codigo}: '{nome}',")
    print("}")


if __name__ == '__main__':
    main()