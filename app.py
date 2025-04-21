from flask import Flask, request, send_file, render_template_string
from pdf2docx import Converter
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PDF to Word Converter</title>
</head>
<body>
    <h2>Upload PDF to Convert to Word</h2>
    <form method="POST" action="/convert" enctype="multipart/form-data">
        <input type="file" name="pdf_file" accept="application/pdf" required>
        <button type="submit">Convert</button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    file = request.files['pdf_file']
    if file and file.filename.endswith('.pdf'):
        filename = str(uuid.uuid4()) + '.pdf'
        pdf_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(pdf_path)

        docx_filename = filename.replace('.pdf', '.docx')
        docx_path = os.path.join(CONVERTED_FOLDER, docx_filename)

        # Convert PDF to DOCX
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()

        return send_file(docx_path, as_attachment=True)
    return "Invalid file format. Please upload a PDF file."

if __name__ == '__main__':
    app.run(debug=True)
