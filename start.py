#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONIWORK 2026 - Lanzador Universal con Gestor de Automatización
Simulador de escritura automática para emular trabajo
Desarrollador: Darian Alberto Camacho Salas
Organización: XONIDU
#Somos XONINDU
"""

import subprocess
import sys
import os
import platform
import shutil
import time
import webbrowser
import threading
from pathlib import Path

# ============================================================================
# Colores para terminal
# ============================================================================
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def supports_color():
        if platform.system() == 'Windows':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                return kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                return False
        return True

if not Colors.supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_') and attr != 'supports_color':
            setattr(Colors, attr, '')

# ============================================================================
# Detección del sistema
# ============================================================================
def get_system():
    return platform.system().lower()

def get_linux_distro():
    if get_system() != 'linux':
        return None
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content or 'debian' in content or 'mint' in content or 'antix' in content:
                    return 'debian-based'
                elif 'arch' in content or 'manjaro' in content:
                    return 'arch-based'
                elif 'fedora' in content:
                    return 'fedora'
                elif 'centos' in content or 'rhel' in content:
                    return 'centos'
                elif 'opensuse' in content:
                    return 'opensuse'
        if shutil.which('apt'):
            return 'debian-based'
        elif shutil.which('pacman'):
            return 'arch-based'
        elif shutil.which('dnf'):
            return 'fedora'
        elif shutil.which('yum'):
            return 'centos'
        elif shutil.which('zypper'):
            return 'opensuse'
        return 'linux-generico'
    except:
        return 'linux-generico'

def get_python_command():
    if get_system() == 'windows':
        return ['python']
    else:
        try:
            subprocess.run(['python3', '--version'], capture_output=True, check=True)
            return ['python3']
        except:
            return ['python']

def get_pip_command():
    return [sys.executable, '-m', 'pip']

def get_install_flags():
    flags = []
    sistema = get_system()
    distro = get_linux_distro()
    if sistema == 'linux':
        if distro in ['arch-based', 'fedora']:
            flags.append('--break-system-packages')
        else:
            flags.append('--user')
    elif sistema == 'darwin':
        flags.append('--user')
    return flags

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_xoniwork_path():
    script_dir = get_script_dir()
    rutas = [
        os.path.join(script_dir, 'xoniwork.py'),
        os.path.join(os.getcwd(), 'xoniwork.py')
    ]
    for r in rutas:
        if os.path.exists(r):
            return r
    return None

def print_banner():
    sistema = get_system()
    distro = get_linux_distro()
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'DESCONOCIDO')
    
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗
║                    XONIWORK 2026 v1.0                    ║
║           Simulador de Escritura Automatica              ║
║                  Para emular trabajo                     ║
║                   en computadora                         ║
║                                                            ║
║               Sistema detectado: {sistema_texto:<27} ║
║                                                            ║
║               Desarrollado por: Darian Alberto           ║
║                      Camacho Salas                       ║
║                      Organizacion: XONIDU                ║
║                      #Somos XONINDU                      ║
╚══════════════════════════════════════════════════════════╝{Colors.END}
    """
    print(banner)

def mostrar_ayuda():
    ayuda = f"""
{Colors.BOLD}XONIWORK - Simulador de Escritura Automatica{Colors.END}

{Colors.BOLD}DESCRIPCION:{Colors.END}
  Emula escritura manual en computadora con errores controlados.
  Sube un archivo (txt, word, pdf) y el programa escribira el texto
  como si lo hiciera una persona, con errores ortograficos opcionales.

{Colors.BOLD}OPCIONES WEB:{Colors.END}
  - Velocidad de escritura (caracteres por segundo)
  - Porcentaje de errores (0% a 8%)
  - Tiempo de espera inicial

{Colors.BOLD}CONTROLES:{Colors.END}
  Ctrl+C     - Detener la escritura
  Web        - Configurar parametros en http://localhost:5000

{Colors.BOLD}USO:{Colors.END}
  1. Ejecutar: python start.py
  2. Abrir navegador en http://localhost:5000
  3. Subir archivo y configurar parametros
  4. Posicionar cursor y hacer clic en "INICIAR"
    """
    print(ayuda)

