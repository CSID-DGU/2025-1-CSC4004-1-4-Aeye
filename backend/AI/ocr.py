from PIL import Image
import io
from google.cloud import vision
from google.oauth2 import service_account

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