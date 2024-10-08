# TextToVideo

TextToVideo is an innovative tool designed for effortlessly creating AI-driven short videos. Leveraging the power of GPT-4, it crafts dynamic scripts that are brought to life through your choice of text-to-speech engines, including pyttsx3, ElevenLabs, gTTS or OpenAI TTS. The visual elements are enhanced with AI-generated backgrounds, utilizing DALL-E 3 or Flux-pro, tailored to your needs. To make the content even more engaging, captions with highlighted words are automatically generated using OpenAI Whisper, ensuring your videos captivate and inform.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Dinesh5aini/Text-to-Video.git
    cd Text-to-Video
    ```

2. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Install ImageMagick and FFmpeg:**
    - **For Windows:**
        - Download and install [ImageMagick](https://imagemagick.org/script/download.php) and [FFmpeg](https://ffmpeg.org/download.html).
        - Add the installation directories to your system's `PATH` environment variable.
    - **For macOS:**
        - Install via Homebrew:
        ```sh
        brew install imagemagick
        brew install ffmpeg
        ```
    - **For Linux:**
        - Install via package manager:
        ```sh
        sudo apt-get install imagemagick
        sudo apt-get install ffmpeg
        ```

4. **Set up environment variables:**
    - Create a `.env` file in the root directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```
    - Alternatively, you can set the API key via terminal:
    ```sh
    export OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

1. **Prepare the Source Material:**
   - Place your source material in the `artifacts/input/source_material.txt` file. This file should contain the text that will be used to generate the narration and images.

2. **Run the Main Script:**
   - Execute the main script to generate the video:
    ```sh
    python src/components/main.py
    ```

3. **Access the Generated Video:**
   - The video will be saved in the `artifacts/output` directory.

4. **Audio Generation Options:**
   - By default, the project uses `pyttsx3` for text-to-speech audio generation. If you wish to use a different TTS engine:
     - To use **Eleven Labs**, set the API key and specify the model in the parameters.
     - To use **OpenAI's TTS**, set up the necessary API keys.
     - Specify these options in the `audioGenerator` class within the project.

5. **Image Generation Options:**
   - If you're not using OpenAI for image generation, you can use **Flux-pro** via **Replicate**:
     - Set the API tokens for Replicate either in the `.env` file or directly in the terminal:
     ```env
     REPLICATE_API_TOKEN=your_replicate_api_token
     ```

## Project Structure

```plaintext
TextToVideo/
├── artifacts/
│   ├── input/
│   │   └── source_material.txt       # Place your input text file here
│   └── output/                       # Generated video and intermediate files will be stored here
│   
├── src/
│   └── components/
│       ├── main.py                   # Main script to run the video generation process
│       ├── audio.py                  # Module to generate audio from text
│       ├── images.py                 # Module to generate images based on text descriptions
│       ├── video.py                  # Script for managing video processing
│       ├── caption.py                # Module for handling captions within the video
│       ├── exception.py              # Module for managing exceptions
│       └── logger.py                 # Module for logging processes and errors
│   
├── .env                              # Environment variables, such as API keys
├── requirements.txt                  # Python dependencies
├── setup.py                          # Script for setting up the package
├── .gitignore                        # Git ignore file to exclude certain files and directories
└── README.md                         # Project documentation
