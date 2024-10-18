from exception import customException
from logger import logging
from moviepy.editor import TextClip, ImageClip
from PIL import Image, ImageFilter
from typing import Callable
import numpy as np
import whisper
import sys
import json

class CaptionGenerator:

    @classmethod
    def captions(cls,audio_file,resolution,color, highlight_color, stroke_color, shadow_blur_radius,opacity,bg_blur, font = "Arial",font_size = 100, stroke_width= 2,line_count = 2):
        try:
            max_line_width = resolution[0] - 100

            logging.info("Generating audio transcriptions...")
            # Generating audio transcriptions
            segments = cls.transcribe_audio(audio_file)

            logging.info("Parsing audio transcriptions...")
            captions = cls.parse(segments, cls.fits_frame(line_count, font, font_size, stroke_width, max_line_width))

            # with open('caption.json', 'w') as f:
            #     json.dump(captions, f, indent=4)

            # with open('caption.json') as f:
            #     captions = json.load(f)

            word_clps = []
            shadow_clps = []

            for caption in captions:
                word_clips, shadows= cls.create_caption(
                    caption= caption, framesize=resolution, font=font,color=color, highlight_color= highlight_color, stroke_color=stroke_color, stroke_width= stroke_width, shadow_blur_radius=shadow_blur_radius,
                    opacity=opacity, fontsize=font_size, bg_blur=bg_blur
                )
                shadow_clps.extend(shadows)
                word_clps.extend(word_clips)
            
            shadow_clps.extend(word_clps)

            logging.info("Caption clips generated successfully.")
            return shadow_clps
        except Exception as e:
            logging.error("Error in CaptionGenerator.captions", exc_info=True)
            raise customException(e, sys)

    @staticmethod
    def transcribe_audio(audio_file: str, prompt: str = None):
        try:
            model = whisper.load_model("base")

            transcription = model.transcribe(
                audio=audio_file,
                word_timestamps=True,
                fp16=False,
                initial_prompt=prompt,
            )

            return transcription["segments"]
        except Exception as e:
            logging.error("Error in CaptionGenerator.transcribe_audio", exc_info=True)
            raise customException(e, sys)

    @staticmethod
    def parse(segments: list[dict], fit_function: Callable, allow_partial_sentences: bool = False):
        try:
            captions = []
            caption = {"start": None, "end": 0, "words": [], "text": []}

            for segment in segments:
                words = segment["words"]
                i = 0
                while i < len(words) - 1:
                    if words[i + 1]["word"][0] != " ":
                        words[i]["word"] += words[i + 1]["word"]
                        words[i]["end"] = words[i + 1]["end"]
                        del words[i + 1]
                    else:
                        i += 1

            for segment in segments:
                for word in segment["words"]:
                    if caption["start"] is None:
                        caption["start"] = word["start"]
                    # let's join the lines inside the line keys of dict inside the caption["text"]
                    text = " ".join([line["line"] for line in caption["text"]])
                    text += word["word"]
                    caption_fits = allow_partial_sentences or not CaptionGenerator.has_partial_sentence(text)
                    lines_list, val = fit_function(text)
                    caption_fits = caption_fits and val

                    if caption_fits:
                        caption["words"].append(word)
                        caption["end"] = word["end"]
                        caption["text"] = lines_list
                    else:
                        captions.append(caption)
                        lines_list, _ = fit_function(word["word"].strip())
                        caption = {"start": word["start"], "end": word["end"], "words": [word], "text": lines_list}

            captions.append(caption)
            return captions
        except Exception as e:
            logging.error("Error in CaptionGenerator.parse", exc_info=True)
            raise customException(e, sys)

    @staticmethod
    def has_partial_sentence(text):
        try:
            words = text.split()
            if len(words) >= 2:
                prev_word = words[-2].strip()
                if prev_word[-1] == ".":
                    return True
            return False
        except Exception as e:
            logging.error("Error in CaptionGenerator.has_partial_sentence", exc_info=True)
            raise customException(e, sys)

    @staticmethod
    def fits_frame(line_count, font, font_size, stroke_width, max_line_width):
        try:
            def fit_function(text):
                lines = CaptionGenerator.calculate_lines(text, font, font_size, stroke_width, max_line_width)
                return lines, len(lines) <= line_count
            return fit_function

        except Exception as e:
            logging.error("Error in CaptionGenerator.fits_frame", exc_info=True)
            raise customException(e, sys)
        
    @staticmethod
    def calculate_lines(text, font, font_size, stroke_width, max_line_width):
        try:
            lines = []
            line = ""
            words = text.split()
            word_index = 0
            line_to_draw = None

            while word_index < len(words):
                word = words[word_index]
                line += word + " "
                text_size = CaptionGenerator.get_text_size(line.strip(), font, font_size, stroke_width)
                text_width = text_size[0]

                if text_width < max_line_width:
                    line_to_draw = {'line' : line.strip(),'line_width' : text_width}
                    word_index += 1
                else:
                    if not line_to_draw:
                        print(f"NOTICE: Word '{line.strip()}' is too long for the frame!")
                        line_to_draw ={'line' : line.strip(),'line_width' : text_width}
                        word_index += 1

                    lines.append(line_to_draw)
                    line_to_draw = None
                    line = ""

            if line_to_draw:
                lines.append(line_to_draw)

            return lines
        
        except Exception as e:
            logging.error("Error in CaptionGenerator.calculate_lines", exc_info=True)
            raise customException(e, sys)

    @staticmethod
    def get_text_size(text, font, fontsize, stroke_width):
        try:
            text_clip = TextClip(text, fontsize=fontsize, color='white', font=font, stroke_color='black', stroke_width=stroke_width).set_position(('center', 'center'))
            text_clip_size = text_clip.size
            text_clip.close()
            return text_clip_size
        except Exception as e:
            logging.error("Error in CaptionGenerator.get_text_size", exc_info=True)
            raise customException(e, sys)
        
    @staticmethod
    def create_shadow(text: str, font_size: int, font: str, blur_radius: float = 5, opacity: float = 1.0) -> ImageClip:
        try:
            # Create the initial shadow as a TextClip
            shadow_clip = TextClip(text, fontsize=font_size, font=font, color="black", stroke_width=0, bg_color='transparent').set_opacity(opacity)
            
            # Convert TextClip to a numpy array (image)
            img_array = shadow_clip.get_frame(0)
            pil_img = Image.fromarray(img_array).convert("RGBA")

            pil_img = pil_img.resize((pil_img.width, font_size*9//10))
    
            # Determine padding size based on font size and blur radius
            padding = int(blur_radius)  # Adjust this factor as needed to fit the shadow effect
            padded_width = pil_img.width + padding
            padded_height = pil_img.height + padding
            
            # Create a new image with padding
            pil_img_padded = Image.new("RGBA", (padded_width, padded_height))
            
            # Paste the original image onto the padded image
            pil_img_padded.paste(pil_img, (padding//2, padding//2))
    
            # Apply Gaussian blur to create the shadow effect
            pil_img_blurred = pil_img_padded.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            
            # Convert the blurred PIL image back to an ImageClip
            blurred_clip = ImageClip(np.array(pil_img_blurred))
            
            return blurred_clip, shadow_clip.h
        except Exception as e:
            raise customException(e, sys)

    
    @staticmethod
    def create_caption(caption: dict, framesize: tuple, font: str = "Helvetica",fontsize: int = 50 , color: str = 'white', highlight_color: str = 'yellow', stroke_color: str = 'black', stroke_width: float = 1.5, shadow_blur_radius: float = 0.1, opacity: float = 1.0, bg_blur: bool = True):
        try:
            full_duration = caption['end'] - caption['start']
            frame_width = framesize[0]
            frame_height = framesize[1]

            y_pos = frame_height // 2 - fontsize  # Vertical starting position
            space_width = TextClip(" ", font=font, fontsize=fontsize, color=color).size[0]
            word_clips = []
            shadows = []

            # Index to track the current word in the list
            current_word_index = 0
            word_count = len(caption['words'])

            for line_info in caption['text']:
                line = line_info['line']
                line_width = line_info['line_width']
                x_start_pos = (frame_width - line_width) // 2
                x_pos = x_start_pos

                if bg_blur:
                    shadow, w_clip_height = CaptionGenerator.create_shadow(line.strip(), font_size=fontsize, font=font,blur_radius= shadow_blur_radius,opacity=opacity)
                    shadow.set_start(caption["start"]).set_duration(full_duration)

                    shadow_x_pos = x_pos - shadow_blur_radius//2
                    shadow_y_pos = y_pos - (shadow.h - w_clip_height) // 2
                    shadow = shadow.set_position((shadow_x_pos, shadow_y_pos))
                    shadows.append(shadow)


                # Process words that belong to the current line
                while current_word_index < word_count:
                    word = caption['words'][current_word_index]
                    if word['word'].lstrip() in line:
                        duration = word['end'] - word['start']

                        word_clip = TextClip(word['word'].lstrip(), font=font, fontsize=fontsize, color=color, stroke_color=stroke_color, stroke_width=stroke_width).set_start(caption['start']).set_duration(full_duration)

                        highlight_word_clip = TextClip(word['word'].lstrip(), font=font, fontsize=fontsize, color=highlight_color, stroke_color=stroke_color, stroke_width=stroke_width).set_start(word['start']).set_duration(duration)

                        word_width, word_height = word_clip.size
                        word_clip = word_clip.set_position((x_pos, y_pos))
                        highlight_word_clip = highlight_word_clip.set_position((x_pos, y_pos))

                        word_clips.extend([ word_clip, highlight_word_clip])
                        x_pos += word_width + space_width - shadow_blur_radius
                        current_word_index += 1
                    else:
                        break
                                          
                y_pos += word_height + 10  # Move to the next line vertically

            return word_clips, shadows

        except Exception as e:
            logging.error("Error in CaptionGenerator.create_caption", exc_info=True)
            raise customException(e, sys)