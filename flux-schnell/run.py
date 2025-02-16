import replicate
import os
from datetime import datetime
from dotenv import load_dotenv
import json
import requests
from constants import REPLICATE_CONFIG, UPSCALE_CONFIG, PATH_TO_PROMPTS, PATH_TO_OUTPUT, PATH_TO_UPSCALE, MAX_RETRIES


class ImageProcessor:
    def __init__(self, uuid_dir: str):
        self.uuid_dir = uuid_dir
        load_dotenv()
        self.prompts_dir = os.path.join(PATH_TO_PROMPTS, uuid_dir)
        self.output_dir = os.path.join(PATH_TO_OUTPUT, uuid_dir)
        self.upscale_dir = os.path.join(PATH_TO_UPSCALE, uuid_dir)
        self._create_output_directories()

    def _create_output_directories(self) -> None:
        """Create the necessary output directories"""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.upscale_dir, exist_ok=True)

    def _collect_prompts(self) -> list:
        """Collect all prompts from JSON files"""
        if not os.path.exists(self.prompts_dir):
            raise ValueError(f"Directory not found: {self.prompts_dir}")

        all_prompts = []
        for filename in os.listdir(self.prompts_dir):
            if filename.endswith('.json'):
                with open(os.path.join(self.prompts_dir, filename), 'r') as f:
                    json_data = json.load(f)
                    prompts = [image['prompt'] for image in json_data['response']['images']]
                    all_prompts.extend(prompts)
        return all_prompts

    def _generate_image(self, prompt: str, retries: int = 0) -> str:
        """Generate an image using Replicate"""
        if retries >= MAX_RETRIES:
            raise Exception("Maximum number of retries reached")

        try:
            output = replicate.run(
                REPLICATE_CONFIG["model"],
                input=REPLICATE_CONFIG["default_params"] | {"prompt": prompt}
            )
            return output[0]
        except Exception as e:
            print(f"Error generating image (attempt {retries + 1}): {str(e)}")
            return self._generate_image(prompt, retries + 1)

    def _save_image(self, image_url: str) -> str:
        """Download and save the image"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.output_dir, f"{timestamp}.png")
        
        response = requests.get(image_url)
        with open(output_path, "wb") as f:
            f.write(response.content)
        return output_path

    def _upscale_image(self, input_path: str, retries: int = 0) -> str:
        """Perform upscale of an image"""
        if retries >= MAX_RETRIES:
            raise Exception("Maximum number of retries reached")

        try:
            with open(input_path, "rb") as f:
                output = replicate.run(
                    UPSCALE_CONFIG["model"],
                    input=UPSCALE_CONFIG["default_params"] | {"image": f}
                )
            return str(output)
        except Exception as e:
            print(f"Error making upscale (attempt {retries + 1}): {str(e)}")
            return self._upscale_image(input_path, retries + 1)

    def _validate_output_directory(self) -> bool:
        """Validate if the output directory exists and contains images"""
        if not os.path.exists(self.output_dir):
            print(f"Error: Directory not found: {self.output_dir}")
            return False
        
        image_files = [f for f in os.listdir(self.output_dir) 
                      if f.endswith(('.png', '.jpg', '.jpeg'))]
        if not image_files:
            print(f"Error: No images found in the directory: {self.output_dir}")
            return False
            
        return True

    def process_images(self) -> None:
        """Process all prompts and generate images"""
        try:
            prompts = self._collect_prompts()
            for prompt in prompts:
                try:
                    image_url = self._generate_image(prompt)
                    saved_path = self._save_image(image_url)
                    print(f"Image saved in: {saved_path}")
                except Exception as e:
                    print(f"Error processing prompt: {str(e)}")

        except Exception as e:
            print(f"Error during image processing: {str(e)}")

    def process_upscale(self) -> None:
        """Process the upscale of all images in the output directory"""
        if not self._validate_output_directory():
            return

        try:
            for filename in os.listdir(self.output_dir):
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    input_path = os.path.join(self.output_dir, filename)
                    output_path = os.path.join(self.upscale_dir, f"upscaled_{filename}")

                    try:
                        print(f"Processing upscale of: {filename}")
                        upscaled_url = self._upscale_image(input_path)
                        
                        response = requests.get(upscaled_url)
                        with open(output_path, "wb") as f:
                            f.write(response.content)
                        print(f"Upscaled image saved in: {output_path}")

                    except Exception as e:
                        print(f"Error processing upscale of {filename}: {str(e)}")

        except Exception as e:
            print(f"Error during upscale processing: {str(e)}")

def main():
    try:
        uuid = input("Enter the UUID of the directory to be processed: ")
        processor = ImageProcessor(uuid)
        
        print("\nChoose the operation:")
        print("1 - Generate images")
        print("2 - Upscale images")
        print("3 - Both")
        choice = input("Enter your choice (1, 2 or 3): ")
        
        if choice in ['1', '3']:
            processor.process_images()
        if choice in ['2', '3']:
            processor.process_upscale()
            
    except Exception as e:
        print(f"Error during execution: {str(e)}")

if __name__ == "__main__":
    main()