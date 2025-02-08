import requests
import json
from datetime import datetime
import os
import uuid
from run import process_images_by_uuid, process_upscale_by_uuid  # Adicionar esta importação no topo do arquivo
from constants import DEFAULT_API_URL, LM_STUDIO_CONFIG, TEMPLATE_IMAGES

def generate_completion(prompt, api_url=DEFAULT_API_URL):
    """
    Função para gerar completions usando a API local do LM Studio
    
    Args:
        prompt (str): O texto de entrada para o modelo
        api_url (str): URL da API local (padrão para LM Studio)
    
    Returns:
        str: A resposta gerada pelo modelo
    """
    
    # Preparando o payload no formato esperado
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        **LM_STUDIO_CONFIG
    }
    
    try:
        # Fazendo a requisição POST
        response = requests.post(
            api_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Verificando se a requisição foi bem sucedida
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Erro: Status code {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return f"Erro na requisição: {str(e)}"




# Exemplo de uso
if __name__ == "__main__":
    
    about = input("Escreva um tema para as imagens que serão geradas: ")
    number_of_images = input("Escreva o número de imagens que serão geradas (deve ser par): ")
    final_prompt = TEMPLATE_IMAGES.replace("[ABOUT]", about)
    number_range = int(int(number_of_images)/2)

    # Gerando um UUID único para esta execução
    execution_uuid = str(uuid.uuid4())
    
    # Criando o diretório prompts/[uuid] se não existir
    output_dir = os.path.join("./prompts", execution_uuid)
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n=== Gerando prompts ===")
    # Loop para gerar os arquivos
    for i in range(number_range):
        print(f"\nGerando arquivo {i+1} de {number_range}...")
        response = generate_completion(final_prompt)
        
        # Obtendo timestamp atual
        now = datetime.now()
        timestamp = {
            "date": now.strftime("%Y-%m-%d"),
            "hour": now.strftime("%H"),
            "minute": now.strftime("%M"),
            "second": now.strftime("%S")
        }
        
        # Criando o objeto JSON final
        try:
            response_json = json.loads(response)  # Convertendo a string para JSON
            final_json = {
                "timestamp": timestamp,
                "theme": about,
                "response": response_json
            }
            
            # Modificando o nome do arquivo para usar o novo diretório
            filename = os.path.join(output_dir, f"response_{now.strftime('%Y%m%d_%H%M%S')}_{i+1}.json")
            
            # Salvando o arquivo
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(final_json, f, ensure_ascii=False, indent=4)
                
            print(f"Arquivo salvo com sucesso em: {filename}")
                
        except json.JSONDecodeError as e:
            print(f"Erro ao converter resposta para JSON: {str(e)}")
            print("Resposta recebida:", response)

    print("\n=== Gerando imagens ===")
    # Após gerar todos os prompts, chamar a função para processar as imagens
    process_images_by_uuid(execution_uuid)

    print("\n=== Gerando upscale das imagens ===")
    # Após gerar as imagens, chamar a função para fazer o upscale
    process_upscale_by_uuid(execution_uuid)