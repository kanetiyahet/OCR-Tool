# OCR-Tool

A Flask-based OCR Tool that works on both Laptop and Mobile.

## Features

- EasyOCR (Offline OCR)
- Sarvam AI OCR
- Gemini Vision OCR
- OpenAI Vision OCR
- Multiple Image Upload
- Drag & Drop Upload
- Paste Image (Ctrl + V)
- Mobile Camera Capture
- TXT Export
- DOCX Export
- PDF Export
- JSON Export
- Word Count & Character Count
- Multi-language Support

## Supported Languages

- English
- Hindi
- Gujarati
- Marathi
- Bengali
- Tamil
- Telugu
- Kannada
- Malayalam
- Punjabi
- Urdu
- Chinese
- Japanese
- Korean
- Arabic
- French
- German
- Spanish

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/kanetiyahet/OCR-Tool.git
cd OCR-Tool
```

### 2. Create Virtual Environment

```bash
py -m venv venv
```

### 3. Activate Virtual Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### 4. Install Requirements

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Or:

```bash
pip install flask easyocr python-docx reportlab python-dotenv google-generativeai openai sarvamai
```

## API Keys

Create a file named `.env`

```env
SARVAM_API_KEY=your_sarvam_key
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
```

## Run Application

```bash
python app.py
```

Server will start:

```text
http://127.0.0.1:5000
```

## Mobile Access

Find your laptop IP:

```bash
ipconfig
```

Open on mobile:

```text
http://YOUR_IP:5000
```

Example:

```text
http://192.168.1.43:5000
```

Both devices must be connected to the same Wi-Fi network.

## Project Structure

```text
OCR-Tool/
│
├── app.py
├── .env
├── requirements.txt
├── uploads/
│
├── templates/
│   └── index.html
│
└── README.md
```

## Technologies Used

- Python
- Flask
- EasyOCR
- Sarvam AI
- Gemini AI
- OpenAI
- HTML
- CSS
- JavaScript

## Update Project Later

```bash
git pull origin main
```

## Author

Kanetiya Het D.
CSE (AI & ML)