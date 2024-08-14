from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, ImageSequenceClip, concatenate_audioclips, vfx, CompositeVideoClip
import os
import sys
import numpy as np
from PIL import Image
from exception import customException
from logger import logging
from caption import CaptionGenerator
import tempfile

class videoGenerator:

    @staticmethod
    def create(images_dir, audio_dir, output_file, font,color = "white", word_highlight_color = "yellow", line_count = 2, font_size = 90 ,stroke_width = 2,stroke_color = "black", resolution = (1080, 1920), shadow_blur_radius = 10, opacity = 1.0, bg_blur =False):
        try:
            frame_rate = 30
            transition_duration = 1  

            # Get sorted list of images and audios
            images = sorted([os.path.join(images_dir, img) for img in os.listdir(images_dir)])
            audios = sorted([os.path.join(audio_dir, aud) for aud in os.listdir(audio_dir) ])

            clips = []

            for i in range(len(images)):
                image_path = images[i]
                audio_path = audios[i]

                # Load audio
                audio_clip = AudioFileClip(audio_path)

                if i == 0:
                    # Create an ImageClip from the image
                    image_clip = ImageClip(image_path).set_duration(audio_clip.duration).resize(newsize=resolution)
                    image_clip = videoGenerator.apply_fadein(image_clip, duration=1) # if first clip, then apply fade in effect

                # If this is not the first image, create a transition from the previous image
                if i > 0: 
                    prev_image_path = images[i - 1]
                    transition_frames = []
                    prev_image = np.array(Image.open(prev_image_path))
                    curr_image = np.array(Image.open(image_path))
                    
                    for alpha in np.linspace(0, 1, int(frame_rate * transition_duration)):
                        blended_image = videoGenerator.blend_images(prev_image, curr_image, alpha)
                        blended_frame = ImageClip(blended_image, duration=1/frame_rate).resize(newsize=resolution)
                        transition_frames.append(blended_frame)
                
                    clips.extend(transition_frames)
                    image_clip = ImageClip(image_path).set_duration(audio_clip.duration-transition_duration).resize(newsize=resolution)
                
                if i == len(images) - 1:
                    image_clip = videoGenerator.apply_fadeout(image_clip, duration=1) # if last clip, then apply fade out effect

                clips.append(image_clip)
            
            audio_clip = concatenate_audioclips([AudioFileClip(audio) for audio in audios]) # combine all audio clips into a single audio clip

            clips = concatenate_videoclips(clips).set_audio(audio_clip) #concatenate all the video frames in sequence

            tmp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name

            audio_clip.write_audiofile(tmp_audio, codec='libmp3lame',verbose=False, logger=None) # write the audio to a temporary file

            logging.info("Generating captions...")
            
            print("Generating captions...")
            # generate the caption clips for the video
            clps = CaptionGenerator.captions( 
                audio_file=tmp_audio,
                color=color,
                highlight_color=word_highlight_color,
                stroke_color=stroke_color,
                font_size=font_size,
                font= font, 
                stroke_width=stroke_width, 
                resolution=resolution,
                line_count=line_count,
                shadow_blur_radius=shadow_blur_radius,
                opacity=opacity,
                bg_blur=bg_blur
                )

            # overlaping the caption frames over the video clip 
            final_clip = CompositeVideoClip([clips]+clps).set_duration(audio_clip.duration) 

            # fr = final_clip.get_frame(1) # get the first frame of the final clip
            # fr = Image.fromarray(fr) # convert the frame to an image
            # fr.save('test.png') # save the first frame as the output file
            # quit()

            # Write the final video file
            final_clip.write_videofile(output_file, codec='libx264', fps=frame_rate, verbose=False)
            
            logging.info(f"Video file saved: {output_file}")

        except Exception as e:
            logging.error("Error in videoGenerator.create", exc_info=True)
            raise customException(e, sys)
        
    @staticmethod
    def apply_fadein(clip, duration=1):
        try:
            return clip.fx(vfx.fadein, duration)
        except Exception as e:
            logging.error("Error in videoGenerator.apply_fadein", exc_info=True)
            raise customException(e, sys)
        
    @staticmethod
    def apply_fadeout(clip, duration=1):
        try:
            return clip.fx(vfx.fadeout, duration)
        except Exception as e:
            logging.error("Error in videoGenerator.apply_fadeout", exc_info=True)
            raise customException(e, sys)

    @staticmethod
    def blend_images(image1, image2, alpha):
        try:
            return (image1 * (1 - alpha) + image2 * alpha).astype(np.uint8)
        except Exception as e:
            logging.error("Error in videoGenerator.blend_images", exc_info=True)
            raise customException(e, sys)