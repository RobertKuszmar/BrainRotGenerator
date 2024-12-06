import json
import google.generativeai as genai

class ScriptGenerator:
    def __init__(self, gemini_key: str):
        genai.configure(api_key=gemini_key)
        self.model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config={"response_mime_type": "application/json"},  
        )

    def generate_topic(self) -> str:
        response = self.model.generate_content(f"""
            Generate a topic for a captivating 30 second short form video.
            The video should catch the viewer's attention instantly and be weird, scary, and/or unbelievable.
            The video will be narrated.
            The video will be accompanied by still images that change every few seconds.
            Return the output in this JSON schema:
                {{"topic" : str}}
        """)
        try:
            return json.loads(response.text)
        except Exception as e:
            print("Failed to parse topic response: " + e)
        return None

    def generate_script(self, topic: str) -> list[dict]:
        response = self.model.generate_content(f"""
            Generate a script for a short video about the following topic: "{topic}".
            The script should be broken up into a series of sentences.
            Each sentence is represented by a single image.
            Each sentence has a max length of 15 words.
            Reading the entire script should take no more than 45 seconds.
            Include facts in the script.
            Using this JSON schema:
                Paragraph = {{"script_text" : str, "image_description": str}}
            Return a `list[Paragraph]`.
        """)
        try:
            return json.loads(response.text)
        except Exception as e:
            print("Failed to parse script response: " + e)
        return None
