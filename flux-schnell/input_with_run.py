import uuid
from run import ImageProcessor
from input import PromptGenerator
from pos_process import ImagePostProcessor
from constants import LLM_TYPES

class CompleteFlowProcessor:
    def __init__(self, theme: str, num_images: int, llm_type: str = LLM_TYPES["local"]):
        """
        Initialize the complete flow processor.
        
        Args:
            theme (str): Theme for image generation
            num_images (int): Number of images to generate
            llm_type (str): Type of LLM to use (local or replicate)
        """
        self.theme = theme
        self.num_images = self._validate_num_images(num_images)
        self.llm_type = self._validate_llm_type(llm_type)
        self.execution_uuid = str(uuid.uuid4())

    @staticmethod
    def _validate_num_images(num: int) -> int:
        """
        Validate and adjust the number of images
        
        Args:
            num (int): Number of images to validate
            
        Returns:
            int: Validated number of images
        """
        try:
            num = int(num)
            return max(1, num)
        except ValueError:
            return 1

    @staticmethod
    def _validate_llm_type(llm_type: str) -> str:
        """
        Validate the LLM type
        
        Args:
            llm_type (str): LLM type to validate
            
        Returns:
            str: Validated LLM type
        """
        if llm_type not in [LLM_TYPES["local"], LLM_TYPES["replicate"]]:
            return LLM_TYPES["local"]
        return llm_type

    def process_complete_flow(self) -> None:
        """Execute the complete flow of prompt generation and image processing"""
        try:
            # Step 1: Generate Prompts
            print("\n=== Generating prompts ===")
            prompt_generator = PromptGenerator(
                theme=self.theme,
                num_images=self.num_images,
                llm_type=self.llm_type
            )
            prompt_generator.execution_uuid = self.execution_uuid
            prompt_generator.output_dir = prompt_generator._create_output_directory()
            prompt_generator.generate_prompts()
            
            # Step 2: Generate Images
            print("\n=== Generating images ===")
            image_processor = ImageProcessor(self.execution_uuid)
            image_processor.process_images()

            # Step 3: Generate Upscales
            print("\n=== Generating image upscales ===")
            image_processor.process_upscale()

            # Step 4: Post-process upscaled images
            print("\n=== Post-processing upscaled images ===")
            post_processor = ImagePostProcessor(
                uuid_dir=self.execution_uuid,
                input_folder="upscaly"
            )
            post_processor.process_images()

            print("\nComplete flow executed successfully!")
            print(f"Execution UUID: {self.execution_uuid}")

        except Exception as e:
            print(f"Error during complete flow execution: {str(e)}")

def main():
    try:
        # Get theme input
        theme = input("Enter a theme for the images to be generated: ")
        
        # Get number of images input
        while True:
            try:
                num_images = int(input("Enter the number of images to be generated: "))
                if num_images > 0:
                    break
                print("Please enter a number greater than 0")
            except ValueError:
                print("Please enter a valid number")

        # Get LLM type input
        print("\nChoose the LLM TYPE:")
        print("1 - Local (LM Studio)")
        print("2 - Replicate (Llama)")
        
        while True:
            llm_choice = input("Enter your choice (1 or 2): ")
            if llm_choice in ['1', '2']:
                break
            print("Please enter 1 or 2")

        llm_type = LLM_TYPES["local"] if llm_choice == "1" else LLM_TYPES["replicate"]

        # Initialize and run complete flow
        processor = CompleteFlowProcessor(
            theme=theme,
            num_images=num_images,
            llm_type=llm_type
        )
        
        # Show execution plan
        print("\nExecution plan:")
        print("1. Generate prompts using selected LLM")
        print("2. Generate images from prompts")
        print("3. Upscale generated images")
        print("4. Post-process upscaled images")
        
        # Confirm execution
        while True:
            confirm = input("\nProceed with execution? (y/n): ").lower()
            if confirm in ['y', 'n']:
                break
            print("Please enter 'y' or 'n'")

        if confirm == 'y':
            processor.process_complete_flow()
        else:
            print("Execution cancelled by user")
        
    except Exception as e:
        print(f"Error during execution: {str(e)}")
    finally:
        print("\nExecution finished")

if __name__ == "__main__":
    main()