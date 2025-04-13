import json
import ollama
from ask_deepseek import ask_deepseek

def process_image_to_json(image_path, output_file="formatted_questions.json"):
    # === MODEL 1: OCR ===
    print(f"Loading image from {image_path}...")
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()

    print("Extracting text from image using MiniCPM...")
    ollama_response = ollama.chat(
    model="minicpm-v:8b-2.6-fp16",
    messages=[
        {
            "role": "user",
            "content": (
                "Please extract **all visible text** from the attached image. "
                "This is a scanned exam or quiz page in **Polish**, often with some **English technical terms**. "
                "The text contains **multiple-choice questions**, typically with answers labeled like: a), b), c) or using dashes. "
                "\n\n"
                "Your task:\n"
                "- Extract the text **exactly as shown** (don't paraphrase).\n"
                "- Preserve **line breaks**, spacing, and structure to reflect the layout of questions and answers.\n"
                "- Do **not** skip anything, even if the text seems unclear or partially cropped.\n"
                "- **Do not format** the output as JSON or Markdown — just return raw extracted text.\n\n"
                "The output will be processed later by another model, so formatting is important.\n\n"
                "If you're not sure about a word or symbol, try your best to keep its shape as it appears visually."
            ),
            "images": [image_bytes]
        }
    ]
)

    extracted_text = ollama_response["message"]["content"]
    print("Extracted text:")
    print(extracted_text)

    # === MODEL 2: Deepseek cleaning and formatting ===
    json_template = '''
    [
      {
        "question": "{question}",
        "answers": [
          { "text": "{answer1}", "correct": {is_correct1} },
          { "text": "{answer2}", "correct": {is_correct2} },
          { "text": "{answer3}", "correct": {is_correct3} },
          { "text": "{answer4}", "correct": {is_correct4} }
        ]
      }
    ]
    '''

    system_prompt = f'''
        You are a professional assistant that transforms messy, OCR-scanned Polish quiz content into clean, structured multiple-choice question JSON.

        ## Your objective
        Transform the input text (containing multiple quiz questions and answers in Polish) into a valid JSON array using the format below:

        {json_template}

        ## Rules (Follow exactly!)
        1. **Each object must include**:
        - `question`: string
        - `answers`: array of 2 or more objects, each with:
            - `text`: string
            - `correct`: boolean (always false)

        2. **Do NOT** generate:
        - Any question with fewer than 2 answers.
        - Any question with 0 answers.
        - Any object using keys like `options`, `correct_answer`, etc. — only use `question` and `answers` with `text` and `correct`.

        3. The final response must be:
        - A JSON **array** of objects as shown above.
        - **No Markdown code blocks** (no triple backticks).
        - Strictly conform to the JSON format or parsing will fail.

        ## Additional guidelines
        - Correct OCR errors in both questions and answers.
        - Fix spelling, grammar, and phrasing — make it fluent and natural in Polish.
        - Don’t skip any questions that follow the rules above.
        - Include all answer options if there are more than four.
        - If a question seems incomplete, ignore it.
        - If input includes scores, numbers, or metadata (like `Punktowy: 0,00 z 1,00`), ignore them.
    '''

    print("Sending to Deepseek for cleaning and formatting...")
    clean_response, deep_think_response = ask_deepseek(
        input_content=extracted_text,
        system_prompt=system_prompt,
        deep_think=True,
        print_log=False
    )

    print("\n✅ Final JSON response from Deepseek:")
    print(clean_response)

    # print("\n🧠 Deep Think (inference or reasoning, if any):")
    # print(deep_think_response)

    # === Save Deep Think log to a file ===
    log_file_path = "deep_think_logs.txt"
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write("\n" + "="*80 + "\n")
        log_file.write(f"🖼️ Image: {image_path}\n")
        log_file.write(f"🕒 Timestamp: {__import__('datetime').datetime.now().isoformat()}\n")

        log_file.write("\n📜 Extracted OCR text:\n")
        log_file.write(extracted_text.strip() + "\n")

        log_file.write("\n🧠 Deep Think response:\n")
        log_file.write(deep_think_response.strip() + "\n")
        log_file.write("="*80 + "\n")

    print(f"\n📝 Deep Think log saved in: {log_file_path}")

    # === Clean the response from Deepseek by removing code block markers ===
    clean_response = clean_response.strip()
    clean_response = clean_response.replace('```json', '').replace('```', '').strip()

    # === Parse the clean response as JSON or create fallback if invalid ===
    try:
        parsed_json = json.loads(clean_response)
    except json.JSONDecodeError as e:
        print(f"\n❌ Failed to parse JSON from Deepseek response: {e}")
        parsed_json = [{
            "title": f"Failed to process: {image_path}"
        }]

    # === Load existing data if present ===
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            if isinstance(existing_data, list):
                existing_data.extend(parsed_json)
            else:
                existing_data = parsed_json
    except FileNotFoundError:
        existing_data = parsed_json

    # === Save the combined JSON ===
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

    print(f"\n📁 JSON saved in {output_file}")
