import requests
import json
from datetime import datetime
import os
import uuid
import replicate
from typing import Dict
from constants import (
    DEFAULT_API_URL, 
    LM_STUDIO_CONFIG, 
    TEMPLATE_IMAGES, 
    REPLICATE_LLM_CONFIG,
    LLM_TYPES,
    PATH_TO_PROMPTS,
    MAX_RETRIES
)
from dotenv import load_dotenv


class PromptGenerator:
    def __init__(self, theme: str, num_images: int, llm_type: str = LLM_TYPES["local"]):
        self.theme = theme
        self.num_images = self._validate_num_images(num_images)
        self.llm_type = self._validate_llm_type(llm_type)
        self.execution_uuid = str(uuid.uuid4())
        self.output_dir = self._create_output_directory()

    @staticmethod
    def _validate_num_images(num: int) -> int:
        """Validate the number of images"""
        try:
            num = int(num)
            return max(1, num)
        except ValueError:
            return 1

    @staticmethod
    def _validate_llm_type(llm_type: str) -> str:
        """Validate the LLM type"""
        if llm_type not in [LLM_TYPES["local"], LLM_TYPES["replicate"]]:
            return LLM_TYPES["local"]
        return llm_type

    def _create_output_directory(self) -> str:
        """Create the output directory"""
        output_dir = os.path.join(PATH_TO_PROMPTS, self.execution_uuid)
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def _generate_timestamp(self) -> Dict[str, str]:
        """Generate the timestamp"""
        now = datetime.now()
        return {
            "date": now.strftime("%Y-%m-%d"),
            "hour": now.strftime("%H"),
            "minute": now.strftime("%M"),
            "second": now.strftime("%S")
        }

    def _save_response(self, response: str, iteration: int) -> None:
        """Save the response"""
        try:
            response_json = json.loads(response)
            final_json = {
                "timestamp": self._generate_timestamp(),
                "theme": self.theme,
                "response": response_json
            }
            
            now = datetime.now()
            filename = os.path.join(
                self.output_dir, 
                f"response_{now.strftime('%Y%m%d_%H%M%S')}_{iteration+1}.json"
            )
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(final_json, f, ensure_ascii=False, indent=4)
            
            print(f"File successfully saved at: {filename}")
                
        except json.JSONDecodeError as e:
            raise ValueError(f"Error converting response to JSON: {str(e)}")

    def generate_prompts(self) -> None:
        """Generate the prompts"""
        remaining_images = self.num_images
        iterations = (self.num_images + 1) // 2
        retries = 0

        i = 0
        while i < iterations:
            try:
                images_this_iteration = min(2, remaining_images)
                current_prompt = TEMPLATE_IMAGES.replace("[ABOUT]", self.theme)
                current_prompt = current_prompt.replace("[NUM_IMAGES]", str(images_this_iteration))
                
                print(f"\nGenerating file {i+1} of {iterations}...")
                response = self._generate_completion(current_prompt)
                
                self._save_response(response, i)
                remaining_images -= images_this_iteration
                i += 1

            except Exception as e:
                if retries < MAX_RETRIES:
                    while retries < MAX_RETRIES:
                        try:
                            print(f"Error in iteration {i+1}. Retrying... (Attempt {retries + 1} of {MAX_RETRIES})")
                            response = self._generate_completion(current_prompt)
                            self._save_response(response, i)
                            remaining_images -= images_this_iteration
                            i += 1
                            break
                        except Exception as retry_error:
                            retries += 1
                            if retries >= MAX_RETRIES:
                                print(f"Maximum number of retries reached for iteration {i+1}. Skipping to the next one.")
                                i += 1
                else:
                    print(f"Maximum number of retries reached. Ending generation.")
                    break

    def _generate_completion(self, prompt: str) -> str:
        """Generate the completion"""
        if self.llm_type == LLM_TYPES["local"]:
            return self._generate_completion_local(prompt)
        return self._generate_completion_replicate(prompt)

    def _generate_completion_local(self, prompt: str) -> str:
        """Generate the completion locally"""
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            **LM_STUDIO_CONFIG
        }
        
        try:
            response = requests.post(
                DEFAULT_API_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            
            raise ValueError(f"API error: Status code {response.status_code}")
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Request error: {str(e)}")

    def _generate_completion_replicate(self, prompt: str) -> str:
        """Generate the completion using Replicate"""
        load_dotenv()
        try:
            output = replicate.run(
                REPLICATE_LLM_CONFIG["model"],
                input={"prompt": prompt, **REPLICATE_LLM_CONFIG["default_params"]}
            )
            return "".join(output)
        except Exception as e:
            raise ValueError(f"Replicate error: {str(e)}")

def main():
    try:
        about = input("Write a THEME for the images that will be generated: ")
        num_images = input("Write the NUMBER of images that will be generated: ")
        
        print("\nChoose the LLM TYPE:")
        print("1 - Local (LM Studio)")
        print("2 - Replicate (Llama)")
        llm_choice = input("Enter your choice (1 or 2): ")
        
        llm_type = LLM_TYPES["local"] if llm_choice == "1" else LLM_TYPES["replicate"]
        
        generator = PromptGenerator(about, int(num_images), llm_type)
        generator.generate_prompts()
        
    except Exception as e:
        print(f"Error during execution: {str(e)}")

if __name__ == "__main__":
    main()