# ============================================================================
# Verificacion de dependencias
# ============================================================================
def check_python():
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def check_pip():
    try:
        cmd = get_pip_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def install_pip_linux():
    distro = get_linux_distro()
    print(f"{Colors.YELLOW}Instalando pip en Linux ({distro})...{Colors.END}")
    if distro == 'debian-based':
        try:
            subprocess.run(['sudo', 'apt', 'update'], check=False)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'python3-pip'], check=True)
            return True
        except:
            return False
    elif distro == 'arch-based':
        try:
            subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'python-pip'], check=True)
            return True
        except:
            return False
    elif distro == 'fedora':
        try:
            subprocess.run(['sudo', 'dnf', 'install', '-y', 'python3-pip'], check=True)
            return True
        except:
            return False
    return False

def install_pip_windows():
    print(f"{Colors.YELLOW}Instalando pip en Windows...{Colors.END}")
    try:
        subprocess.run([sys.executable, '-m', 'ensurepip', '--upgrade'], check=True)
        return True
    except:
        return False

def install_pip_macos():
    print(f"{Colors.YELLOW}Instalando pip en macOS...{Colors.END}")
    try:
        subprocess.run(['python3', '-m', 'ensurepip', '--upgrade'], check=True)
        return True
    except:
        try:
            subprocess.run(['brew', 'install', 'python3'], check=True)
            return True
        except:
            return False

def check_flask():
    try:
        __import__('flask')
        return True
    except ImportError:
        return False

def check_pyautogui():
    try:
        __import__('pyautogui')
        return True
    except ImportError:
        return False

def check_pypdf2():
    try:
        __import__('PyPDF2')
        return True
    except ImportError:
        return False

def check_python_docx():
    try:
        __import__('docx')
        return True
    except ImportError:
        return False

def check_unidecode():
    try:
        __import__('unidecode')
        return True
    except ImportError:
        return False

def install_dependencies():
    deps = ['flask', 'pyautogui', 'PyPDF2', 'python-docx', 'unidecode']
    print(f"{Colors.YELLOW}Instalando dependencias...{Colors.END}")
    flags = get_install_flags()
    all_ok = True
    
    for dep in deps:
        try:
            if dep == 'python-docx':
                __import__('docx')
            else:
                __import__(dep)
            print(f"{Colors.GREEN}  - {dep} ya instalado{Colors.END}")
        except ImportError:
            print(f"{Colors.YELLOW}  - Instalando {dep}...{Colors.END}")
            success = False
            try:
                cmd = get_pip_command() + ['install', dep] + flags
                subprocess.run(cmd, check=True, capture_output=True)
                success = True
            except:
                try:
                    cmd = get_pip_command() + ['install', dep]
                    subprocess.run(cmd, check=True)
                    success = True
                except:
                    pass
            
            if success:
                print(f"{Colors.GREEN}    - {dep} instalado{Colors.END}")
            else:
                print(f"{Colors.RED}    - Error instalando {dep}{Colors.END}")
                all_ok = False
    
    return all_ok

def check_system_deps_linux():
    if get_system() != 'linux':
        return True
    
    distro = get_linux_distro()
    faltantes = []
    
    if not shutil.which('scrot'):
        faltantes.append('scrot')
    if not shutil.which('xdotool'):
        faltantes.append('xdotool')
    
    if faltantes:
        print(f"{Colors.YELLOW}Faltan dependencias: {', '.join(faltantes)}{Colors.END}")
        respuesta = input("Instalar automaticamente? (s/n): ")
        if respuesta.lower() == 's':
            if distro == 'debian-based':
                try:
                    subprocess.run(['sudo', 'apt', 'update'], check=False)
                    subprocess.run(['sudo', 'apt', 'install', '-y'] + faltantes, check=True)
                    print(f"{Colors.GREEN}Dependencias instaladas{Colors.END}")
                except:
                    print(f"{Colors.RED}Error instalando{Colors.END}")
                    return False
            elif distro == 'arch-based':
                try:
                    subprocess.run(['sudo', 'pacman', '-S', '--noconfirm'] + faltantes, check=True)
                    print(f"{Colors.GREEN}Dependencias instaladas{Colors.END}")
                except:
                    print(f"{Colors.RED}Error instalando{Colors.END}")
                    return False
            elif distro == 'fedora':
                try:
                    subprocess.run(['sudo', 'dnf', 'install', '-y'] + faltantes, check=True)
                    print(f"{Colors.GREEN}Dependencias instaladas{Colors.END}")
                except:
                    print(f"{Colors.RED}Error instalando{Colors.END}")
                    return False
        else:
            print(f"{Colors.YELLOW}Algunas funciones pueden no funcionar{Colors.END}")
            return False
    return True

