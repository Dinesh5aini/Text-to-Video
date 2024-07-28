import os
import sys
# from elevenlabs.client import ElevenLabs
# from elevenlabs import save
from dotenv import load_dotenv
from exception import customException
from logger import logging
import openai
from pydub import AudioSegment

# from gtts import gTTS



class audioGenerator:
    def __init__(self):
        load_dotenv()
        # Initialize OpenAI client with your API key
        openai.api_key = os.getenv("OPENAI_API_KEY")

    #     self.elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    def create(self, data, output_folder,increased_volume=15):
        try:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            n = 0
            tmp_file = os.path.join(output_folder, "tmp.mp3")
            for element in data:
                if element["type"] != "text":
                    continue

                n += 1
                output_file = os.path.join(output_folder, f"tts_audio{n}.mp3")
                response = openai.audio.speech.create(
                    model="tts-1",
                    voice="onyx",
                    input=element["content"],
                    speed=1.25
                )
                response.write_to_file(tmp_file)

                audio = AudioSegment.from_file(output_file, format="mp3")
                louder_audio = audio + increased_volume
                louder_audio.export(output_file, format="mp3")

                os.remove(tmp_file)

                logging.info(f"Audio file saved: {output_file}")

        except Exception as e:
            logging.error("Error in audioGenerator.create", exc_info=True)
            raise customException(e, sys)

    # def create(self, data, output_folder):
    #     try:
    #         if not os.path.exists(output_folder):
    #             os.makedirs(output_folder)

    #         n = 0
    #         for element in data:
    #             if element["type"] != "text":
    #                 continue

    #             n += 1
    #             output_file = os.path.join(output_folder, f"tts_audio{n}.mp3")
    #             tts = gTTS(element["content"],lang = 'en',tld='co.in')
    #             tts.save(output_file)
    #             logging.info(f"Audio file saved: {output_file}")

    #     except Exception as e:
    #         logging.error("Error in audioGenerator.parse", exc_info=True)
    #         raise customException(e, sys)

    # def create(self, data, output_folder):
    #     try:
    #         if not os.path.exists(output_folder):
    #             os.makedirs(output_folder)

    #         n = 0
    #         for element in data:
    #             if element["type"] != "text":
    #                 continue

    #             n += 1
    #             output_file = os.path.join(output_folder, f"tts_audio{n}.mp3")
    #             audio = self.elevenlabs.generate(
    #                 text=element["content"],
    #                 voice="Josh",
    #                 model="eleven_multilingual_v2"
    #             )
    #             save(audio, output_file)
    #             logging.info(f"Audio file saved: {output_file}")

    #     except Exception as e:
    #         logging.error("Error in audioGenerator.create", exc_info=True)
    #         raise customException(e, sys)

    @staticmethod
    def parse(narration):
        try:
            data = []
            narrations = []
            lines = narration.split("\n")
            for line in lines:
                if line.startswith('Narrator: '):
                    text = line.replace('Narrator: ', '')
                    data.append({
                        "type": "text",
                        "content": text.strip('"'),
                    })
                    narrations.append(text.strip('"'))
                elif line.startswith('['):
                    background = line.strip('[]')
                    data.append({
                        "type": "image",
                        "description": background,
                    })
            return data, narrations
        except Exception as e:
            logging.error("Error in audioGenerator.parse", exc_info=True)
            raise customException(e, sys)
