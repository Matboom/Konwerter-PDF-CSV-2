from flask import render_template, request, jsonify, send_file
from app import app
from app.config import SECRET_KEY
from app.converters.Table_1 import convert_pdf_to_csv_1
import io

# Trasa dla głównej strony
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'message': 'No file part in the request', 'success': False}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'message': 'No selected file', 'success': False}), 400
        
        if file:
            try:
                # Tworzenie bufora na dane CSV
                base_filename = file.filename.rsplit('.', 1)[0]
                csv_buffer = io.StringIO()
                
                # Konwersja pliku PDF na CSV
                convert_pdf_to_csv_1(file, csv_buffer)
                
                # Przywracanie kursora na początek bufora
                csv_buffer.seek(0)
                
                # Wysłanie pliku CSV jako odpowiedź do pobrania
                return send_file(
                    io.BytesIO(csv_buffer.getvalue().encode('utf-8')),
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name=f'{base_filename}.csv' 
                )
            
            except Exception as e:
                return jsonify({'message': str(e), 'success': False}), 500
    
    # Jeśli metoda to GET, renderuj standardowy szablon HTML
    return render_template('Home.html', secret_key=SECRET_KEY)
