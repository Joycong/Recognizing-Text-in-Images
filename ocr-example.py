import pytesseract as tess
from PIL import Image

img = Image.open("docs/ocr-example-eng.png")  # 이미지 오픈
text_eng = tess.image_to_string(img)  # 텍스트 추출

img = Image.open("docs/ocr-example-jpn.png")
text_jpn = tess.image_to_string(img, lang="jpn")  # 일본어 OCR

img = Image.open("docs/ocr-example-eng+kor.png")
text_eng_kor = tess.image_to_string(img, lang="eng+kor")  # 다국어 혼합 인식

print("🔍 인식 결과:")
print(f"{text_eng}\n{text_jpn}\n{text_eng_kor}")
