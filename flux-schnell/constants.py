# API URLs e configurações
DEFAULT_API_URL = "http://127.0.0.1:1234/v1/chat/completions"

# Configurações do LM Studio
LM_STUDIO_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 2000
}

# Template para geração de imagens
TEMPLATE_IMAGES = """You are an AI artist who generates high-quality images.
Your task is to generate 2 images, based on a theme provided by the user.
The images must be high quality, with sharp details and vibrant colors.
The images must be unique and non-repetitive.
The images must be generated in a visually appealing and easy to understand style.
The prompt must be rich in details, with lots of information, keywords, describing objects, colors, textures, etc.
Do not generate any text in the images, only the images themselves.
Do not generate any people, only landscapes and nature.
Realistic images, with vivid colors, 4K, ultra-realistic.
Prompt must be in english.

IMPORTANT: Your response must be ONLY a valid JSON object, with no additional text before or after.
The theme is: [ABOUT]

Example of valid response format:
{
    "images": [
        {
            "image": "name1.png",
            "prompt": "prompt1"
        },
        {
            "image": "name2.png",
            "prompt": "prompt2"
        }
    ],
    "description": "description of all images",
    "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10"]
}"""

# Configurações do Replicate
REPLICATE_CONFIG = {
    "model": "black-forest-labs/flux-schnell",
    "default_params": {
        "go_fast": True,
        "megapixels": "1",
        "num_outputs": 1,
        "aspect_ratio": "1:1",
        "output_format": "png",
        "output_quality": 80,
        "num_inference_steps": 4
    }
}

# Configurações do Upscale
UPSCALE_CONFIG = {
    "model": "daanelson/real-esrgan-a100:f94d7ed4a1f7e1ffed0d51e4089e4911609d5eeee5e874ef323d2c7562624bed",
    "default_params": {
        "scale": 4,
        "face_enhance": False
    }
}

# Configurações do Replicate LLM
REPLICATE_LLM_CONFIG = {
    "model": "meta/meta-llama-3-8b-instruct",
    "default_params": {
        "max_new_tokens": 2048,
        "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    }
}

# Tipos de LLM suportados
LLM_TYPES = {
    "local": "local",
    "replicate": "replicate"
}
