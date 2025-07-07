# preprocessing.py

import cv2


def preprocess_image(image_path):
    """
    전처리: 흑백 변환 + 이진화 (Thresholding)
    반환: 전처리된 numpy 이미지 배열
    """
    image = cv2.imread(image_path)

    # 그레이스케일 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 이진화 (Thresholding)
    _, threshed = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY)

    return threshed
