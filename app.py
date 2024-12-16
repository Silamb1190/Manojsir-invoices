from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image
import pdfplumber
import json

app = Flask(__name__)

# Configure file upload folder
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/parse', methods=['POST'])
def parse_document():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process document (OCR for images or PDFs)
        parsed_data = []

        if filename.endswith('.pdf'):
            with pdfplumber.open(filepath) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
        else:
            # OCR for image-based files
            img = Image.open(filepath)
            text = pytesseract.image_to_string(img)
        
        # Example logic to extract data (modify with actual logic)
        invoice_number = text.split("\n")[0]  # Extract the first line as invoice number
        total_amount = "100.00"  # Replace with actual logic

        parsed_data.append({
            'invoiceNumber': invoice_number,
            'date': "2024-12-15",  # Example date
            'totalAmount': total_amount
        })

        return jsonify({"success": True, "parsedData": parsed_data})

    return jsonify({"success": False, "message": "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
