import os
from config import system_prompt
from processing.formatter import process_image_to_json

def process_folder(folder_path, output_file, log_file):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            process_image_to_json(os.path.join(folder_path, filename), output_file, system_prompt, log_file)

if __name__ == "__main__":
    image_path = "data/test_images/i2.jpg"
    output_file = "output/formatted_questions.json"
    log_file = "output/deep_think_logs.txt"
    process_folder("data/images", output_file, log_file)
    
    # process_image_to_json(image_path, output_file, log_file)