# ============================================================================
# Crear archivos .bat para Windows
# ============================================================================
def create_windows_bat():
    if get_system() != 'windows':
        return
    
    simple_bat = '''@echo off
title XONIWORK 2026
color 0A
echo ========================================
echo      XONIWORK 2026 - Simulador de Escritura
echo      Desarrollado por Darian Alberto
echo ========================================
echo.
python start.py
pause
'''
    with open('XONIWORK.bat', 'w', encoding='utf-8') as f:
        f.write(simple_bat)
    print(f"{Colors.GREEN}Creado XONIWORK.bat{Colors.END}")

# ============================================================================
# Abrir navegador
# ============================================================================
def open_browser():
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

# ============================================================================
# Funcion principal
# ============================================================================
def main():
    if get_system() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
    
    print_banner()
    
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', '/?']:
        mostrar_ayuda()
        if get_system() != 'windows':
            input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    if get_system() == 'windows':
        create_windows_bat()
    
    if not check_python():
        print(f"\n{Colors.RED}Python no esta instalado{Colors.END}")
        sys.exit(1)
    
    py_ver = subprocess.run(get_python_command() + ['--version'], capture_output=True, text=True).stdout.strip()
    print(f"{Colors.BOLD}Python:{Colors.END} {py_ver}")
    
    if not check_pip():
        print(f"\n{Colors.YELLOW}Pip no encontrado. Instalando...{Colors.END}")
        sistema = get_system()
        if sistema == 'linux':
            if not install_pip_linux():
                print(f"{Colors.RED}No se pudo instalar pip{Colors.END}")
                sys.exit(1)
        elif sistema == 'windows':
            if not install_pip_windows():
                print(f"{Colors.RED}No se pudo instalar pip{Colors.END}")
                sys.exit(1)
        elif sistema == 'darwin':
            if not install_pip_macos():
                print(f"{Colors.RED}No se pudo instalar pip{Colors.END}")
                sys.exit(1)
    else:
        print(f"{Colors.GREEN}Pip disponible{Colors.END}")
    
    print(f"\n{Colors.BOLD}Verificando dependencias...{Colors.END}")
    if not install_dependencies():
        print(f"{Colors.RED}Error instalando dependencias{Colors.END}")
        respuesta = input("Continuar de todas formas? (s/n): ")
        if respuesta.lower() != 's':
            sys.exit(1)
    
    if get_system() == 'linux':
        check_system_deps_linux()
    
    script_dir = get_script_dir()
    xoniwork_path = get_xoniwork_path()
    
    if not xoniwork_path:
        print(f"\n{Colors.RED}xoniwork.py no encontrado{Colors.END}")
        sys.exit(1)
    
    xoniwork_dir = os.path.dirname(xoniwork_path)
    os.chdir(xoniwork_dir)
    
    uploads_dir = os.path.join(xoniwork_dir, 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    
    templates_dir = os.path.join(xoniwork_dir, 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    print(f"\n{Colors.GREEN}XONIWORK listo para iniciar{Colors.END}")
    print(f"{Colors.CYAN}Abriendo navegador en http://localhost:5000{Colors.END}")
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    print(f"{Colors.YELLOW}Para detener: Ctrl+C en esta terminal{Colors.END}")
    print("-"*50)
    
    try:
        python_cmd = get_python_command()
        subprocess.run(python_cmd + [xoniwork_path])
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Programa detenido{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}")
    
    print(f"\n{Colors.GREEN}Gracias por usar XONIWORK{Colors.END}")
    print(f"{Colors.BLUE}#Somos XONINDU{Colors.END}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
