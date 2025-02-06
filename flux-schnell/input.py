import requests
import json
from datetime import datetime
import os

def generate_completion(prompt, api_url="http://127.0.0.1:1234/v1/chat/completions"):
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
        "temperature": 0.7,
        "max_tokens": 2000
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

template_images = """
    You are an AI artist who generates high-quality images.
    Your task is to generate 2 images based on a theme provided by the user.
    The images must be high quality, with sharp details and vibrant colors.
    The images must be unique and non-repetitive.
    The images must be generated in a visually appealing and easy to understand style.
    The prompt must be rich in details, with lots of information, keywords, describing objects, colors, textures, etc.
    Do not generate any text in the images, only the images themselves.
    Do not generate any people, only landscapes and nature.
    Realistic images, with vivid colors, 4K, ultra-realistic.
    Prompt must be in english.
    Prompt example: "An elegant floating breakfast table set in a turquoise-blue lagoon, surrounded by lush tropical greenery. The rising sun paints the sky in golden and pink hues, reflecting gently on the calm water surface. A dark wooden platform floats delicately, decorated with a luxurious breakfast spread: white porcelain cups with golden details, plates filled with fresh croissants, vibrant tropical fruits, and natural juices served in crystal goblets. Hibiscus flowers and palm leaves adorn the table, adding an exotic touch to the setting. Colorful fish swim beneath the platform, while in the background, a small waterfall gently flows into the lagoon, creating a soothing ambiance. The morning breeze and the sweet scent of nature make this a paradise-like breakfast experience."
    The image theme is: [ABOUT]
    The output must be a json in the following format (always respect the format, do not add anything beyond what is inside the curly braces \{\}):
    {
        "images": [
            {
                "image": "[choose a name for the image].png",
                "prompt": "prompt1",
                "brief_description": "brief description of the image",
                "tags": ["tag1", "tag2", "tag3"]
            },
            {
                "image": "[choose a name for the image].png",
                "prompt": "prompt2",
                "brief_description": "brief description of the image",
                "tags": ["tag1", "tag2", "tag3"]
            },
            ...

        ]
    }
"""


# Exemplo de uso
if __name__ == "__main__":
    # Criando o diretório prompts se não existir
    if not os.path.exists("./prompts"):
        os.makedirs("./prompts")
    
    about = input("Escreva um tema para as imagens que serão geradas: ")
    number_of_images = input("Escreva o número de imagens que serão geradas: ")
    final_prompt = template_images.replace("[ABOUT]", about)
    number_range = int(int(number_of_images)/2)
    

    # Loop para gerar 10 arquivos diferentes
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
            
            # Gerando nome do arquivo com timestamp e número da iteração
            filename = f"./prompts/response_{now.strftime('%Y%m%d_%H%M%S')}_v{i+1}.json"
            
            # Salvando o arquivo
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(final_json, f, ensure_ascii=False, indent=4)
                
            print(f"Arquivo salvo com sucesso em: {filename}")
                
        except json.JSONDecodeError as e:
            print(f"Erro ao converter resposta para JSON: {str(e)}")
            print("Resposta recebida:", response)