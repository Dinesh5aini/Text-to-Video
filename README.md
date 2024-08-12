# TextToVideo

TextToVideo is a Python project that generates short video narrations with AI-generated images based on provided source material. The project uses OpenAI's GPT-4 model to create narrations and descriptions for images, which are then used to generate a video.

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
│   ├── output/                       # Generated video and intermediate files will be stored here
│   └── temp/                         # Temporary files used during video generation
├── src/
│   ├── components/
│   │   ├── main.py                   # Main script to run the video generation process
│   │   ├── text_generator.py         # Module to generate text narration using GPT-4
│   │   ├── image_generator.py        # Module to generate images based on text descriptions
│   │   ├── video_creator.py          # Module to create video from images and narration
│   └── utils/
│       ├── helpers.py                # Helper functions for various tasks
│       └── config.py                 # Configuration settings and environment management
├── .env                              # Environment variables, such as API keys
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
