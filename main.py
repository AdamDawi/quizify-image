import os
import time
from config import system_prompt_image_to_json
from config import system_prompt_text_to_json
from processing.formatter import process_image_to_json, process_text_to_json

def process_folder_images(folder_path, output_file, log_file):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            process_image_to_json(os.path.join(folder_path, filename), output_file, system_prompt_image_to_json, log_file)

def process_folder_texts(folder_path, output_file, log_file):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.txt'):
            process_text_to_json(os.path.join(folder_path, filename), output_file, system_prompt_text_to_json, log_file)

if __name__ == "__main__":
    start_time = time.time()

    # --- CONFIGURATION ---
    MODE = "text"  # Change to "text" for .txt processing or "image" for .jpg/.png processing
    # image_path = "data/test_images/i2.jpg"
    # text_path = "data/texts/t3.txt"
    images_folder = "data/images"
    texts_folder = "data/texts"
    output_file = "output/formatted_questions.json"
    log_file = "output/deep_think_logs.txt"
    # ---------------------

    if MODE == "image":
        # Single image
        # process_image_to_json(image_path, output_file, system_prompt, log_file)
        process_folder_images(images_folder, output_file, log_file)
    elif MODE == "text":
        # Single text file
        # process_text_to_json(text_path, output_file, system_prompt_text_to_json, log_file)
        process_folder_texts(texts_folder, output_file, log_file)
    else:
        print("Invalid MODE selected. Use 'image' or 'text'.")

    end_time = time.time()
    total_time = end_time - start_time
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)
    print(f"Program execution time: {minutes} minute(s) {seconds} second(s)")