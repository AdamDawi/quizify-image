import json
from llm.deepseek_client import ask_deepseek
from ocr.ocr_reader import extract_text_from_image
from utils.io_utils import append_to_log, load_existing_json, save_json
from config import system_prompt

def process_image_to_json(image_path, output_file, log_file="deep_think_logs.txt"):
    extracted_text = extract_text_from_image(image_path)
    clean_response, deep_think_response = ask_deepseek(
        input_content=extracted_text,
        system_prompt=system_prompt,
        deep_think=True,
        print_log=False
    )

    append_to_log(image_path, extracted_text, deep_think_response, log_file)

    clean_response = clean_response.replace('```json', '').replace('```', '').strip()
    try:
        parsed_json = json.loads(clean_response)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        parsed_json = [{"title": f"Failed to process: {image_path}"}]

    existing_data = load_existing_json(output_file)
    existing_data.extend(parsed_json)
    save_json(existing_data, output_file)
