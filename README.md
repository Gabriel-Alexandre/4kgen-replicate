# 🖼️ Replicate Image Generator Pro

**Turn your ideas into stunning 4K high-definition images with the power of AI!**

Welcome to Replicate Image Generator Pro, an open-source project that harnesses the capabilities of advanced AI models to transform simple text themes into breathtaking high-resolution images. This tool allows you to generate, upscale, and enhance images with professional quality results.

## ✨ Features

- 🤖 **AI-Powered Generation**: Uses advanced AI models to create unique images from text descriptions
- 🔍 **High-Resolution Output**: Upscales images to 4K quality with enhanced details
- 🎨 **Post-Processing**: Professional-grade image enhancement for stunning results
- 🌐 **Local or Cloud Models**: Flexibility to use both Replicate cloud models or your local LLM
- 🔒 **Privacy-Focused**: Keep your creations private with local processing options

## 🛠️ Prerequisites

Before getting started, make sure you have the following:

1. **Python**: Version 3.8 or higher installed on your system

2. **ImageMagick**: Required for post-processing operations
   - [Download ImageMagick](https://imagemagick.org/script/download.php)
   - Windows users: Use the installer from the official website
   - Linux users: Install via package manager (`apt-get install imagemagick` or similar)
   - Mac users: Install via Homebrew (`brew install imagemagick`)

3. **Replicate API Token**: For cloud-based image generation
   - Create an account at [Replicate](https://replicate.com)
   - Get your API token from your [account settings](https://replicate.com/account/api-tokens)

4. **[Optional] LM Studio**: For local LLM processing instead of using Replicate API
   - [Download LM Studio](https://lmstudio.ai)
   - Set up a local model (Recommended: Llama-3-8B or similar)
   - The application is pre-configured to work with LM Studio's default settings

## 🚀 Installation

1. **Create and activate a virtual environment**:
   - On Windows:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
   - On Linux/MacOS:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install the project dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file and configure your API token**:
   ```bash
   REPLICATE_API_TOKEN=your_token_here
   ```

## 🎮 How to Use

### Complete Workflow (Recommended)

The easiest way to use the application is through the complete workflow script:

```bash
cd code
python input_with_run.py
```

**The script will guide you through:**
1. Entering a theme for image generation
2. Selecting number of images to create
3. Choosing between local LLM (LM Studio) or Replicate for text processing
4. Automatically generating images based on AI-crafted prompts
5. Upscaling the images to 4K resolution
6. Applying post-processing for professional results

### Step-by-Step Manual Process

Alternatively, you can run each step manually:

1. **Generate Prompts**:
   ```bash
   cd code
   python input.py
   ```
   - Enter your theme and number of images
   - Choose your LLM type (local or Replicate)
   - The script will generate prompt files in the `prompts` directory

2. **Generate Images**:
   ```bash
   cd code
   python run.py
   ```
   - Enter the UUID provided by the previous step
   - Choose operation 1 to generate images
   - Images will be saved in the `output` directory

3. **Upscale Images**:
   ```bash
   cd code
   python run.py
   ```
   - Enter the same UUID as before
   - Choose operation 2 to upscale images
   - Upscaled images will be saved in the `upscaly` directory

4. **Post-Process Images**:
   ```bash
   cd code
   python pos_process.py
   ```
   - Enter the same UUID as before
   - Choose the input folder (upscaled images recommended)
   - Final results will be in the `pos_process` directory

## 🧰 Advanced Usage

### Using a Local LLM with LM Studio

1. Download and install [LM Studio](https://lmstudio.ai)
2. Download a compatible model (recommended: Llama-3-8B or similar)
3. Start the local server in LM Studio (Developer tab)
4. Choose the "Local" option when running the application

### Configuration Options

Advanced users can modify settings in `constants.py`:
- Change models used for image generation and upscaling
- Adjust post-processing parameters
- Configure the local LLM settings

## 📁 Project Structure

- `code/`: Main application code
  - `input.py`: Prompt generation from themes
  - `run.py`: Image generation and upscaling
  - `pos_process.py`: Image post-processing
  - `input_with_run.py`: Complete workflow script
  - `constants.py`: Configuration settings
- `prompts/`: Stored AI-generated prompts
- `output/`: Generated images
- `upscaly/`: Upscaled images
- `pos_process/`: Final post-processed images

## 🙏 Acknowledgments

This project leverages several incredible technologies:
- [Replicate](https://replicate.com) for cloud-based AI models
- [ImageMagick](https://imagemagick.org) for image processing
- [LM Studio](https://lmstudio.ai) for local LLM capabilities

## 📄 License

This project is open-source and free to use for personal and commercial purposes.

---

⭐ **Star this project if you find it useful!** ⭐

Happy image generating! 🎨✨
