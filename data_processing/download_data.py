import requests
import zipfile
import os
from tqdm import tqdm
from config import URLS, RAW_DATA_PATH

def download_file(url, dest_path):
    print(f"Baixando {dest_path}...")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size_in_bytes = int(r.headers.get('content-length', 0))
            block_size = 1024
            
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            with open(dest_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=block_size):
                    progress_bar.update(len(chunk))
                    f.write(chunk)
            progress_bar.close()

            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print("ERRO: Algo deu errado durante o download.")
                return False
        print("Download completo.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")
        return False
    
def main():
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    print(f"Diretório de dados brutos: '{RAW_DATA_PATH}'")

    for year, url in URLS.items():
        zip_filename = os.path.join(RAW_DATA_PATH, f'microdados_enade_{year}.zip')
        extract_path = os.path.join(RAW_DATA_PATH, f'enade_{year}')

        if not os.path.exists(zip_filename):
            if not download_file(url, zip_filename):
                continue
        else:
            print(f"Arquivo '{zip_filename}' já existe. Pulando download.")

        if not os.path.exists(extract_path):
            print(f"Descompactando '{zip_filename}' para '{extract_path}'...")
            try:
                with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                print("Descompactação concluída.")
            except zipfile.BadZipFile:
                print(f"ERRO: O arquivo '{zip_filename}' está corrompido ou não é um ZIP válido.")
        else:
            print(f"Diretório '{extract_path}' já existe. Pulando descompactação.")

if __name__ == '__main__':
    main()