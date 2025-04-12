# 파일 위치: pdfproject/app.py
from flask import Flask, render_template, request, send_file
import img2pdf
from werkzeug.utils import secure_filename
import os
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    image_files = request.files.getlist('jpgFiles')

    image_paths = []
    for file in image_files:
        if file and file.filename.lower().endswith(('.jpg', '.jpeg')):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_paths.append(filepath)

    # PDF로 변환
    pdf_bytes = BytesIO()
    with open(pdf_bytes.fileno(), 'wb') as f:  # file descriptor로 오류나므로 아래처럼 바꿈
        f.write(img2pdf.convert(image_paths))
    pdf_bytes.seek(0)

    # 임시 이미지 삭제
    for path in image_paths:
        os.remove(path)

    return send_file(
        pdf_bytes,
        as_attachment=True,
        download_name="converted.pdf",
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
