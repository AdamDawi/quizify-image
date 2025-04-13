import json
import time
from llm.deepseek_client import ask_deepseek
from ocr.ocr_reader import extract_text_from_image
from utils.io_utils import append_to_log, load_existing_json, save_json

def process_image_to_json(image_path, output_file, system_prompt, log_file):
    start_time = time.time()  # Start timer
    
    print(f"\nSTART: Extracting text from image: {image_path}")
    
    # Extract text from image
    extracted_text = extract_text_from_image(image_path)
    print("DONE: Extracting text from image")
    
    # Ask Deepseek to process the extracted text
    clean_response, deep_think_response = ask_deepseek(
        input_content=extracted_text,
        system_prompt=system_prompt,
        deep_think=True,
        print_log=False
    )
    print("DONE: Cleaning and formatting Deepseek response")

    # Append to log
    append_to_log(image_path, extracted_text, deep_think_response, log_file, result=clean_response)

    # Clean and parse the response
    clean_response = clean_response.replace('```json', '').replace('```', '').strip()
    try:
        parsed_json = json.loads(clean_response)
        print("JSON parsed successfully.")
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        parsed_json = [{"title": f"Failed to process: {image_path}"}]

    # Load existing data, extend it, and save it
    existing_data = load_existing_json(output_file)
    existing_data.extend(parsed_json)
    save_json(existing_data, output_file)

    # End timer and calculate the total time taken
    end_time = time.time()  # End timer
    elapsed_time = end_time - start_time  # Calculate elapsed time

    # Calculate minutes and seconds
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    print(f"Processing complete for image: {image_path}")
    print(f"Total processing time: {minutes} minute(s) {seconds} second(s)")
