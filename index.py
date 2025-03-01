import pyautogui
from PIL import Image
from PIL import ImageEnhance
import pytesseract
import os
from dotenv import load_dotenv
from model import model

import cv2 as cv
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
load_dotenv()

def get_img_match(org_img, match_img):
  result = cv.matchTemplate(org_img, match_img, cv.TM_CCOEFF_NORMED)

  threshold = 0.6
  locations = list(zip(*np.where(result >= threshold)[::-1]))
#   print(len(locations))

  return locations

def get_game_name(image):
  game_name = ''
  image = cv.imread("./a.png", cv.IMREAD_REDUCED_COLOR_2)
  kkong_img = cv.imread("./game_img/kkong.png", cv.IMREAD_REDUCED_COLOR_2)
  olla_img = cv.imread("./game_img/olla.png", cv.IMREAD_REDUCED_COLOR_2)
  hamburger_img = cv.imread("./game_img/hamburger.png", cv.IMREAD_REDUCED_COLOR_2)

  kkong_locations = get_img_match(image, kkong_img)
  olla_locations = get_img_match(image, olla_img)
  hamburger_locations = get_img_match(image, hamburger_img)

  if hamburger_locations:
     game_name = 'hamburger'
  elif kkong_locations:
     game_name = 'kkong'
  elif olla_locations:
     game_name = 'olla'
  else:
     game_name = ''

#   if locations:
#    img_w = kkong_img.shape[1]
#    img_h = kkong_img.shape[0]
#    line_color = (0, 255, 0)
#    line_type = cv.LINE_4

#    for loc in locations:
#       print('aa')
#       top_left = loc
#       bottom_right = (loc[0] + img_w, loc[1] + img_h)
#       cv.rectangle(image, top_left, bottom_right, line_color, line_type)

#    cv.imshow('Matches', image)
#    cv.waitKey()
#    cv.imwrite('./zxc.jpg', arena_img)

  return game_name

def crop_img(image, game_name):
   
   # 꽁꽁
   if game_name == 'kkong':
      crop_size = (248, 66, 1217, 269)
   elif game_name == 'olla':
      crop_size = (262, 88, 1299, 381)
   else:
      crop_size = (248, 66, 1311, 431)

   crop_region = crop_region = crop_size
   cropped_img = image.crop(crop_region)

   return cropped_img

def run_ocr(cropped_img, game_name):
   cropped_img = cropped_img.convert('L')
   cropped_img = ImageEnhance.Contrast(cropped_img).enhance(3.0)

   if game_name != 'kkong':
      cropped_img = ImageEnhance.Color(cropped_img).enhance(0)
      cropped_img = ImageEnhance.Contrast(cropped_img).enhance(3.0)
      cropped_img = ImageEnhance.Brightness(cropped_img).enhance(0.8)
      cropped_img = ImageEnhance.Sharpness(cropped_img).enhance(3)

   # cropped_img.show()

   text = pytesseract.image_to_string(cropped_img, lang='kor+eng', config='--psm 4')
   text = text.replace('|', '')
   text = text.replace('ㅣ', '')

   return text

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def dict_search(keyword, game_name):
   file_path = ''
   match_text = ''

   if game_name == 'kkong':
      file_path = './dict/kkong.txt'
   elif game_name == 'olla':
      file_path = './dict/olla.txt'
   else:
      file_path = './dict/ox.txt'

   with open(file_path, 'r') as file:
      lines = file.readlines()

   for item in lines:
      percentage = similar(keyword,item)
      if percentage > 0.43:
         match_text += item
         print(item,percentage )
         # print( str(item.split('(')[-1:][0]).split(')')[0] )

   return match_text

def quiz_game_start(model, game_name):
   #   print(game_name)
  image = Image.open('./a.png')
  cropped_img = crop_img(image, game_name)
  question = run_ocr(cropped_img, game_name)

  print(f"Game Name : {game_name}")
  print(f"Q : {question}")

  answer = ''
  
#   question = '문제 1623년 서인 일파가 광해군 및 대북파를 몰아내고 능양군(인조)을 왕으로 옹립한 사건은?(4글자)'
#   question = '관을 활용해서 2차 대전 중인 1946년 에커트와 모클리에 의해 최초로 개'
#   question = '둘 이상의 프로세서가 연결되어 CPU가 같은 제어프로그램하에서 둘 이상의 동시작업을'

  answer = dict_search(question, game_name)

  if answer is None or answer == '':
     print('AI RUN')
     answer, markdownTxt  = model.run_model(question, cropped_img)
     if type(answer) == 'str':
        answer = answer
     else:
        answer = markdownTxt

  print(f"A : {answer}")
   #   cropped_img.show()

if __name__ == '__main__':
  survival_title  = 'MapleStory Worlds-QPlay Archive(서바이벌)'
  arcade_title  = 'MapleStory Worlds-QPlay Archive(아케이드&보드&퀴즈)'
  window_title  = 'MapleStory Worlds-QPlay Archive'
  window = None
  model = model(env=None)

#   for win in pyautogui.getAllWindows():
  for win in pyautogui.getWindowsWithTitle(window_title):
  # pyautogui.getWindowsWithTitle('MapleStory Worlds')
     if win.title == survival_title or win.title == arcade_title:
        window = win
        # print(win)
#   print(window.title)
  window.resizeTo(1566, 1211)

  try:
   window.activate()
  except:
     print('')

  window_x, window_y, window_width, window_height = window.left, window.top, window.width, window.height

  # 화면 캡쳐
  screenshot = pyautogui.screenshot(region=(window_x, window_y, window_width, window_height))
  screenshot.save(f"./a.png")

#   screenshot = Image.open('./a.png')

  #게임 이름 찾기
  game_name = get_game_name(screenshot)

  if game_name == 'hamburger':
     print('')
  else:
     quiz_game_start(model, game_name)
