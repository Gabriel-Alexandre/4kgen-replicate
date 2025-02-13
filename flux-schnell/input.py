import requests
import json
from datetime import datetime
import os
import uuid
import replicate
from constants import (
    DEFAULT_API_URL, 
    LM_STUDIO_CONFIG, 
    TEMPLATE_IMAGES, 
    REPLICATE_LLM_CONFIG,
    LLM_TYPES
)
from dotenv import load_dotenv

def generate_completion_local(prompt, api_url=DEFAULT_API_URL):
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

def generate_completion_replicate(prompt):
    load_dotenv()
    """
    Função para gerar completions usando o Replicate
    """
    try:
        output = replicate.run(
            REPLICATE_LLM_CONFIG["model"],
            input={
                "prompt": prompt,
                **REPLICATE_LLM_CONFIG["default_params"]
            }
        )
        return "".join(output)  # Junta todos os chunks do stream
    except Exception as e:
        return f"Erro ao usar Replicate: {str(e)}"

def generate_completion(prompt, llm_type=LLM_TYPES["local"]):
    """
    Função wrapper para gerar completions usando o provedor escolhido
    """
    if llm_type == LLM_TYPES["local"]:
        return generate_completion_local(prompt)
    elif llm_type == LLM_TYPES["replicate"]:
        return generate_completion_replicate(prompt)
    else:
        raise ValueError(f"Tipo de LLM não suportado: {llm_type}")

# Exemplo de uso
if __name__ == "__main__":
    about = input("Escreva um tema para as imagens que serão geradas: ")
    number_of_images = input("Escreva o número de imagens que serão geradas: ")
    
    try:
        number_of_images = int(number_of_images)
        if number_of_images < 1:
            print("Número inválido. Usando 1 imagem.")
            number_of_images = 1
    except ValueError:
        print("Número inválido. Usando 1 imagem.")
        number_of_images = 1

    # Calculando o número de iterações e imagens por JSON
    remaining_images = number_of_images
    iterations = (number_of_images + 1) // 2  # Arredonda para cima

    print("\nEscolha o tipo de LLM:")
    print("1 - Local (LM Studio)")
    print("2 - Replicate (Llama)")
    llm_choice = input("Digite sua escolha (1 ou 2): ")
    
    try:
        llm_choice = int(llm_choice)
        if llm_choice not in [1, 2]:
            print(f"Opção inválida. Usando opção 1 (Local)")
            llm_type = LLM_TYPES["local"]
        else:
            llm_type = LLM_TYPES["local"] if llm_choice == 1 else LLM_TYPES["replicate"]
    except ValueError:
        print("Opção inválida. Usando opção 1 (Local)")
        llm_type = LLM_TYPES["local"]

    final_prompt = TEMPLATE_IMAGES.replace("[ABOUT]", about)

    # Gerando um UUID único para esta execução
    execution_uuid = str(uuid.uuid4())
    
    # Criando o diretório prompts/[uuid] se não existir
    output_dir = os.path.join("./prompts", execution_uuid)
    os.makedirs(output_dir, exist_ok=True)
    
    # Loop para gerar os arquivos
    for i in range(iterations):
        # Determina quantas imagens gerar nesta iteração
        images_this_iteration = 2 if remaining_images >= 2 else 1
        
        # Atualiza o template com o número correto de imagens
        current_prompt = final_prompt.replace("[NUM_IMAGES]", str(images_this_iteration))
        
        print(f"\nGerando arquivo {i+1} de {iterations}...")
        response = generate_completion(current_prompt, llm_type)
        
        remaining_images -= images_this_iteration
        
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