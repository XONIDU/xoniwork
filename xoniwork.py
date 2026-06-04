#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONIWORK 2026 - Servidor de Simulacion de Escritura Automatica
Emula trabajo de escritura con errores controlados
"""

from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import os
import re
import time
import random
import threading
from werkzeug.utils import secure_filename
import pyautogui
import json

# Procesamiento de archivos
try:
    from PyPDF2 import PdfReader
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

try:
    from docx import Document
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False

try:
    from unidecode import unidecode
    UNIDECODE_SUPPORT = True
except ImportError:
    UNIDECODE_SUPPORT = False
    def unidecode(text):
        return text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configuracion por defecto
config = {
    'velocidad': 0.05,
    'error_nivel': 0,
    'espera_inicial': 3,
    'texto_actual': ''
}

ERROR_PORCENTAJES = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}

# Letras para errores de teclado (adyacentes en teclado QWERTY)
TECLADO_ADYACENTES = {
    'q': ['w', 'a', 's'],
    'w': ['q', 'e', 'a', 's', 'd'],
    'e': ['w', 'r', 's', 'd', 'f'],
    'r': ['e', 't', 'd', 'f', 'g'],
    't': ['r', 'y', 'f', 'g', 'h'],
    'y': ['t', 'u', 'g', 'h', 'j'],
    'u': ['y', 'i', 'h', 'j', 'k'],
    'i': ['u', 'o', 'j', 'k', 'l'],
    'o': ['i', 'p', 'k', 'l'],
    'p': ['o', 'l'],
    'a': ['q', 'w', 's', 'z'],
    's': ['w', 'e', 'a', 'd', 'z', 'x'],
    'd': ['e', 'r', 's', 'f', 'x', 'c'],
    'f': ['r', 't', 'd', 'g', 'c', 'v'],
    'g': ['t', 'y', 'f', 'h', 'v', 'b'],
    'h': ['y', 'u', 'g', 'j', 'b', 'n'],
    'j': ['u', 'i', 'h', 'k', 'n', 'm'],
    'k': ['i', 'o', 'j', 'l', 'm'],
    'l': ['o', 'p', 'k'],
    'z': ['a', 's', 'x'],
    'x': ['s', 'd', 'z', 'c'],
    'c': ['d', 'f', 'x', 'v'],
    'v': ['f', 'g', 'c', 'b'],
    'b': ['g', 'h', 'v', 'n'],
    'n': ['h', 'j', 'b', 'm'],
    'm': ['j', 'k', 'n']
}

def extraer_texto_archivo(filepath):
    """Extrae texto de TXT, PDF o DOCX"""
    extension = os.path.splitext(filepath)[1].lower()
    texto = ""
    
    if extension == '.txt':
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            texto = f.read()
    
    elif extension == '.pdf' and PDF_SUPPORT:
        try:
            reader = PdfReader(filepath)
            for page in reader.pages:
                texto += page.extract_text()
        except Exception as e:
            print(f"Error leyendo PDF: {e}")
    
    elif extension in ['.docx', '.doc'] and DOCX_SUPPORT:
        try:
            doc = Document(filepath)
            for para in doc.paragraphs:
                texto += para.text + '\n'
        except Exception as e:
            print(f"Error leyendo DOCX: {e}")
    
    else:
        raise Exception(f"Formato no soportado: {extension}")
    
    # Limpiar y normalizar texto
    texto = unidecode(texto)
    texto = re.sub(r'\s+', ' ', texto)
    texto = texto.strip()
    
    return texto

def generar_error_ortografico(letra, nivel):
    """Genera un error ortografico basado en el nivel"""
    if nivel == 0:
        return letra
    
    porcentaje = ERROR_PORCENTAJES[nivel]
    if random.randint(1, 100) > porcentaje:
        return letra
    
    letra_lower = letra.lower()
    if letra_lower in TECLADO_ADYACENTES and random.random() < 0.7:
        error = random.choice(TECLADO_ADYACENTES[letra_lower])
        return error if letra.islower() else error.upper()
    
    # Fallback: caracter aleatorio cercano
    if letra_lower.isalpha():
        offset = random.choice([-1, 1])
        codigo = ord(letra_lower) + offset
        if ord('a') <= codigo <= ord('z'):
            if random.random() < 0.5:
                error = chr(codigo)
                return error if letra.islower() else error.upper()
    
    return letra

def aplicar_errores(texto, nivel):
    """Aplica errores ortograficos al texto"""
    if nivel == 0:
        return texto
    
    resultado = []
    for char in texto:
        if char.isalpha():
            resultado.append(generar_error_ortografico(char, nivel))
        else:
            resultado.append(char)
    
    return ''.join(resultado)

def escribir_caracteres(texto, delay, detener_evento):
    """Escribe caracteres uno por uno con pyautogui"""
    for i, char in enumerate(texto):
        if detener_evento.is_set():
            return False, i
        try:
            pyautogui.write(char)
            time.sleep(delay)
        except Exception as e:
            return False, i
    return True, len(texto)

# ============================================================================
# Rutas Flask
# ============================================================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Empty filename'})
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        texto = extraer_texto_archivo(filepath)
        
        if not texto:
            return jsonify({'success': False, 'error': 'No se pudo extraer texto del archivo'})
        
        return jsonify({
            'success': True,
            'texto': texto,
            'longitud': len(texto),
            'filename': filename
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/configurar', methods=['POST'])
def configurar():
    data = request.json
    config['velocidad'] = data.get('velocidad', 0.05)
    config['error_nivel'] = data.get('error_nivel', 0)
    config['espera_inicial'] = data.get('espera_inicial', 3)
    
    print(f"\nConfiguracion actualizada:")
    print(f"  Velocidad: {config['velocidad']}s por caracter")
    print(f"  Nivel error: {config['error_nivel']} ({ERROR_PORCENTAJES[config['error_nivel']]}%)")
    print(f"  Espera inicial: {config['espera_inicial']}s")
    
    return jsonify({'success': True})

detener_evento = threading.Event()

@app.route('/iniciar_escritura')
def iniciar_escritura():
    def generate():
        global detener_evento
        detener_evento = threading.Event()
        
        texto = request.args.get('texto', '')
        if not texto:
            yield f"data: {json.dumps({'type': 'error', 'message': 'Texto vacio'})}\n\n"
            return
        
        # Aplicar errores
        nivel = config['error_nivel']
        texto_con_errores = aplicar_errores(texto, nivel) if nivel > 0 else texto
        
        delay = config['velocidad']
        espera_inicial = config['espera_inicial']
        
        print(f"\nIniciando escritura:")
        print(f"  Longitud: {len(texto_con_errores)} caracteres")
        print(f"  Errores: {ERROR_PORCENTAJES[nivel]}%")
        print(f"  Delay: {delay}s")
        
        if espera_inicial > 0:
            for i in range(int(espera_inicial), 0, -1):
                yield f"data: {json.dumps({'type': 'waiting', 'message': f'Iniciando en {i} segundos...'})}\n\n"
                time.sleep(1)
        
        yield f"data: {json.dumps({'type': 'start', 'total': len(texto_con_errores)})}\n\n"
        
        exito, procesados = escribir_caracteres(texto_con_errores, delay, detener_evento)
        
        if not exito:
            yield f"data: {json.dumps({'type': 'detenido', 'procesados': procesados})}\n\n"
        else:
            yield f"data: {json.dumps({'type': 'completado', 'total': procesados})}\n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/detener', methods=['POST'])
def detener():
    detener_evento.set()
    print("Escritura detenida por el usuario")
    return jsonify({'success': True})

@app.route('/reset', methods=['POST'])
def reset():
    detener_evento.set()
    return jsonify({'success': True})

if __name__ == '__main__':
    print("="*60)
    print("XONIWORK - Servidor de Escritura Automatica")
    print("="*60)
    print("")
    print("Servidor iniciado en: http://localhost:5000")
    print("")
    print("Parametros configurables:")
    print("  - Velocidad: tiempo entre caracteres")
    print("  - Errores: 0=0% 1=2% 2=4% 3=6% 4=8%")
    print("  - Espera inicial: segundos antes de empezar")
    print("")
    print("Para detener: Ctrl+C")
    print("="*60)
    
    app.run(debug=False, host='0.0.0.0', port=5000)
