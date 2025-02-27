import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import pyautogui
from PIL import Image
from PIL import ImageEnhance
import pytesseract
import os
from dotenv import load_dotenv
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
load_dotenv()

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
MODEL = None
genai.configure(api_key=GOOGLE_API_KEY)
# MODEL = genai.GenerativeModel('models/gemini-2.0-flash')
MODEL = genai.GenerativeModel('models/gemini-2.0-flash-lite')

# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

def run_model(text,image):
    content = f"{text} 정답만 작성해줘"
    if image is not None:
       content = [f"{text} 정답만 작성해줘",image]
    response = MODEL.generate_content(content)
    resultText = to_markdown(response.text)
    return {resultText, response.text}

def crop_img():
   # 서바꼬르륵
   crop_size = (248, 66, 1217, 269)
   # 서바꼬르륵 외
   # crop_size = (248, 66, 1311, 431)
   crop_region = crop_region = crop_size
   mission = Image.open('./a.png')
   cropped_img = mission.crop(crop_region)

   cropped_img = cropped_img.convert('L')
   cropped_img = ImageEnhance.Contrast(cropped_img).enhance(3.0)

   text = pytesseract.image_to_string(cropped_img, lang='kor+eng', config='--psm 4')
   print(f"Q : {text}")
   orgTxt, markdownTxt  = run_model(text,cropped_img)
   print(f"A : {orgTxt}")
#    cropped_img.show()

if __name__ == '__main__':
  window_title  = 'MapleStory Worlds-QPlay Archive(서바이벌)'
  window = None

  for win in pyautogui.getAllWindows():
  # pyautogui.getWindowsWithTitle('MapleStory Worlds')
     if win.title == window_title:
        window = win
        # print(win)
#   print(window.title)
  window.resizeTo(1566, 1211)
  window.activate()
  window_x, window_y, window_width, window_height = window.left, window.top, window.width, window.height

  capture_x = window_x
  capture_y = window_y
  width = window_width
  height = window_height
  # 화면 캡쳐
  screenshot = pyautogui.screenshot(region=(capture_x, capture_y, width, height))
  screenshot.save(f"./a.png")

  crop_img()