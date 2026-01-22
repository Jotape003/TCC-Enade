import pandas as pd
import os
import glob

from config import PROCESSED_DATA_PATH, YEARS_TO_PROCESS, CURSOS_CSV_PATH

def get_cursos_avaliados():
    codigos_avaliados = set()

    campus_folders = [d for d in os.listdir(PROCESSED_DATA_PATH) if os.path.isdir(os.path.join(PROCESSED_DATA_PATH, d))]

    for campus_name in campus_folders:
        for year in YEARS_TO_PROCESS:
            campus_year_path = os.path.join(PROCESSED_DATA_PATH, campus_name, str(year))
            if os.path.exists(campus_year_path):
                info_files = glob.glob(os.path.join(campus_year_path, '*arq1.csv'))
                if info_files:
                    try:
                        df = pd.read_csv(info_files[0], sep=';', usecols=['CO_CURSO'])
                        unique_codes = df['CO_CURSO'].dropna().unique().tolist()
                        codigos_avaliados.update(unique_codes)
                    except Exception as e:
                        print(f"  -> Erro ao ler {os.path.basename(info_files[0])}: {e}")
    return list(codigos_avaliados)

def main():
    cursos_com_dados = get_cursos_avaliados()

    df_cursos_geral = pd.read_csv(CURSOS_CSV_PATH, sep=';', dtype={'Código': str})

    df_cursos_geral['Curso'] = df_cursos_geral['Curso'].astype(str).str.strip()
    
    if 'Grau' in df_cursos_geral.columns:
        df_cursos_geral['Grau'] = df_cursos_geral['Grau'].astype(str).str.strip()
    else:
        df_cursos_geral['Grau'] = ''

    df_cursos_geral['Nome Detalhado'] = df_cursos_geral.apply(
        lambda row: f"{row['Curso']} - {row['Grau']}" if row['Grau'] and row['Grau'].lower() != 'nan' else row['Curso'],
        axis=1
    )
    if cursos_com_dados:
        codigos_str = [str(c) for c in cursos_com_dados]
        df_cursos_filtrados = df_cursos_geral[df_cursos_geral['Código'].isin(codigos_str)]
    else:
        df_cursos_filtrados = df_cursos_geral

    curso_map = pd.Series(
        df_cursos_filtrados['Nome Detalhado'].values, 
        index=df_cursos_filtrados['Código']
    ).to_dict()

    print("CURSO_MAP = {")
    for codigo, nome in sorted(curso_map.items()):
        nome_safe = nome.replace("'", "\\'")
        print(f"    {codigo}: '{nome_safe}',")
    print("}")

if __name__ == '__main__':
    main()