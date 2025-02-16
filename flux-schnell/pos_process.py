import os
import subprocess
from typing import List

MAX_RETRIES = 5
PATH_TO_UPSCALE = "./upscaly"
PATH_TO_POS_PROCESS = "./pos_process"

class ImagePostProcessor:
    def __init__(self, uuid_dir: str, input_folder: str = "upscaly"):
        """
        Initialize the post-processor for images.
        
        Args:
            uuid_dir (str): UUID of the directory to be processed
            input_folder (str): Input folder to process ('upscaly' or 'output')
        """
        self.uuid_dir = uuid_dir
        self.input_folder = input_folder
        self.input_dir = os.path.join(f"./{input_folder}", uuid_dir)
        self.output_dir = os.path.join("./pos_process", uuid_dir)
        self._create_output_directory()

    def _create_output_directory(self) -> None:
        """Create the output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _validate_input_directory(self) -> bool:
        """Validate if the input directory exists and contains images"""
        if not os.path.exists(self.input_dir):
            print(f"Error: Input directory not found: {self.input_dir}")
            return False
        
        valid_extensions = ('.png', '.jpg', '.jpeg') if self.input_folder == "output" else ('.png',)
        image_files = [f for f in os.listdir(self.input_dir) 
                      if f.endswith(valid_extensions)]
        
        if not image_files:
            print(f"Error: No valid images found in directory: {self.input_dir}")
            return False
            
        return True

    def _build_imagemagick_command(self) -> List[str]:
        """Build the ImageMagick command with all parameters"""
        file_pattern = "*.png" if self.input_folder == "upscaly" else "*.{png,jpg,jpeg}"
        return [
            "magick", "mogrify",
            "-sharpen", "0x1",
            "-contrast-stretch", "2%x98%",
            "-brightness-contrast", "-5x10",
            "-modulate", "95,105",
            "-colorize", "5,2,0",
            "-attenuate", "0.5",
            "+noise", "Gaussian",
            "-path", self.output_dir,
            os.path.join(self.input_dir, file_pattern)
        ]

    def _execute_imagemagick(self, command: List[str], retries: int = 0) -> bool:
        """
        Execute the ImageMagick command with retry logic
        
        Args:
            command (List[str]): Command to be executed
            retries (int): Current retry attempt
            
        Returns:
            bool: True if successful, False otherwise
        """
        if retries >= MAX_RETRIES:
            print("Error: Maximum number of retries reached")
            return False

        try:
            print("Executing ImageMagick command...")
            print(f"Command: {' '.join(command)}")
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("Processing completed successfully!")
                return True
                
            print(f"Error processing images: {result.stderr}")
            return self._execute_imagemagick(command, retries + 1)
            
        except Exception as e:
            print(f"Error during processing (attempt {retries + 1}): {str(e)}")
            return self._execute_imagemagick(command, retries + 1)

    def process_images(self) -> None:
        """Process all images in the input directory"""
        try:
            if not self._validate_input_directory():
                return

            command = self._build_imagemagick_command()
            success = self._execute_imagemagick(command)
            
            if not success:
                print("Failed to process images after all retry attempts")
                
        except Exception as e:
            print(f"Error during image processing: {str(e)}")

def main():
    try:
        uuid = input("Enter the UUID of the directory to be processed: ")
        
        print("\nChoose the input folder:")
        print("1 - Upscaled images (from upscaly folder)")
        print("2 - Original images (from output folder)")
        folder_choice = input("Enter your choice (1 or 2): ")
        
        input_folder = "upscaly" if folder_choice == "1" else "output"
        
        processor = ImagePostProcessor(uuid, input_folder)
        processor.process_images()
        
    except Exception as e:
        print(f"Error during execution: {str(e)}")

if __name__ == "__main__":
    main()
