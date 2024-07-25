from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
import sys
import tempfile
from exception import customException

class subtitleGenerator:
    
    def __init__(self, video_path, text_path, output_path):
        try:
            # Generate temporary SRT file
            srt_fd, srt_path = tempfile.mkstemp(suffix=".srt")
            os.close(srt_fd)
            self.text_to_srt(text_path, srt_path)

            # Load your video
            video = VideoFileClip(video_path)

            # Create a TextClip from the SRT file
            txt_clip = TextClip(filename=srt_path, 
                                fontsize = 70, 
                                color='white', 
                                method='caption', 
                                align='Center',
                                size=(video.size, None),
                                font='Arial',
                                stroke_color='black',
                                stroke_width=2)

            # Position the text at the bottom of the screen
            txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(video.duration)

            # Overlay the text on the video
            video_with_text = CompositeVideoClip([video, txt_clip])

            # Write the result to a file
            video_with_text.write_videofile(output_path, codec='libx264')

            # Remove the temporary SRT file
            if os.path.exists(srt_path):
                os.remove(srt_path)

        except Exception as e:
            raise customException(e, sys)
        
    def text_to_srt(self, text_path, srt_path, duration_per_line=2):
        with open(text_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    
        srt_content = ""
        index = 1
        start_time = 0
    
        for line in lines:
            # Create subtitle entry
            end_time = start_time + duration_per_line
            start_time_formatted = self.format_time(start_time)
            end_time_formatted = self.format_time(end_time)
    
            srt_content += f"{index}\n"
            srt_content += f"{start_time_formatted} --> {end_time_formatted}\n"
            srt_content += f"{line.strip()}\n\n"
    
            # Update for next subtitle
            index += 1
            start_time = end_time
    
        with open(srt_path, 'w', encoding='utf-8') as file:
            file.write(srt_content)
    
    def format_time(self, seconds):
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        seconds = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"