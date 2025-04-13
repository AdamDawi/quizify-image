import json
from datetime import datetime

def append_to_log(image_path, extracted_text, deep_think_response, log_file, result):
    with open(log_file, "a", encoding="utf-8") as log_file:
        log_file.write("\n" + "="*80 + "\n")
        log_file.write(f"🖼️ Image: {image_path}\n")
        log_file.write(f"🕒 Timestamp: {datetime.now().isoformat()}\n")
        
        log_file.write("\n📜 Extracted OCR text:\n")
        log_file.write(extracted_text.strip() + "\n")
        
        log_file.write("\n🧠 Deep Think response:\n")
        log_file.write(deep_think_response.strip() + "\n")
        
        if result:
            log_file.write("\n✅ Result:\n")
            log_file.write(result + "\n")

        log_file.write("="*80 + "\n")

def load_existing_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            return existing_data if isinstance(existing_data, list) else []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: {e}. Starting with an empty list.")
        return []

def save_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
