import os

DATA_BASE_PATH = 'data'
RAW_DATA_PATH = os.path.join(DATA_BASE_PATH, 'raw')
PROCESSED_DATA_PATH = os.path.join(DATA_BASE_PATH, 'processed')
JSON_DATA_PATH = os.path.join(DATA_BASE_PATH, 'json')
CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv')

# Contagem a partir de 2014 até o ano mais recente disponível
YEARS_TO_PROCESS = ['2014', '2015', '2016', '2017', '2018', '2019', '2021', '2022', '2023']
UFC_IES_CODE = 583

FINAL_JSON_PATH = os.path.join(JSON_DATA_PATH, 'visao_geral.json')
FINAL_MEDIA_JSON_PATH = os.path.join(JSON_DATA_PATH, 'medias.json')
FINAL_CE_JSON_PATH = os.path.join(JSON_DATA_PATH, 'comp_especifico.json')

CAMPUS_MAP = {
    2311801: 'Russas',
    2312908: 'Sobral',
    2311306: 'Quixada',
    2304400: 'Fortaleza',
    2304103: 'Crateus',
    2306306: 'Itapaje'
}

URLS = {
    '2014': 'https://download.inep.gov.br/microdados/microdados_enade_2014_LGPD.zip',
    '2015': 'https://download.inep.gov.br/microdados/microdados_enade_2015_LGPD.zip',
    '2016': 'https://download.inep.gov.br/microdados/microdados_enade_2016_LGPD.zip',
    '2017': 'https://download.inep.gov.br/microdados/microdados_enade_2017_LGPD.zip',
    '2018': 'https://download.inep.gov.br/microdados/microdados_enade_2018_LGPD.zip',
    '2019': 'https://download.inep.gov.br/microdados/microdados_enade_2019_LGPD.zip',
    '2021': 'https://download.inep.gov.br/microdados/microdados_enade_2021.zip',
    '2022': 'https://download.inep.gov.br/microdados/microdados_enade_2022_LGPD.rar',
    '2023': 'https://download.inep.gov.br/microdados/microdados_enade_2023.zip'
}

CURSO_MAP = {
    13965: 'AGRONOMIA',
    13967: 'PEDAGOGIA',
    13968: 'DIREITO',
    13969: 'CIÊNCIAS CONTÁBEIS',
    13970: 'CIÊNCIAS ECONÔMICAS',
    13972: 'FÍSICA',
    13974: 'CIÊNCIAS BIOLÓGICAS ',
    13976: 'GEOGRAFIA',
    13977: 'MATEMÁTICA',
    13980: 'CIÊNCIA DA COMPUTAÇÃO',
    13982: 'CIÊNCIAS SOCIAIS',
    13984: 'HISTÓRIA',
    13986: 'PSICOLOGIA',
    13987: 'ARQUITETURA E URBANISMO',
    13988: 'ENGENHARIA CIVIL',
    13989: 'ENGENHARIA ELÉTRICA',
    13990: 'ENGENHARIA MECÂNICA',
    13991: 'ENGENHARIA QUÍMICA',
    13992: 'ENGENHARIA DE PESCA',
    13993: 'ENGENHARIA DE ALIMENTOS',
    13994: 'ENFERMAGEM',
    13995: 'FARMÁCIA',
    13996: 'MEDICINA',
    13997: 'ODONTOLOGIA',
    13998: 'ADMINISTRAÇÃO',
    14000: 'EDUCAÇÃO FÍSICA',
    14002: 'SECRETARIADO EXECUTIVO',
    23947: 'JORNALISMO',
    25821: 'LETRAS - PORTUGUÊS E ITALIANO',
    25822: 'LETRAS - PORTUGUÊS E ALEMÃO',
    27263: 'LETRAS - PORTUGUÊS E ESPANHOL',
    29489: 'LETRAS - LÍNGUA PORTUGUESA',
    33013: 'LETRAS - PORTUGUÊS E INGLÊS',
    34433: 'LETRAS - PORTUGUÊS E FRANCÊS',
    37265: 'ENGENHARIA DE PRODUÇÃO',
    37267: 'COMUNICAÇÃO SOCIAL - PUBLICIDADE E PROPAGANDA',
    37274: 'FILOSOFIA',
    38202: 'ADMINISTRAÇÃO',
    38204: 'CIÊNCIAS CONTÁBEIS',
    38206: 'CIÊNCIAS ECONÔMICAS',
    38208: 'DIREITO',
    38217: 'QUÍMICA',
    38239: 'FÍSICA',
    38246: 'MATEMÁTICA',
    38273: 'PEDAGOGIA',
    50392: 'ZOOTECNIA',
    54490: 'MEDICINA',
    99300: 'ENGENHARIA DE COMPUTAÇÃO',
    99302: 'ENGENHARIA ELÉTRICA',
    99306: 'CIÊNCIAS ECONÔMICAS',
    99308: 'ODONTOLOGIA',
    99310: 'PSICOLOGIA',
    99567: 'QUÍMICA',
    99572: 'ENGENHARIA METALÚRGICA',
    100021: 'MÚSICA',
    100256: 'EDUCAÇÃO FÍSICA',
    100367: 'QUÍMICA',
    100369: 'MATEMÁTICA',
    100375: 'LETRAS - LÍNGUA PORTUGUESA',
    100376: 'LETRAS - INGLÊS',
    106167: 'SISTEMAS DE INFORMAÇÃO',
    113757: 'FÍSICA',
    116834: 'CIÊNCIAS SOCIAIS',
    150099: 'MÚSICA',
    150112: 'ENGENHARIA AMBIENTAL E SANITÁRIA',
    150113: 'ENGENHARIA DE PETRÓLEO',
    150116: 'ENGENHARIA DE ENERGIAS RENOVÁVEIS',
    313974: 'CIÊNCIAS BIOLÓGICAS ',
    313976: 'GEOGRAFIA',
    313982: 'CIÊNCIAS SOCIAIS',
    337274: 'FILOSOFIA',
    416834: 'CIÊNCIAS SOCIAIS',
    1122966: 'FISIOTERAPIA',
    1127191: 'REDES DE COMPUTADORES',
    1128911: 'LETRAS - INGLÊS',
    1167971: 'DESIGN',
    1191427: 'EDUCAÇÃO FÍSICA',
    1191555: 'EDUCAÇÃO FÍSICA',
    1216500: 'ADMINISTRAÇÃO PÚBLICA',
    1270596: 'CIÊNCIA DA COMPUTAÇÃO',
    1272079: 'CIÊNCIA DA COMPUTAÇÃO',
    1299927: 'CIÊNCIA DA COMPUTAÇÃO',
    1299931: 'ENGENHARIA CIVIL',
    1299933: 'ENGENHARIA DE COMPUTAÇÃO',
    1299935: 'ENGENHARIA DE PRODUÇÃO',
    1299936: 'ENGENHARIA MECÂNICA',
    1300426: 'ENGENHARIA AMBIENTAL E SANITÁRIA',
    1300427: 'ENGENHARIA CIVIL',
    1300429: 'SISTEMAS DE INFORMAÇÃO',
    1313213: 'ENGENHARIA DE COMPUTAÇÃO',
}