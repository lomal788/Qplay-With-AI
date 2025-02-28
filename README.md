## QPlay Archive Survival Quiz With AI

### 메이플 월드 QPlay 서바이벌 퀴즈 With 잼민이

### Spec

- Lang : Python 3.13.2
- AI : gemini-2.0-flash-lite
- OCR : pytesseract
- OpenCv

### requirements

- Gemini API KEY ( Check .env )
- pytesseract (install)

### 설명

- 게임화면 캡쳐
- 무슨 퀴즈 게임인지 자동 판별 (꽁, 올라만 가능)
- 캡쳐된 화면에서 원하는 퀴즈 부분만 자른뒤 흑백 전환 및 대비 조정
- OCR로 문자 추출
- 가지고 있는 족보에서 검색된 내용이 있을경우 해당 내용 표시
- 족보에서 검색 불가시 제미나이에게 추출된 문자,캡쳐 이미지 화면 전송
- 추출 문자 및결과 정답 표시

![img0.png](https://raw.githubusercontent.com/lomal788/Qplay-With-AI/master/img/img0.png)
![img1.png](https://raw.githubusercontent.com/lomal788/Qplay-With-AI/master/img/img1.png)

```
python index.py
Q : 문제
1623년 서인 일파가 광해군 및 대북파를 몰아내고 능양군(인조)을
왕으로 옹립한 사건은?(4글자)

A : 인조반정
```

## Warning - 어뷰징 하려고 만든게 아니라 그냥 재미로 만들었습니다. I make this Just for fun not to abuse the game
