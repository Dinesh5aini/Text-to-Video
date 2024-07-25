import base64
import os
import openai
from dotenv import load_dotenv
from exception import customException
import sys

class imageGenerator:
    def __init__(self):
        load_dotenv()
        # Initialize OpenAI client with your API key
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def create_from_data(self, data, output_dir):
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            image_number = 0
            for element in data:
                if element["type"] != "image":
                    continue
                image_number += 1
                image_name = f"image_{image_number}.webp"
                self.generate(element["description"] + ". Vertical image, fully filling the canvas.", os.path.join(output_dir, image_name))
        except Exception as e:
            raise customException(e, sys)
        
    @staticmethod
    def generate(self, prompt, output_file, size="1024x1792"):
        try:
            response = openai.Image.create(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                n=1
            )
    
            image_b64 = response['data'][0]['b64_json']
    
            with open(output_file, "wb") as f:
                f.write(base64.b64decode(image_b64))
    
        except Exception as e:
            print(f"An error occurred while generating the image: {e}")