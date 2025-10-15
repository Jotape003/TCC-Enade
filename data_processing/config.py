import os

DATA_BASE_PATH = 'data'
RAW_DATA_PATH = os.path.join(DATA_BASE_PATH, 'raw')
PROCESSED_DATA_PATH = os.path.join(DATA_BASE_PATH, 'processed')

YEARS_TO_PROCESS = ['2021', '2019', '2017', '2014']
UFC_IES_CODE = 583

CAMPUS_MAP = {
    2311801: 'Russas',
    2312908: 'Sobral',
    2311306: 'Quixada',
    2304400: 'Fortaleza',
    2304103: 'Crateus',
    2306306: 'Itapaje'
}

BASE_URL = "https://download.inep.gov.br/microdados/microdados_enade_{year}_LGPD.zip"
URLS = {year: BASE_URL.format(year=year) for year in YEARS_TO_PROCESS}