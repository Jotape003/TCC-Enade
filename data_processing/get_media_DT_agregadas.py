# Importa as FUNÇÕES de dentro do seu pacote
from get_Media_DT.get_media_Nacional_DT import run_calculation_br
from get_Media_DT.get_medias_Regiao_DT import run_calculation_regiao
from get_Media_DT.get_medias_UF_DT import run_calculation_uf 
from get_Media_DT.get_medias_UFC_DT import run_calculation_ufc
from get_Media_DT.get_media_Curso_DT import run_calculation_curso

def main_orchestrator():
    print("--- INICIANDO ORQUESTRADOR MESTRE DE CÁLCULO DE MÉDIAS ---")

    print("\n[BLOCO 1/5] Calculando Médias Nacionais (BR)...")
    run_calculation_br()

    print("\n[BLOCO 2/5] Calculando Médias Regionais (NE)...")
    run_calculation_regiao()

    print("\n[BLOCO 3/5] Calculando Médias Estaduais (UF)...")
    run_calculation_uf()    

    print("\n[BLOCO 4/5] Calculando Médias da UFC (UFC)...")
    run_calculation_ufc()
    
    print("\n[BLOCO 5/5] Calculando Médias por Curso...")
    run_calculation_curso()

if __name__ == "__main__":
    main_orchestrator()