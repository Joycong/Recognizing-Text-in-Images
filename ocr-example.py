from PIL import Image, ImageDraw, ImageFont
import pytesseract
from preprocessing import preprocess_image  # 전처리 함수 불러오기
from pytesseract import Output
import cv2

# 📂 OCR 대상 이미지 경로
image_path = "docs/test_picture.jpg"
text_output_path = "output.txt"
output_image_path = "output.png"

# 원본 이미지를 RGB로 열기
image = Image.open(image_path)

### 전처리 이미지로 열기
# # 🧪 전처리 (흑백 이진화) : numpy 배열 반환됨
# preprocessed_ndarray = preprocess_image(image_path)

# # ✨ numpy → PIL 이미지로 변환 + RGB모드 적용
# image = Image.fromarray(preprocessed_ndarray)
# image = image.convert("RGB")
###

# 🧠 OCR 수행 (박스 정보 포함)
custom_config = r"--oem 3 --psm 3 -l eng+kor"
ocr_result = pytesseract.image_to_data(
    image, config=custom_config, output_type=Output.DICT
)

# 🖋️ 시각화 준비
draw = ImageDraw.Draw(image)
font_path = "C:/WINDOWS/FONTS/MALGUNSL.TTF"  # 한글 지원 폰트
font = ImageFont.truetype(font_path, 18)

# 📋 텍스트 추출 결과 저장용
recognized_text = ""

# 🔁 OCR 결과 반복 처리
n_boxes = len(ocr_result["text"])
for i in range(n_boxes):
    text = ocr_result["text"][i].strip()
    conf = ocr_result["conf"][i]

    if text and str(conf).isdigit() and int(conf) >= 0:
        confidence = int(conf) / 100  # 정수 → 소수 (예: 98 → 0.98)

        x, y, w, h = (
            ocr_result["left"][i],
            ocr_result["top"][i],
            ocr_result["width"][i],
            ocr_result["height"][i],
        )

        # ✅ 텍스트 출력 및 박스 그리기
        draw.rectangle([(x, y), (x + w, y + h)], outline="green", width=2)
        draw.text((x, y - 20), text, font=font, fill="green")

        # ✅ 정확도 포함하여 텍스트 저장
        recognized_text += f"[{confidence:.2f}] {text}\n"


# 💾 결과 저장
image.save(output_image_path)
with open(text_output_path, "w", encoding="utf-8") as f:
    f.write(recognized_text)

print(f"[✔] 박스 시각화된 이미지 저장: {output_image_path}")
print(f"[✔] 추출된 텍스트 저장 완료: {text_output_path}")

# 📊 평균 인식 정확도 계산
conf_values = []

for conf in ocr_result["conf"]:
    if isinstance(conf, str):
        if conf.strip().isdigit():
            conf_values.append(int(conf))
    elif isinstance(conf, int):
        if conf >= 0:
            conf_values.append(conf)

if conf_values:
    avg_conf = sum(conf_values) / len(conf_values)
    print(f"📊 평균 인식 정확도: {avg_conf:.2f}")
else:
    print("⚠️ 유효한 신뢰도(conf) 값이 없습니다.")
