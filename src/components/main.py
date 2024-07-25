import os
import sys
from audio import audioGenerator
from images import imageGenerator
from video import videoGenerator
from exception import customException


from openai import OpenAI
import time
import json
import video

client = OpenAI()

with open(r'../../artifacts/input/source_material.txt','r') as f:
    source_material = f.read()

output_file = "output.mp4"

basedir = r'../../artifacts/output'
if not os.path.exists(basedir):
    os.makedirs(basedir)

print("Generating script...")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": """You are a YouTube short narration generator. You generate 30 seconds to 1 minute of narration. The shorts you create have a background that fades from image to image as the narration is going on.

You will need to generate descriptions of images for each of the sentences in about 2 lines. They will be passed to an AI image generator. DO NOT IN ANY CIRCUMSTANCES use names of celebrities or people in the image descriptions. It is illegal to generate images of celebrities. Only describe persons without their names. Do not reference any real person or group in the image descriptions. Don't mention the female figure or other sexual content in the images because they are not allowed.

You are however allowed to use any content, including real names in the narration. Only image descriptions are restricted.

Note that the narration will be fed into a text-to-speech engine, so don't use special characters.

Respond with a pair of an image description in square brackets and a narration below it. Both of them should be on their own lines, as follows:

###

[Description of a background image]

Narrator: "One sentence of narration"

[Description of a background image]

Narrator: "One sentence of narration"

[Description of a background image]

Narrator: "One sentence of narration"

###

The short should be 6 sentences maximum.

You should add a description of a fitting backround image in between all of the narrations. It will later be used to generate an image with AI.
"""
        },
        {
            "role": "user",
            "content": f"Create a YouTube short narration based on the following source material:\n\n{source_material}"
        }
    ]
)

response_text = response.choices[0].message.content
response_text.replace("’", "'").replace("`", "'").replace("…", "...").replace("“", '"').replace("”", '"')

with open(os.path.join(basedir,"temp", "response.txt"), "w") as f:
    f.write(response_text)

narration = audioGenerator()
data, narrations = narration.parse(response_text)
with open(os.path.join(basedir,"temp", "data.json"), "w") as f:
    json.dump(data, f, ensure_ascii=False)

print(f"Generating audio...")
narration.create(data, os.path.join(basedir, "audio"))

image = imageGenerator()
print("Generating images...")
image.create_from_data(data, os.path.join(basedir, "images"))

videos = videoGenerator()
print("Generating video...")
videos.create(os.path.join(basedir,"images"),os.path.join(basedir,"audio"), output_file)

print(f"DONE! Here's your video: {os.path.join(basedir, output_file)}")
