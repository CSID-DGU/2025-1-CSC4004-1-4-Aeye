import requests
from io import BytesIO
from backend.AI import ocr

def extract_text_from_images(image_paths):
    """
    이미지 파일 경로 리스트를 받아 OCR 텍스트를 반환한다.
    """
    image_files = []

    for path in image_paths:
        try:
            response = requests.get(path, timeout=5)
            response.raise_for_status()
            image_files.append(BytesIO(response.content))
        except Exception as e:
            print('Error: ', e)

    return ocr.run(image_files)