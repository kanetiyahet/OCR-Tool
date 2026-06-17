from flask import Flask, render_template, request
import easyocr
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

reader = easyocr.Reader(['en'])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ocr", methods=["POST"])
def ocr():
    file = request.files["image"]

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    result = reader.readtext(path)

    text = "\n".join([r[1] for r in result])

    return render_template(
        "result.html",
        text=text
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)