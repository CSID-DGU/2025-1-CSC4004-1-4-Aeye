import os
from backend.AI import ocr

def extract_text_from_images(image_paths):
    """
    이미지 파일 경로 리스트를 받아 OCR 텍스트를 반환한다.
    """
    img_streams = []

    for path in image_paths:
        if not os.path.exists(path):
            continue
        with open(path, "rb") as f:
            img_streams.append(f)

    if not img_streams:
        return ""

    return ocr.run(img_streams)