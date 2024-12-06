import os
import re
import json
import random
from moviepy.editor import *

class ClipEditor:
    def __init__(self):
        return

    def create_video_from_source_dir(self, source_dir: str) -> None:
        subtitles = []
        script_file_path = os.path.join(source_dir, "script.json")
        with open(script_file_path, "r") as script_file:
            script_data = json.load(script_file)
            for entry in script_data:
                subtitles.append(entry["script_text"])

        audio_file_paths = [None] * len(subtitles)
        image_files_path = [None] * len(subtitles)
        for file_name in os.listdir(source_dir):
            full_path = os.path.join(source_dir, file_name)
            index_match = re.search(r'\d+', file_name)
            if not index_match:
                continue
            index = int(index_match.group())
            if file_name.startswith("audio"):
                audio_file_paths[index] = full_path
            elif file_name.startswith("image"):
                image_files_path[index] = full_path

        self._create_video(
            subtitles=subtitles, 
            audio_files=audio_file_paths, 
            image_files=image_files_path,
            file_path=os.path.join(source_dir, "final_clip.mp4"))


    def _create_video(self, subtitles: list[str], audio_files: list[str], image_files: list[str], file_path: str) -> None:
        if len(subtitles) != len(audio_files) != len(image_files):
            print("Error creating video: mismatched input array sizes!")
            return
        
        for i in range(len(subtitles)):
            if subtitles[i] == None or audio_files[i] == None or image_files[i] == None:
                print("Error creating video: None found in input data lists!")
                return

        image_clips = []
        curr_time = 0

        for i in range(len(subtitles)):
            audio_clip = AudioFileClip(audio_files[i])
            end_time = curr_time + audio_clip.duration

            image_clip = (ImageClip(image_files[i])
                        .resize(newsize=(1080,960))
                        .resize(lambda t: 1 + 0.04 * t))
            
            text_clip = (TextClip(subtitles[i], font="Amiri-regular", fontsize=56, color="white", stroke_width=3, method="caption", size=(600, 0))
                        .set_position(('center', image_clip.h - 100)))
            text_clip = text_clip.set_position(('center', image_clip.h - text_clip.h - 100))

            image_with_text = (CompositeVideoClip([image_clip, text_clip])
                        .set_duration(audio_clip.duration)
                        .resize(newsize=(1080,960))
                        .set_position(('center', 'center'))
                        .set_fps(60)
                        .set_start(curr_time)
                        .set_end(end_time)
                        .set_audio(audio_clip))

            image_clips.append(image_with_text)
            curr_time = end_time
        concatenated_images_clip = concatenate_videoclips(image_clips)

        filler_file_path = self._get_random_filler_clip()
        filler_clip = VideoFileClip(filler_file_path)
        max_end = filler_clip.duration - concatenated_images_clip.duration
        random_start = random.uniform(0, max_end)
        print("here 2")
        filler_clip = (filler_clip
                       .subclip(random_start, random_start + concatenated_images_clip.duration)
                       .set_audio(None)
                       .resize(newsize=(1080,960)))
        
        final_clip = clips_array([[concatenated_images_clip], [filler_clip]])
        final_clip.write_videofile(file_path,
                                   fps=60,
                                   threads=os.cpu_count())

        for image_clip in image_clips:
            image_clip.close()
        filler_clip.close()
        final_clip.close()

    def _get_random_filler_clip(self1):
        curr_path = os.path.dirname(__file__)
        filler_clip_dir = os.path.join(curr_path, "filler-clips")
        filler_file_paths = [os.path.join(filler_clip_dir, file_name) for file_name in os.listdir(filler_clip_dir)]
        return random.choice(filler_file_paths)
            