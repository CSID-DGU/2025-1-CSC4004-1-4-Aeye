from PIL import Image
import cv2
import numpy as np
import io
from google.cloud import vision
from google.oauth2 import service_account
import re

credentials = service_account.Credentials.from_service_account_file('service-account-file.json')
vision_client = vision.ImageAnnotatorClient(credentials=credentials)

# API 호출
def call_google_ocr_api(img_np):
    img_pil = Image.fromarray(img_np)
    buffered = io.BytesIO()
    img_pil.save(buffered, format="PNG")
    img_content = buffered.getvalue()

    img = vision.Image(content=img_content)
    response = vision_client.text_detection(image=img)

    annotations = response.text_annotations
    if annotations:
        return annotations[0].description
    else:
        return ""
    
# 이미지 전처리(업스케일링)
def preprocess_img(img_stream, upscale_factor):
    img = Image.open(img_stream).convert('RGBA')
    img_np = np.array(img)
    height, width = img_np.shape[:2] 

    img_upscaled = cv2.resize(img_np, (width * upscale_factor, height * upscale_factor), interpolation=cv2.INTER_CUBIC)
    img_gray = cv2.cvtColor(img_upscaled, cv2.COLOR_BGR2GRAY)
    height, width = img_gray.shape

    slices = []
    if height > 1000 * upscale_factor:
        step = 500 * upscale_factor
        overlap = 500
        y = 0
        while y < height:
            y_end = min(y + step, height)
            slice_img = img_gray[y:y_end, :]
            slices.append(slice_img)
            if y_end == height:
                break
            y = y + (step - overlap)
    else:
        slices.append(img_gray)

    return slices

# 유효 텍스트 확인
def is_valid_line(line):
    line = line.strip()

    valid_ratio = len(re.findall(r'[A-Za-z0-9가-힣]', line)) / len(line)
    special_ratio = len(re.findall(r'[^A-Za-z0-9가-힣\s]', line)) / len(line)
    if re.search(r'[^A-Za-z0-9가-힣\s]{3,}', line):
        return False
    
    return valid_ratio >= 0.7 and special_ratio < 0.3

# OCR 및 텍스트 후처리
def img_to_text(img_stream, upscale_factor):
    preprocessed = preprocess_img(img_stream, upscale_factor)
    results = []
    prev_lines = set()

    for s in preprocessed:
        text = call_google_ocr_api(s)
        if text:
            lines = [line.strip() for line in text.splitlines() if line.strip() and is_valid_line(line)]
            current_lines = [line for line in lines if line not in prev_lines]
            
            results.extend(current_lines)
            prev_lines = set(current_lines)

    return " ".join(results) if results else ""

# 받아온 이미지 파일들을 넣어 실행
def run(img_files, upscale_factor = 3):
    result = []
    for img_file in img_files:
        try:
            text = img_to_text(img_file.stream, upscale_factor)
            result.append(text)
        except Exception as e:
            result.append(f"Error: {str(e)}")

    return " ".join(result)