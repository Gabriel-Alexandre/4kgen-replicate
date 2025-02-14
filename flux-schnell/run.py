import replicate
import os
from datetime import datetime
from dotenv import load_dotenv
import json
import requests
from constants import REPLICATE_CONFIG, UPSCALE_CONFIG

def process_images_by_uuid(uuid_dir):
    """
    Processa todos os arquivos JSON dentro de um diretório UUID específico e gera imagens.
    
    Args:
        uuid_dir (str): UUID do diretório a ser processado
    """
    # Carregar variáveis de ambiente do arquivo .env
    load_dotenv()

    # Definir o diretório específico do UUID
    prompts_dir = os.path.join('prompts', uuid_dir)
    all_prompts = []

    # Verificar se o diretório existe
    if not os.path.exists(prompts_dir):
        print(f"Diretório não encontrado: {prompts_dir}")
        return

    # Percorrer todos os arquivos no diretório do UUID
    for filename in os.listdir(prompts_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(prompts_dir, filename)
            with open(file_path, 'r') as f:
                json_data = json.load(f)
                prompts = [image['prompt'] for image in json_data['response']['images']]
                all_prompts.extend(prompts)

    # Criar diretório de output se não existir
    output_dir = os.path.join("./output", uuid_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Processar cada prompt sequencialmente
    for prompt in all_prompts:
        # Gerar timestamp único para o nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Fazer a requisição para a API
        output = replicate.run(
            REPLICATE_CONFIG["model"],
            input=REPLICATE_CONFIG["default_params"] | {"prompt": prompt}
        )

        print(output)
        
        # O output é uma URL da imagem gerada
        image_url = output[0]
        
        # Baixar e salvar a imagem usando requests
        response = requests.get(image_url)
        output_path = os.path.join(output_dir, f"{timestamp}.png")
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        print(f"Imagem salva em: {output_path}")

def process_upscale_by_uuid(uuid_dir):
    """
    Processa todas as imagens dentro do diretório output/uuid e gera versões upscaled.
    
    Args:
        uuid_dir (str): UUID do diretório a ser processado
    """
    # Carregar variáveis de ambiente do arquivo .env
    load_dotenv()

    # Definir os diretórios
    input_dir = os.path.join("./output", uuid_dir)
    output_dir = os.path.join("./upscaly", uuid_dir)

    # Verificar se o diretório de entrada existe
    if not os.path.exists(input_dir):
        print(f"Diretório de entrada não encontrado: {input_dir}")
        return

    # Criar diretório de output se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Processar cada imagem no diretório
    for filename in os.listdir(input_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_dir, filename)
            
            # Preparar o caminho de saída
            output_filename = f"upscaled_{filename}"
            output_path = os.path.join(output_dir, output_filename)

            print(f"Processando upscale de: {filename}")

            try:
                # Abrir a imagem como arquivo binário para enviar diretamente
                with open(input_path, "rb") as f:
                    # Fazer a requisição de upscale enviando o arquivo diretamente
                    output = replicate.run(
                        UPSCALE_CONFIG["model"],
                        input=UPSCALE_CONFIG["default_params"] | {"image": f}
                    )

                print(output)

                # O output é uma URL da imagem upscaled
                upscaled_url = str(output)  # Convertendo o FileOutput para string

                # Baixar e salvar a imagem upscaled
                response = requests.get(upscaled_url)
                with open(output_path, "wb") as f:
                    f.write(response.content)

                print(f"Imagem upscaled salva em: {output_path}")

            except Exception as e:
                print(f"Erro ao processar {filename}: {str(e)}")

if __name__ == "__main__":
    # Exemplo de uso
    uuid = input("Digite o UUID do diretório a ser processado: ")
    process_images_by_uuid(uuid)
    # process_upscale_by_uuid(uuid)