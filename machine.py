import os
from process_image_to_json import process_image_to_json

def process_images_in_folder(folder_path, output_file="formatted_questions.json"):
    if not os.path.isdir(folder_path):
        print(f"Folder {folder_path} does not exist!")
        return
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Image processing: {filename}")
            process_image_to_json(file_path, output_file)
        else:
            print(f"File skipped (not image): {filename}")


process_images_in_folder("images_folder")