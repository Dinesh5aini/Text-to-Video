from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, ImageSequenceClip, concatenate_audioclips
import os
import sys
import numpy as np
from PIL import Image
from exception import customException
from logger import logging

class videoGenerator:

    @staticmethod
    def create(images_dir, audio_dir, output_file):
        try:
            frame_rate = 30
            resolution = (1080, 1920)  # Set desired resolution
            transition_duration = 1  # Set duration of transition in seconds

            # Get sorted list of images and audios
            images = sorted([os.path.join(images_dir, img) for img in os.listdir(images_dir) if img.endswith(('webp', 'png', 'jpg', 'jpeg', 'bmp'))])
            audios = sorted([os.path.join(audio_dir, aud) for aud in os.listdir(audio_dir) if aud.endswith(('mp3', 'wav'))])

            clips = []

            for i in range(len(images)):
                image_path = images[i]
                audio_path = audios[i]

                # Load audio
                audio_clip = AudioFileClip(audio_path)
                
                if i == 0:
                    # Create an ImageClip from the image
                    image_clip = ImageClip(image_path).set_duration(audio_clip.duration).resize(newsize=resolution)

                # If this is not the first image, create a transition from the previous image
                else:
                    prev_image_path = images[i - 1]
                    transition_frames = []
                    prev_image = np.array(Image.open(prev_image_path).resize(resolution))
                    curr_image = np.array(Image.open(image_path).resize(resolution))

                    # Generate transition frames
                    for alpha in np.linspace(0, 1, int(transition_duration * frame_rate)):
                        blended_image = videoGenerator.blend_images(prev_image, curr_image, alpha)
                        transition_frames.append(blended_image)

                    # Create a transition clip using the NumPy arrays
                    transition_clip = ImageSequenceClip([np.array(frame) for frame in transition_frames], fps=frame_rate)
                    clips.append(transition_clip)

                    # Create an ImageClip from the image
                    image_clip = ImageClip(image_path).set_duration((audio_clip.duration-transition_duration)).resize(newsize=resolution)

                clips.append(image_clip)
            
            audio_clip = concatenate_audioclips([AudioFileClip(audio) for audio in audios])
            
            # Concatenate all clips
            final_clip = concatenate_videoclips(clips, method="compose").set_audio(audio_clip)

            # Write the final video file
            final_clip.write_videofile(output_file, codec='libx264')

            logging.info(f"Video file saved: {output_file}")

        except Exception as e:
            logging.error("Error in videoGenerator.create", exc_info=True)
            raise customException(e, sys)

    @staticmethod
    def blend_images(image1, image2, alpha):
        try:
            return (image1 * (1 - alpha) + image2 * alpha).astype(np.uint8)
        except Exception as e:
            logging.error("Error in videoGenerator.blend_images", exc_info=True)
            raise customException(e, sys)
        
        

