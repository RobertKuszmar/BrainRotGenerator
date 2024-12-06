
import os
import json
import datetime
from dotenv import load_dotenv
from script_generator import ScriptGenerator
from audio_generator import AudioGenerator
from image_generator import ImageGenerator
from clip_editor import ClipEditor

def main():
    load_dotenv()

    gemini_key = os.getenv("GEMINI_API_KEY")
    script_generator = ScriptGenerator(gemini_key=gemini_key)
    audio_generator = AudioGenerator()
    image_generator = ImageGenerator()
    clip_editor = ClipEditor()

    output_dir = _generate_output_directory()

    topic = script_generator.generate_topic()
    with open(os.path.join(output_dir, "topic.json"), "w") as file:
        file.write(json.dumps(topic))

    script = script_generator.generate_script(topic)
    with open(os.path.join(output_dir, "script.json"), "w") as file:
        file.write(json.dumps(script))

    subtitles, audio_files, image_files = [], [], []
    for i, section in enumerate(script):
        audio_file_path = os.path.join(output_dir, f"audio_{i}.mp3")
        image_file_path = os.path.join(output_dir, f"image_{i}.png")
        audio_generator.tts_to_file(section["script_text"], audio_file_path)
        image_generator.save_image_to_file(section["image_description"], image_file_path)
        subtitles.append(section["script_text"])
        audio_files.append(audio_file_path)
        image_files.append(image_file_path)

    clip_editor.create_video_from_source_dir(output_dir)

def _generate_output_directory() -> str:
    timestamp_str = '{date:%Y-%m-%d_%H-%M-%S}'.format(date=datetime.datetime.now())
    curr_dir = os.path.dirname(__file__)
    output_dir_path = os.path.join(curr_dir, "output", timestamp_str)
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    return output_dir_path

if __name__ == "__main__":
    main()
