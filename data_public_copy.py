import os
import shutil

origem = os.path.join('data_processing', 'data', 'json')
destino = os.path.join('frontend', 'public', 'data')

pastas_desejadas = ['Desempenho_Topico', 'Visao_Geral', 'Evolucao_Historica']

def main():
    print(f"Origem: {origem}")
    print(f"Destino: {destino}")

    if os.path.exists(destino):
        shutil.rmtree(destino)

    os.makedirs(destino, exist_ok=True)

    for pasta in pastas_desejadas:
        origem_pasta = os.path.join(origem, pasta)
        destino_pasta = os.path.join(destino, pasta)

        if os.path.exists(origem_pasta):
            shutil.copytree(origem_pasta, destino_pasta)

if __name__ == '__main__':
    main()
