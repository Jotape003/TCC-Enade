import os
import shutil

origem = os.path.join('data_processing', 'data', 'json')
destino = os.path.join('frontend', 'public', 'data') 

def main():
    print(f"Origem: {origem}")
    print(f"Destino: {destino}")

    if os.path.exists(destino):
        shutil.rmtree(destino)

    shutil.copytree(origem, destino)

if __name__ == '__main__':
    main()