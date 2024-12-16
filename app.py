from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
import pdfplumber
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Document Parser API!"})

@app.route('/parse', methods=['POST'])
def parse_document():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400

    if len(file.read()) > MAX_FILE_SIZE:
        return jsonify({"success": False, "message": "File size exceeds limit"}), 400

    file.seek(0)  # Reset file pointer after size check

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Process document (OCR for images or PDFs)
            parsed_data = []
            if filename.endswith('.pdf'):
                with pdfplumber.open(filepath) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text()
            else:
                img = Image.open(filepath)
                text = pytesseract.image_to_string(img)

            if not text:
                return jsonify({"success": False, "message": "No text extracted from the document"}), 400

            # Example data extraction logic
            invoice_number = text.split("\n")[0]  # Replace with actual logic
            total_amount = "100.00"  # Replace with actual logic
            parsed_data.append({
                'invoiceNumber': invoice_number,
                'date': "2024-12-15",  # Example date
                'totalAmount': total_amount
            })

            os.remove(filepath)  # Cleanup

            return jsonify({"success": True, "parsedData": parsed_data})

        except Exception as e:
            os.remove(filepath)  # Cleanup on error
            return jsonify({"success": False, "message": f"Error processing the file: {str(e)}"}), 500

    return jsonify({"success": False, "message": "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(debug=True)