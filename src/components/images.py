import os
import openai
from dotenv import load_dotenv
from exception import customException
from logger import logging
import sys
import requests

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
                self.generate(prompt=element["description"] + ". Vertical image, fully filling the canvas.", output_file=os.path.join(output_dir, image_name))
                logging.info(f"Image file saved: {image_name}")
        except Exception as e:
            logging.error("Error in imageGenerator.create_from_data", exc_info=True)
            raise customException(e, sys)
        
    @staticmethod
    def generate(prompt, output_file, size="1024x1792"):
        try:
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                n=1
            )
    
            image_url = response.data[0].url if response.data else None
    
            img_data = requests.get(image_url).content
            with open(output_file, 'wb') as handler:
                handler.write(img_data)
            logging.info(f"Generated image from prompt: {prompt}")

        except Exception as e:
            logging.error("Error in imageGenerator.generate", exc_info=True)
            raise customException(e, sys)