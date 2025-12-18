import os

DATA_BASE_PATH = 'data'
RAW_DATA_PATH = os.path.join(DATA_BASE_PATH, 'raw')
PROCESSED_DATA_PATH = os.path.join(DATA_BASE_PATH, 'processed')
JSON_DATA_PATH = os.path.join(DATA_BASE_PATH, 'json')
CURSOS_CSV_PATH = os.path.join('data', 'cursos_ufc.csv')

# Contagem a partir de 2014 até o ano mais recente disponível
YEARS_TO_PROCESS = ['2014', '2015', '2016', '2017', '2018', '2019', '2021', '2022', '2023']
UFC_IES_CODE = 583
UF_CODE = 23
REGIAO_CODE = 2

FINAL_VG_JSON_PATH = os.path.join(JSON_DATA_PATH, 'Visao_Geral')
FINAL_MEDIA_JSON_PATH = os.path.join(JSON_DATA_PATH, 'Medias')
FINAL_ESTRUTURA_JSON_PATH = os.path.join(JSON_DATA_PATH, 'Estruturas_json')
FINAL_DT_JSON_PATH = os.path.join(JSON_DATA_PATH, 'Desempenho_Topico')
FINAL_EH_JSON_PATH = os.path.join(JSON_DATA_PATH, 'Evolucao_Historica')

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
    100021: 'MÚSICA - Licenciatura',
    100256: 'EDUCAÇÃO FÍSICA - Bacharelado',
    100367: 'QUÍMICA - Licenciatura',
    100369: 'MATEMÁTICA - Licenciatura',
    100375: 'LETRAS - LÍNGUA PORTUGUESA - Licenciatura',
    100376: 'LETRAS - INGLÊS - Licenciatura',
    106167: 'SISTEMAS DE INFORMAÇÃO - Bacharelado',
    1122966: 'FISIOTERAPIA - Bacharelado',
    1127191: 'REDES DE COMPUTADORES - Tecnológico',
    1128911: 'LETRAS - INGLÊS - Licenciatura',
    113757: 'FÍSICA - Licenciatura',
    1167971: 'DESIGN - Bacharelado',
    116834: 'CIÊNCIAS SOCIAIS - Licenciatura',
    1191427: 'EDUCAÇÃO FÍSICA - Licenciatura',
    1191555: 'EDUCAÇÃO FÍSICA - Bacharelado',
    1216500: 'ADMINISTRAÇÃO PÚBLICA - Bacharelado',
    1270596: 'CIÊNCIA DA COMPUTAÇÃO - Bacharelado',
    1272079: 'CIÊNCIA DA COMPUTAÇÃO - Bacharelado',
    1299927: 'CIÊNCIA DA COMPUTAÇÃO - Bacharelado',
    1299931: 'ENGENHARIA CIVIL - Bacharelado',
    1299933: 'ENGENHARIA DE COMPUTAÇÃO - Bacharelado',
    1299935: 'ENGENHARIA DE PRODUÇÃO - Bacharelado',
    1299936: 'ENGENHARIA MECÂNICA - Bacharelado',
    1300426: 'ENGENHARIA AMBIENTAL E SANITÁRIA - Bacharelado',
    1300427: 'ENGENHARIA CIVIL - Bacharelado',
    1300429: 'SISTEMAS DE INFORMAÇÃO - Bacharelado',
    1313213: 'ENGENHARIA DE COMPUTAÇÃO - Bacharelado',
    13965: 'AGRONOMIA - Bacharelado',
    13967: 'PEDAGOGIA - Licenciatura',
    13968: 'DIREITO - Bacharelado',
    13969: 'CIÊNCIAS CONTÁBEIS - Bacharelado',
    13970: 'CIÊNCIAS ECONÔMICAS - Bacharelado',
    13972: 'FÍSICA - Bacharelado',
    13974: 'CIÊNCIAS BIOLÓGICAS - Licenciatura',
    13976: 'GEOGRAFIA - Licenciatura',
    13977: 'MATEMÁTICA - Bacharelado',
    13980: 'CIÊNCIA DA COMPUTAÇÃO - Bacharelado',
    13982: 'CIÊNCIAS SOCIAIS - Licenciatura',
    13984: 'HISTÓRIA - Licenciatura',
    13986: 'PSICOLOGIA - Bacharelado',
    13987: 'ARQUITETURA E URBANISMO - Bacharelado',
    13988: 'ENGENHARIA CIVIL - Bacharelado',
    13989: 'ENGENHARIA ELÉTRICA - Bacharelado',
    13990: 'ENGENHARIA MECÂNICA - Bacharelado',
    13991: 'ENGENHARIA QUÍMICA - Bacharelado',
    13992: 'ENGENHARIA DE PESCA - Bacharelado',
    13993: 'ENGENHARIA DE ALIMENTOS - Bacharelado',
    13994: 'ENFERMAGEM - Bacharelado',
    13995: 'FARMÁCIA - Bacharelado',
    13996: 'MEDICINA - Bacharelado',
    13997: 'ODONTOLOGIA - Bacharelado',
    13998: 'ADMINISTRAÇÃO - Bacharelado',
    14000: 'EDUCAÇÃO FÍSICA - Licenciatura',
    14002: 'SECRETARIADO EXECUTIVO - Bacharelado',
    150099: 'MÚSICA - Licenciatura',
    150112: 'ENGENHARIA AMBIENTAL E SANITÁRIA - Bacharelado',
    150113: 'ENGENHARIA DE PETRÓLEO - Bacharelado',
    150116: 'ENGENHARIA DE ENERGIAS RENOVÁVEIS - Bacharelado',
    23947: 'JORNALISMO - Bacharelado',
    25821: 'LETRAS - PORTUGUÊS E ITALIANO - Licenciatura',
    25822: 'LETRAS - PORTUGUÊS E ALEMÃO - Licenciatura',
    27263: 'LETRAS - PORTUGUÊS E ESPANHOL - Licenciatura',
    29489: 'LETRAS - LÍNGUA PORTUGUESA - Licenciatura',
    313974: 'CIÊNCIAS BIOLÓGICAS - Bacharelado',
    313976: 'GEOGRAFIA - Bacharelado',
    313982: 'CIÊNCIAS SOCIAIS - Bacharelado',
    33013: 'LETRAS - PORTUGUÊS E INGLÊS - Licenciatura',
    337274: 'FILOSOFIA - Bacharelado',
    34433: 'LETRAS - PORTUGUÊS E FRANCÊS - Licenciatura',
    37265: 'ENGENHARIA DE PRODUÇÃO - Bacharelado',
    37267: 'COMUNICAÇÃO SOCIAL - PUBLICIDADE E PROPAGANDA - Bacharelado',
    37274: 'FILOSOFIA - Licenciatura',
    38202: 'ADMINISTRAÇÃO - Bacharelado',
    38204: 'CIÊNCIAS CONTÁBEIS - Bacharelado',
    38206: 'CIÊNCIAS ECONÔMICAS - Bacharelado',
    38208: 'DIREITO - Bacharelado',
    38217: 'QUÍMICA - Licenciatura',
    38239: 'FÍSICA - Licenciatura',
    38246: 'MATEMÁTICA - Licenciatura',
    38273: 'PEDAGOGIA - Licenciatura',
    416834: 'CIÊNCIAS SOCIAIS - Bacharelado',
    50392: 'ZOOTECNIA - Bacharelado',
    54490: 'MEDICINA - Bacharelado',
    99300: 'ENGENHARIA DE COMPUTAÇÃO - Bacharelado',
    99302: 'ENGENHARIA ELÉTRICA - Bacharelado',
    99306: 'CIÊNCIAS ECONÔMICAS - Bacharelado',
    99308: 'ODONTOLOGIA - Bacharelado',
    99310: 'PSICOLOGIA - Bacharelado',
    99567: 'QUÍMICA - Bacharelado',
    99572: 'ENGENHARIA METALÚRGICA - Bacharelado',
}

