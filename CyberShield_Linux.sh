#!/bin/bash
# CyberShield IA v3 - Launcher para Linux
# Requiere: python3, tkinter, pillow (opcional), psutil (opcional)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 no encontrado. Instala Python 3.8+"
    exit 1
fi

# Verificar tkinter
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: tkinter no disponible. Instala: sudo apt install python3-tk"
    exit 1
fi

# Instalar dependencias opcionales
pip3 install --quiet pillow psutil 2>/dev/null

# Ejecutar
echo "Iniciando CyberShield IA v3..."
python3 main.pyw
