import os
import sys
from dotenv import load_dotenv
from exception import customException
from logger import logging
import requests as re
import base64
import openai
import replicate

class imageGenerator:
    def __init__(self):
        load_dotenv()
        # Initialize OpenAI client with your API key
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def create_from_data(self, data, output_dir, use_openai=False):
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            image_number = 0
            for element in data:
                if element["type"] != "image":
                    continue
                image_number += 1
                image_name = f"image_{image_number}.jpg"
                
                if use_openai:
                    self.generate_with_openai(
                        prompt=element["description"] + ". Vertical image, fully filling the canvas.",
                        output_file=os.path.join(output_dir, image_name)
                    )
                else:
                    self.generate_with_flux(
                        prompt=element["description"] + ". Vertical image, fully filling the canvas.",
                        output_file=os.path.join(output_dir, image_name)
                    )

                logging.info(f"Image file saved: {image_name}")

        except Exception as e:
            logging.error("Error in imageGenerator.create_from_data", exc_info=True)
            raise customException(e, sys)
        
    def generate_with_openai(self, prompt, output_file, size="1024x1792"):
        try:
            response = openai.Image.create(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                n=1,
                response_format="b64_json"
            )
            
            image_data = response['data'][0]['b64_json']
            
            with open(output_file, 'wb') as handler:
                handler.write(base64.b64decode(image_data))

            logging.info(f"Generated image from prompt: {prompt} using OpenAI")

        except Exception as e:
            logging.error("Error in imageGenerator.generate_with_openai", exc_info=True)
            raise customException(e, sys)

    def generate_with_flux(self, prompt, output_file, aspect_ratio="9:16"):
        try:
            input = {
                "prompt": prompt,
                "aspect_ratio": aspect_ratio
            }

            response = replicate.run(
                "black-forest-labs/flux-pro",
                input=input
            )

            image_data = re.get(response).content

            with open(output_file, 'wb') as handler:
                handler.write(image_data)

            logging.info(f"Generated image from prompt: {prompt} using Flux")

        except Exception as e:
            logging.error("Error in imageGenerator.generate_with_flux", exc_info=True)
            raise customException(e, sys)
