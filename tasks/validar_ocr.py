import pytesseract
from PIL import Image
import cv2
import re
import numpy as np
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import datetime
import tempfile
import os
from flask import Flask, render_template, request, jsonify
import cv2
import pytesseract

app = Flask(__name__)

@app.route('/check_in', methods=['GET'])

def index():
    return render_template('check_in.html')

@app.route('/validar_ocr/', methods=['POST'])
def validar_ocr():
    if 'documento_adjunto' not in request.files:
        return jsonify({'valid': False, 'message': 'No se ha subido ningún documento'}), 400

    # Obtener la imagen subida
    image_file = request.files['documento_adjunto']
    image_bytes = image_file.read()
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Preprocesamiento (opcional)
    # ... (puedes aplicar técnicas de mejora de imagen)

    # Aplicar OCR
    text = pytesseract.image_to_string(img)

    # Extraer datos (ejemplo básico)
    data = {}
    lines = text.split('\n')
    for line in lines:
        key, value = line.split(':')  # Supone que los datos están en formato clave:valor
        data[key.strip()] = value.strip()

    # Validación de datos (opcional)
    # ... (puedes agregar lógica para validar la estructura o formato de los datos extraídos)

    return jsonify({'valid': True, 'data': data})

if __name__ == '__main__':
    app.run(debug=True)