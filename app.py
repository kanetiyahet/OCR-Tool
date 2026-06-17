from flask import Flask, render_template, request, jsonify, send_file
import easyocr
import os
import json
import io
import uuid
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize EasyOCR reader (supports English; add more languages as needed)
reader = easyocr.Reader(['en'])

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_ocr(filepath):
    result = reader.readtext(filepath)
    text = "\n".join([r[1] for r in result])
    word_count = len(text.split()) if text.strip() else 0
    char_count = len(text)
    return text, word_count, char_count

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ocr", methods=["POST"])
def ocr():
    """Handle single or multiple image uploads."""
    files = request.files.getlist("images")
    if not files or all(f.filename == '' for f in files):
        return jsonify({"error": "No files uploaded"}), 400

    results = []
    for file in files:
        if file and allowed_file(file.filename):
            # Save with unique name to avoid collisions
            ext = file.filename.rsplit('.', 1)[1].lower()
            unique_name = f"{uuid.uuid4().hex}.{ext}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_name)
            file.save(filepath)

            text, word_count, char_count = run_ocr(filepath)

            results.append({
                "filename": file.filename,
                "text": text,
                "word_count": word_count,
                "char_count": char_count,
            })
        else:
            results.append({
                "filename": file.filename,
                "error": "Unsupported file type",
                "text": "",
                "word_count": 0,
                "char_count": 0,
            })

    return jsonify({"results": results})

@app.route("/download/txt", methods=["POST"])
def download_txt():
    data = request.get_json()
    text = data.get("text", "")
    buf = io.BytesIO(text.encode("utf-8"))
    buf.seek(0)
    return send_file(buf, mimetype="text/plain",
                     as_attachment=True, download_name="ocr_result.txt")

@app.route("/download/json", methods=["POST"])
def download_json():
    data = request.get_json()
    results = data.get("results", [])
    payload = {
        "exported_at": datetime.utcnow().isoformat() + "Z",
        "results": results
    }
    buf = io.BytesIO(json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8"))
    buf.seek(0)
    return send_file(buf, mimetype="application/json",
                     as_attachment=True, download_name="ocr_result.json")

@app.route("/download/pdf", methods=["POST"])
def download_pdf():
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.lib import colors
    except ImportError:
        return jsonify({"error": "reportlab not installed. Run: pip install reportlab"}), 500

    data = request.get_json()
    results = data.get("results", [])

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'],
                                  textColor=colors.HexColor('#1a73e8'))
    meta_style = ParagraphStyle('Meta', parent=styles['Normal'],
                                 textColor=colors.grey, fontSize=9)
    body_style = ParagraphStyle('Body', parent=styles['Normal'],
                                 leading=16, fontSize=11)

    story = []
    story.append(Paragraph("OCR Results", title_style))
    story.append(Spacer(1, 6*mm))

    for i, r in enumerate(results, 1):
        story.append(Paragraph(f"Image {i}: {r.get('filename','')}", styles['Heading2']))
        story.append(Paragraph(
            f"Words: {r.get('word_count',0)}  |  Characters: {r.get('char_count',0)}",
            meta_style))
        story.append(Spacer(1, 3*mm))
        text = r.get("text", "").replace("\n", "<br/>")
        story.append(Paragraph(text or "<i>(no text detected)</i>", body_style))
        story.append(Spacer(1, 8*mm))

    doc.build(story)
    buf.seek(0)
    return send_file(buf, mimetype="application/pdf",
                     as_attachment=True, download_name="ocr_result.pdf")

@app.route("/download/docx", methods=["POST"])
def download_docx():
    try:
        from docx import Document
        from docx.shared import Pt, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
    except ImportError:
        return jsonify({"error": "python-docx not installed. Run: pip install python-docx"}), 500

    data = request.get_json()
    results = data.get("results", [])

    document = Document()

    # Title
    title = document.add_heading("OCR Results", 0)
    title.runs[0].font.color.rgb = RGBColor(0x1a, 0x73, 0xe8)

    for i, r in enumerate(results, 1):
        document.add_heading(f"Image {i}: {r.get('filename','')}", level=2)
        meta = document.add_paragraph(
            f"Words: {r.get('word_count',0)}   |   Characters: {r.get('char_count',0)}"
        )
        meta.runs[0].font.size = Pt(9)
        meta.runs[0].font.color.rgb = RGBColor(0x80, 0x80, 0x80)

        text = r.get("text", "") or "(no text detected)"
        p = document.add_paragraph(text)
        p.runs[0].font.size = Pt(11)
        document.add_paragraph()  # spacing

    buf = io.BytesIO()
    document.save(buf)
    buf.seek(0)
    return send_file(buf,
                     mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                     as_attachment=True, download_name="ocr_result.docx")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)