import os
import json
import pandas as pd
from collections import defaultdict

from config import FINAL_ESTRUTURA_JSON_PATH, FINAL_MEDIA_JSON_PATH
from utils import load_json, save_json_safe

MAP_CE_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_competencias_final.json')
MAP_FG_PATH = os.path.join(FINAL_ESTRUTURA_JSON_PATH, 'estrutura_fg_final.json')
OUTPUT_PATH = os.path.join(FINAL_MEDIA_JSON_PATH, 'Estatisticas_Prova')

def process_questions(map_questoes, lista_topicos, tipo_questao, acumulador):
    for q_key, indices in map_questoes.items():
        if not isinstance(indices, list):
            indices = [indices]
            
        for idx in indices:
            try:
                idx_real = int(idx) - 1
                
                if 0 <= idx_real < len(lista_topicos):
                    nome_topico = lista_topicos[idx_real]
                    
                    acumulador[nome_topico]['total'] += 1
                    
                    chave_lista = 'lista_obj' if tipo_questao == 'obj' else 'lista_disc'
                    acumulador[nome_topico][chave_lista].append(q_key)
                    
                else:
                    pass
            except ValueError:
                continue

def analyze_distribution():
    print("--- INICIANDO ANÁLISE DETALHADA DE DISTRIBUIÇÃO DE TÓPICOS ---")
    
    map_ce = load_json(MAP_CE_PATH)
    map_fg = load_json(MAP_FG_PATH)
    
    if not map_ce: return
    resultado_distribuicao_ce = {}

    print("\nProcessando Componentes Específicos (por Grupo)...")
    
    for co_grupo, dados_grupo in map_ce.items():
        lista_topicos = dados_grupo.get('Componente_especifico', [])
        anos_dict = dados_grupo.get('Anos', {})
        
        resultado_distribuicao_ce[co_grupo] = {}
        
        for ano, dados_ano in anos_dict.items():
            questoes_ce = dados_ano.get('questoes_CE', {})
            obj_map = questoes_ce.get('objetivas', {})
            disc_map = questoes_ce.get('discursivas', {})
            
            acumulador = defaultdict(lambda: {'total': 0, 'lista_obj': [], 'lista_disc': []})
            
            process_questions(obj_map, lista_topicos, 'obj', acumulador)
            process_questions(disc_map, lista_topicos, 'disc', acumulador)
            
            resultado_ordenado = dict(sorted(acumulador.items(), key=lambda item: item[1]['total'], reverse=True))
            
            resultado_distribuicao_ce[co_grupo][ano] = resultado_ordenado

    print("Processando Formação Geral (FG)...")
    resultado_distribuicao_fg = {}
    
    if isinstance(map_fg, list): 
        for dados_ano in map_fg:
            ano = str(dados_ano.get('ANO'))
            lista_topicos_fg = dados_ano.get('Formacao_geral', [])
            questoes_fg = dados_ano.get('questoes', {})
            obj_map = questoes_fg.get('objetivas', {})
            disc_map = questoes_fg.get('discursivas', {})
            
            acumulador = defaultdict(lambda: {'total': 0, 'lista_obj': [], 'lista_disc': []})
            
            process_questions(obj_map, lista_topicos_fg, 'obj', acumulador)
            process_questions(disc_map, lista_topicos_fg, 'disc', acumulador)
            
            resultado_ordenado = dict(sorted(acumulador.items(), key=lambda item: item[1]['total'], reverse=True))
            resultado_distribuicao_fg[ano] = resultado_ordenado

    path_ce = os.path.join(OUTPUT_PATH, 'distribuicao_questoes_ce.json')
    save_json_safe(resultado_distribuicao_ce, path_ce, "Distribuição Detalhada (CE)")
    
    path_fg = os.path.join(OUTPUT_PATH, 'distribuicao_questoes_fg.json')
    save_json_safe(resultado_distribuicao_fg, path_fg, "Distribuição Detalhada (FG)")

    print("\n--- Análise concluída com sucesso! ---")

if __name__ == "__main__":
    analyze_distribution()