QUESTOES_MAP = {
    # Organização Didático-Pedagógica
    "QE_I27": {"texto": "Contribuição para formação integral", "cat": "didatica"},
    "QE_I28": {"texto": "Relevância dos conteúdos para formação", "cat": "didatica"},
    "QE_I29": {"texto": "Metodologias de ensino diversificadas", "cat": "didatica"},
    "QE_I30": {"texto": "Avaliações compatíveis com conteúdo", "cat": "didatica"},
    "QE_I31": {"texto": "Domínio de conteúdo pelos professores", "cat": "didatica"},
    "QE_I32": {"texto": "Relação professor-aluno", "cat": "didatica"},
    "QE_I33": {"texto": "Experiências de aprendizado inovadoras", "cat": "didatica"},
    "QE_I34": {"texto": "Desenvolvimento do pensamento crítico", "cat": "didatica"},
    "QE_I35": {"texto": "Desenvolvimento da autonomia (aprender a aprender)", "cat": "didatica"},
    "QE_I36": {"texto": "Capacidade de resolver problemas", "cat": "didatica"},
    "QE_I37": {"texto": "Capacidade de trabalhar em equipe", "cat": "didatica"},
    "QE_I38": {"texto": "Ética e responsabilidade social", "cat": "didatica"},
    "QE_I39": {"texto": "Compreensão e comunicação", "cat": "didatica"},
    "QE_I40": {"texto": "Uso de tecnologias da informação", "cat": "didatica"},
    "QE_I41": {"texto": "Integração teoria e prática", "cat": "didatica"},

    # Infraestrutura
    "QE_I42": {"texto": "Adequação das salas de aula", "cat": "infra"},
    "QE_I43": {"texto": "Equipamentos para aulas práticas", "cat": "infra"},
    "QE_I44": {"texto": "Acervo da biblioteca", "cat": "infra"},
    "QE_I45": {"texto": "Suporte e atendimento ao estudante", "cat": "infra"},
    "QE_I46": {"texto": "Infraestrutura de TI (Internet/Computadores)", "cat": "infra"},
    "QE_I47": {"texto": "Acessibilidade para pessoas com deficiência", "cat": "infra"},
    "QE_I48": {"texto": "Segurança e limpeza", "cat": "infra"},
    "QE_I49": {"texto": "Ambiente de estudo na biblioteca", "cat": "infra"},

    # Oportunidades de Ampliação
    "QE_I50": {"texto": "Oportunidade de Iniciação Científica", "cat": "oportunidades"},
    "QE_I51": {"texto": "Oportunidade de Extensão", "cat": "oportunidades"},
    "QE_I52": {"texto": "Oportunidade de Monitoria", "cat": "oportunidades"},
    "QE_I53": {"texto": "Participação em eventos acadêmicos", "cat": "oportunidades"},
    "QE_I54": {"texto": "Estágio supervisionado", "cat": "oportunidades"},
    "QE_I55": {"texto": "Apoio financeiro/logístico para eventos", "cat": "oportunidades"},
    "QE_I56": {"texto": "Apoio pedagógico/psicológico", "cat": "oportunidades"},
    "QE_I57": {"texto": "Alimentação/Moradia estudantil", "cat": "oportunidades"},
    "QE_I58": {"texto": "Disponibilidade da coordenação", "cat": "oportunidades"},
    "QE_I59": {"texto": "Atuação do colegiado do curso", "cat": "oportunidades"},
    "QE_I60": {"texto": "Comunicação coordenação/estudantes", "cat": "oportunidades"},
    "QE_I61": {"texto": "Planejamento e divulgação de atividades", "cat": "oportunidades"},
    "QE_I62": {"texto": "Atividades extracurriculares", "cat": "oportunidades"},
    "QE_I63": {"texto": "Integração com mercado de trabalho", "cat": "oportunidades"},
    "QE_I64": {"texto": "Integração com comunidade externa", "cat": "oportunidades"},
    "QE_I65": {"texto": "Atividades culturais e esportivas", "cat": "oportunidades"},
    "QE_I66": {"texto": "Ações de sustentabilidade", "cat": "oportunidades"},
    "QE_I67": {"texto": "Ações de direitos humanos", "cat": "oportunidades"},
    "QE_I68": {"texto": "Avaliação Geral do Curso", "cat": "geral"}
}