import os
from dotenv import load_dotenv
import google.generativeai as genai
import textwrap
from IPython.display import display
from IPython.display import Markdown

load_dotenv()

class model:
    model = None
    GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

    def __init__(self, env):
        genai.configure(api_key=self.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('models/gemini-2.0-flash-lite')


    def to_markdown(self,text):
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

    def run_model(self, text, image):
        content = f"{text} 정답만 작성해줘"
        if image is not None:
            content = [f"{text} 정답만 작성해줘",image]
        response = self.model.generate_content(content)
        resultText = self.to_markdown(response.text)
        return {resultText, response.text}
    
    def get_model_list(self):
        for m in genai.list_models():
          if 'generateContent' in m.supported_generation_methods:
            print(m.name)
    