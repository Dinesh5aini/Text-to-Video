import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import sys
from exception import customException

class audioGenerator:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

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
                audio = self.elevenlabs.generate(
                    text=element["content"],
                    voice="Sanjay",
                    model="eleven_multilingual_v2"
                )
                save(audio, output_file)

        except Exception as e:
            raise customException(e, sys)

    @staticmethod
    def parse(narration):
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
