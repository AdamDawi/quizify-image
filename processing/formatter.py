import json
import time
from llm.deepseek_client import ask_deepseek
from ocr.ocr_reader import extract_text_from_image
from utils.io_utils import append_to_log, load_existing_json, save_json

def format_elapsed(elapsed):
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    return f"{minutes}m {seconds}s"

def process_image_to_json(image_path, output_file, system_prompt, log_file, progress=None):
    start_time = time.time()
    if progress: progress.emit(f"START: Extracting text from image: {image_path}")

    extracted_text = extract_text_from_image(image_path)
    if progress: progress.emit("DONE: Extracting text from image")

    if progress: progress.emit("START: AI Formatting text to quiz JSON...")
    clean_response, deep_think_response = ask_deepseek(
        input_content=extracted_text,
        system_prompt=system_prompt,
        deep_think=True,
        print_log=False
    )
    if progress: progress.emit("DONE: AI Formatting text to quiz JSON...")

    append_to_log(image_path, extracted_text, deep_think_response, log_file, result=clean_response)

    clean_response = clean_response.replace('```json', '').replace('```', '').strip()
    try:
        parsed_json = json.loads(clean_response)
        if progress: progress.emit("SUCCESS: Parsed JSON")
        status = "Success"
    except json.JSONDecodeError as e:
        if progress: progress.emit(f"FAILED: JSON parse error: {e}")
        parsed_json = [{"title": f"Failed to process: {image_path}"}]
        status = "Failed"

    existing_data = load_existing_json(output_file)
    existing_data.extend(parsed_json)
    save_json(existing_data, output_file)

    elapsed_time = time.time() - start_time
    if progress: progress.emit(f"File processed in {format_elapsed(elapsed_time)}.")
    return status, elapsed_time

def process_text_to_json(text_path, output_file, system_prompt, log_file, progress=None):
    start_time = time.time()
    if progress: progress.emit(f"START: Reading text file: {text_path}")

    with open(text_path, 'r', encoding='utf-8') as f:
        input_text = f.read()
    if progress: progress.emit("DONE: Reading text file")

    if progress: progress.emit("START: AI Formatting text to quiz JSON...")
    clean_response, deep_think_response = ask_deepseek(
        input_content=input_text,
        system_prompt=system_prompt,
        deep_think=True,
        print_log=False
    )
    if progress: progress.emit("DONE: AI Formatting text to quiz JSON...")

    append_to_log(text_path, input_text, deep_think_response, log_file, result=clean_response)

    clean_response = clean_response.replace('```json', '').replace('```', '').strip()
    try:
        parsed_json = json.loads(clean_response)
        if progress: progress.emit("SUCCESS: Parsed JSON")
        status = "Success"
    except json.JSONDecodeError as e:
        if progress: progress.emit(f"FAILED: JSON parse error: {e}")
        parsed_json = [{"title": f"Failed to process: {text_path}"}]
        status = "Failed"

    existing_data = load_existing_json(output_file)
    existing_data.extend(parsed_json)
    save_json(existing_data, output_file)

    elapsed_time = time.time() - start_time
    if progress: progress.emit(f"File processed in {format_elapsed(elapsed_time)}.")
    return status, elapsed_time
