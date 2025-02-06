import replicate
import os
from datetime import datetime
from dotenv import load_dotenv
import json
import requests

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Processar todos os arquivos JSON na pasta prompts
prompts_dir = 'prompts'
all_prompts = []

# Percorrer todos os arquivos na pasta prompts
for filename in os.listdir(prompts_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(prompts_dir, filename)
        with open(file_path, 'r') as f:
            json_data = json.load(f)
            prompts = [image['prompt'] for image in json_data['response']['images']]
            all_prompts.extend(prompts)

# Criar diretório de output se não existir
output_dir = "./output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Processar cada prompt sequencialmente
for prompt in all_prompts:
    # Gerar timestamp único para o nome do arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Fazer a requisição para a API
    output = replicate.run(
        "black-forest-labs/flux-schnell",
        input={
            "prompt": prompt,
            "go_fast": True,
            "megapixels": "1",
            "num_outputs": 1,
            "aspect_ratio": "1:1",
            "output_format": "png",
            "output_quality": 80,
            "num_inference_steps": 4
        }
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