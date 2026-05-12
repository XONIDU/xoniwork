
# 💼 XONIWORK v1.0.0

**Simulador de Escritura Automática** – Emula trabajo de escritura manual en computadora con errores controlados y parametrización web.

## ⚙️ Características

- 🌐 **Interfaz web** con diseño cyberpunk y configuración en tiempo real
- 📄 **Soporte multi-formato**: TXT, PDF, DOCX
- ✍️ **Escritura caracter por caracter** con `pyautogui`
- 🎲 **Errores ortográficos controlados**: 0%, 2%, 4%, 6%, 8%
- ⚡ **Velocidad ajustable**: tiempo entre caracteres (0.01s - 1s)
- ⏱️ **Espera inicial configurable**: segundos antes de empezar
- 🔄 **Eliminación automática de acentos** (normalización de texto)
- 🐍 **Lanzador automático** (`start.py`) que instala dependencias con soporte `--break-system-packages` en Arch/Manjaro/Fedora
- 🖥️ **Multiplataforma**: Windows, Linux, macOS

## 📦 Estructura del Proyecto

```
XONIWORK/
├── xoniwork.py             # Servidor Flask principal
├── start.py                # Lanzador automático (instalador universal)
├── templates/
│   └── index.html          # Interfaz web cyberpunk
├── uploads/                # Carpeta para archivos subidos (creación automática)
└── README.md               # Este archivo
```

## 🔧 Requisitos

- **Software**: Python 3.8+, navegador web moderno
- **Dependencias**: Flask, PyAutoGUI, PyPDF2, python-docx, unidecode
- **Linux (opcional)**: `scrot` y `xdotool` para funcionalidad completa de PyAutoGUI

## 🚀 Instalación y Uso

### 1. Clonar o descargar el proyecto

```bash
git clone https://github.com/XONIDU/xoniwork.git
cd xoniwork
```

### 2. Ejecutar el lanzador universal

```bash
python start.py
```

El lanzador automáticamente:
- Detecta tu sistema operativo (Windows/Linux/macOS)
- Instala pip si no está disponible
- Instala todas las dependencias con los flags apropiados
- Crea archivo `.bat` para Windows
- Abre el navegador en `http://localhost:5000`

### 3. Uso de la interfaz web

1. **Configurar parámetros**:
   - **Velocidad**: segundos entre caracteres (0.05 = 20 caracteres/segundo)
   - **Nivel de errores**: 0% (perfecto) a 8% (máximos errores)
   - **Espera inicial**: segundos antes de comenzar a escribir

2. **Subir archivo**:
   - Formatos soportados: `.txt`, `.pdf`, `.docx`
   - El texto se extrae automáticamente y se normaliza (elimina acentos)

3. **Iniciar escritura**:
   - Posiciona el cursor en el lugar donde quieres escribir
   - Haz clic en **"INICIAR ESCRITURA"**
   - El programa esperará los segundos configurados
   - Comenzará a escribir caracter por caracter

4. **Controles**:
   - **DETENER**: Detiene la escritura inmediatamente
   - **LIMPIAR**: Borra el archivo cargado y reinicia

## 🎮 Ejemplo de Uso

```bash
# Escritura de ensayo de 1000 palabras
1. Subes ensayo.docx
2. Configuras: velocidad 0.05s, errores 4%, espera 3s
3. Posicionas cursor en editor de texto
4. Click "INICIAR ESCRITURA"
5. Resultado: texto escrito como si fuera humano (con errores orgánicos)
```

## 🎨 Personalización del Error

Los errores ortográficos se generan con:
- **Nivel 0 (0%)**: Sin errores, escritura perfecta
- **Nivel 1 (2%)**: 2% de los caracteres modificados
- **Nivel 2 (4%)**: 4% de los caracteres modificados
- **Nivel 3 (6%)**: 6% de los caracteres modificados
- **Nivel 4 (8%)**: 8% de los caracteres modificados

Los errores consisten en:
- Reemplazo por teclas adyacentes en teclado QWERTY (70% de probabilidad)
- Cambio por caracter anterior/siguiente (30% de probabilidad)

## 📚 Dependencias Detalladas

| Dependencia | Versión | Uso |
|-------------|---------|-----|
| Flask | >=2.0 | Servidor web |
| PyAutoGUI | >=0.9 | Automatización de teclado |
| PyPDF2 | >=3.0 | Extracción de PDFs |
| python-docx | >=0.8 | Extracción de Word |
| unidecode | >=1.3 | Eliminación de acentos |

## 🔧 Instalación Manual de Dependencias

Si prefieres instalar manualmente:

```bash
# Linux (Debian/Ubuntu/Mint)
pip install --user flask pyautogui PyPDF2 python-docx unidecode

# Linux (Arch/Manjaro/Fedora)
pip install --break-system-packages flask pyautogui PyPDF2 python-docx unidecode

# Windows/macOS
pip install flask pyautogui PyPDF2 python-docx unidecode
```

## ⚠️ Notas para Linux

Para funcionamiento completo de PyAutoGUI en Linux, se necesitan:

```bash
# Debian/Ubuntu/Mint
sudo apt install scrot xdotool

# Arch/Manjaro
sudo pacman -S scrot xdotool

# Fedora
sudo dnf install scrot xdotool
```



## 🎯 Casos de Uso

- **Pruebas de interfaces**: Simular entrada de usuario en formularios
- **Demostraciones**: Automatizar escritura de código o documentos
- **Entrenamiento**: Generar datos de entrenamiento para correctores ortográficos
- **Emulación laboral**: Simular trabajo de digitación

## 📊 Métricas en Tiempo Real

La interfaz muestra:
- Progreso de escritura (porcentaje y caracteres)
- Logs detallados de cada acción
- Estado del proceso (esperando, escribiendo, completado)

## 🛠️ Solución de Problemas

### Error: "No se pudo instalar pip"
- **Windows**: Descarga Python oficial y marca "Add to PATH"
- **Linux**: `sudo apt install python3-pip` (Debian) o equivalente

### Error: "pyautogui no escribe"
- Verifica que la ventana destino esté enfocada
- En Linux, instala `scrot` y `xdotool`

### Error: "No se extrajo texto del PDF"
- Algunos PDFs son escaneados (imagen), no contienen texto editable

## 📝 Licencia

Uso exclusivamente educativo. No apto para aplicaciones críticas o malintencionadas.

## 🏆 Créditos

**Desarrollado por:** Darian Alberto Camacho Salas  
**Organización:** XONIDU  
**#Somos XONINDU**

## 📧 Contacto

- **Email**: xonidu@gmail.com
- **GitHub**: [@XONIDU](https://github.com/XONIDU)

---

### ✨ Características Únicas de XONIWORK

| Característica | XONISPAM | XONIDIP | **XONIWORK** |
|----------------|----------|---------|---------------|
| Spam de mensajes | ✅ | ❌ | ❌ |
| Generación de diplomas | ❌ | ✅ | ❌ |
| **Escritura automática humana** | ❌ | ❌ | ✅ |
| **Errores ortográficos controlados** | ❌ | ❌ | ✅ |
| **Extracción de PDF/DOCX** | ❌ | ❌ | ✅ |
| **Delay entre caracteres** | ❌ | ❌ | ✅ |

---

**Versión:** 1.0.0  
**Última actualización:** Enero 2026  
**Estado:** Estable ✅
