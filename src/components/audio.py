import os
import sys
import pyttsx3
from gtts import gTTS
from exception import customException
from logger import logging
import openai
import elevenlabs

class audioGenerator:
    def __init__(self, model="pyttsx3"):
        self.model = model

        if self.model == "pyttsx3":
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 200)
            self.engine.setProperty('volume', 2)
        elif self.model == "openai":
            openai.api_key = os.getenv("OPENAI_API_KEY")
        elif self.model == "elevenlabs":
            self.elevenlabs = elevenlabs
        elif self.model != "gTTS":
            raise ValueError(f"Unsupported model: {self.model}")

    def create(self, data, output_folder):
        try:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
                
            n = 0
            for element in data:
                if element["type"] != "text":
                    continue

                n += 1
                output_file = os.path.join(output_folder, f"tts_audio{n}.mp3")

                if self.model == "pyttsx3":
                    self.engine.save_to_file(element["content"], output_file)
                    self.engine.runAndWait()

                elif self.model == "openai":
                    response = openai.audio.speech.create(
                        model="tts-1",
                        voice="onyx",
                        input=element["content"],
                        speed=1.2
                    )
                    response.write_to_file(output_file)

                elif self.model == "gTTS":
                    tts = gTTS(element["content"], lang='en', tld='co.in')
                    tts.save(output_file)

                elif self.model == "elevenlabs":
                    audio = self.elevenlabs.generate(
                        text=element["content"],
                        voice="Josh",
                        model="eleven_multilingual_v2"
                    )
                    elevenlabs.save(audio, output_file)

                logging.info(f"Audio file saved: {output_file}")

        except Exception as e:
            logging.error("Error in audioGenerator.create", exc_info=True)
            raise customException(e, sys)

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