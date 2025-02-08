# API URLs e configurações
DEFAULT_API_URL = "http://127.0.0.1:1234/v1/chat/completions"

# Configurações do LM Studio
LM_STUDIO_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 2000
}

# Template para geração de imagens
TEMPLATE_IMAGES = """
    You are an AI artist who generates high-quality images.
    Your task is to generate 2 images, based on a theme provided by the user.
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
            },
            {
                "image": "[choose a name for the image].png",
                "prompt": "prompt2",
            },
            ...

        ],
        "description": "description to represent all generated images, be creative and detailed",
        "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10"]
    }
"""

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
