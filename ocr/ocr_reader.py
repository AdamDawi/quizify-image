import easyocr

def extract_text_from_image(image_path: str) -> str:
    reader = easyocr.Reader(['pl', 'en'])
    result = reader.readtext(image_path, detail=0, paragraph=True)
    return "\n".join(result)