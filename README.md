# Quizify Image
Quizify Image is a Python desktop application that transforms images or text files containing quiz questions into a clean, structured JSON format — ready to be used in quiz applications. The app uses OCR to extract text from images, sends the extracted or raw text to an LLM (via Ollama), and formats the response into a quiz-ready structure. It also includes a graphical user interface built with PyQt5.

## ⭐️Features
- **🧾 Text & Image Support:** Convert both text files (`.txt`) and image files (`.jpg`, `.png`, `.jpeg`) into structured quiz data.
  
- **👁️ OCR with EasyOCR:** Extracts text from quiz screenshots or scanned documents.

- **🤖 AI-Powered Parsing:** Uses the `deepseek-coder:14b` model through Ollama to convert plain text into JSON-format quiz questions.

- **🧪 Quiz Formatter:** Outputs are formatted as valid JSON and saved to a specified file.

- **📂 Batch Processing:** Processes all files in the selected directory (either images or text).

- **🕒 Time Tracking:** Calculates how long the processing takes for each file and the entire run.

- **📝 Logging:** Saves logs to a file for debugging or tracking purposes.

- **💻 GUI Interface:** Built using PyQt5 to make the tool user-friendly and accessible.

- **🧹 Prefix Cleaner:** Optionally removes unwanted prefixes like "a)", "1.", etc. from answers in the generated JSON file.

## ⚙️Technologies
**🐍 Python** - Core language used for building the entire application.

**🧠 LLM (Large Language Model)**
  - [Ollama](https://ollama.com/) – A local framework to run large language models.
  - Model used: `deepseek-coder:14b` – Interprets raw quiz text and converts it into a structured JSON format.

**👁️ Optical Character Recognition (OCR)**
  - [EasyOCR](https://github.com/JaidedAI/EasyOCR) – Extracts text from images and screenshots containing quiz questions.

**🧮 Data Processing & Utilities**
  - `json`, `os`, `re`, `time`, `sys` – Built-in Python modules for handling files, text parsing, timing, and JSON formatting.

**💻 GUI Framework**
  - [PyQt5](https://pypi.org/project/PyQt5/) – Used to create the graphical user interface for ease of use.

## Here are some overview pictures:
<img width="400" height="300" alt="Image" src="https://github.com/user-attachments/assets/1e11e7ef-3d00-44a2-8e55-b30e9e1739d4" />
<img width="400" height="300" alt="Image" src="https://github.com/user-attachments/assets/51bebfc3-1002-4477-8335-35db4f64736e" />

## Installation
1. Clone the repository:
```bash
git clone https://github.com/AdamDawi/quizify-image
cd quizify-image
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Make sure you have Python 3.7 or higher installed.
You can check this by running:
```bash
python --version
```
6. Install and set up Ollama:
- Download and install Ollama from [ollama.com](https://ollama.com/).
- Once installed and running, pull the required LLM model:
```bash
ollama pull deepseek-coder:14b
```
5. Run the app:
```bash
python main.py
```

>📌 The app allows you to upload quiz screenshots and automatically converts them into structured JSON format using AI.

## Author

Adam Dawidziuk🧑‍💻
