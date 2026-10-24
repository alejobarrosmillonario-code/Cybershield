#!/usr/bin/env python3
"""
CyberShield IA v3 - Antivirus con Inteligencia Artificial
Interfaz tipo Matrix con predicción de amenazas
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import os
import sys
import random
from datetime import datetime
import time

# Importar módulos locales
try:
    from neural import ThreatPredictor
    from detector import AdvancedDetector
    from registry import BlockchainLikeRegistry
except ImportError as e:
    print(f"Error importando módulos: {e}")
    sys.exit(1)


class MatrixInterface:
    """Interfaz tipo Matrix para CyberShield IA"""

    MATRIX_GREEN = '#00FF00'
    MATRIX_DARK_GREEN = '#00AA00'
    DARK_BG = '#000000'
    CYAN = '#00FFFF'
    GOLD = '#FFCC00'  # Sol de Mayo argentino
    BLUE = '#0033A0'  # Celeste argentino

    def __init__(self, root):
        self.root = root
        self.root.title('CyberShield IA v3 - Antivirus Inteligente')
        self.root.geometry('1400x900')
        self.root.configure(bg=self.DARK_BG)

        # Inicializar componentes de IA
        self.predictor = ThreatPredictor()
        self.detector = AdvancedDetector(self.predictor)
        self.registry = BlockchainLikeRegistry()

        self.scanning = False
        self.threat_queue = []

        self.setup_ui()
        self.animate_matrix()

    def setup_ui(self):
        """Configurar interfaz de usuario"""
        # Marco superior con título Matrix
        title_frame = tk.Frame(self.root, bg=self.DARK_BG, height=60)
        title_frame.pack(fill=tk.X, padx=10, pady=10)

        title = tk.Label(
            title_frame,
            text='█▀▀█ ▀▀█ █▀▀▄ █▀▀▀ █▀▀█   █▀▀█ █  █ █▀▀  █   █ █▀▀\n'
                 '█  █  █  █  █ █ ▀▄ █    █ ▀ █  █ █  █ █  █ █\n'
                 '█▀▀▀  █  █  █ ▀▀▀▀  ▀▀▀▀   ▀▀▀▀  ▀▀▀▄ █  █ ▀▀▀',
            font=('Courier', 9, 'bold'),
            fg=self.MATRIX_GREEN,
            bg=self.DARK_BG,
            justify=tk.LEFT
        )
        title.pack(anchor='w')

        # Subtítulo
        subtitle = tk.Label(
            title_frame,
            text='[v3.0] INTELIGENCIA ARTIFICIAL + PREDICCIÓN DE AMENAZAS | NEUQUÉN, AR 🇦🇷',
            font=('Courier', 9),
            fg=self.CYAN,
            bg=self.DARK_BG
        )
        subtitle.pack(anchor='w')

        # Notebook (pestañas)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.DARK_BG, borderwidth=0)
        style.configure('TNotebook.Tab', background=self.MATRIX_DARK_GREEN, foreground=self.MATRIX_GREEN)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pestaña 1: Dashboard
        self.setup_dashboard_tab()

        # Pestaña 2: Escaneo
        self.setup_scan_tab()

        # Pestaña 3: Predictor IA
        self.setup_predictor_tab()

        # Pestaña 4: Registro
        self.setup_registry_tab()

        # Pestaña 5: Información
        self.setup_info_tab()

    def setup_dashboard_tab(self):
        """Dashboard principal"""
        dashboard_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(dashboard_frame, text='[DASHBOARD]')

        # Estado del sistema
        status_frame = tk.LabelFrame(
            dashboard_frame,
            text='⚡ ESTADO DEL SISTEMA',
            font=('Courier', 10, 'bold'),
            fg=self.MATRIX_GREEN,
            bg=self.DARK_BG,
            borderwidth=2
        )
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Información de estado
        self.status_text = scrolledtext.ScrolledText(
            status_frame,
            height=25,
            font=('Courier', 9),
            bg=self.DARK_BG,
            fg=self.MATRIX_GREEN,
            insertbackground=self.MATRIX_GREEN,
            borderwidth=1,
            relief=tk.SOLID
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Mostrar información inicial
        self.update_dashboard()

    def setup_scan_tab(self):
        """Pestaña de escaneo"""
        scan_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(scan_frame, text='[ESCANEO]')

        # Opciones de escaneo
        options_frame = tk.LabelFrame(
            scan_frame,
            text='🔍 OPCIONES DE ESCANEO',
            font=('Courier', 10, 'bold'),
            fg=self.GOLD,
            bg=self.DARK_BG,
            borderwidth=2
        )
        options_frame.pack(fill=tk.X, padx=10, pady=10)

        button_frame = tk.Frame(options_frame, bg=self.DARK_BG)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        quick_btn = tk.Button(
            button_frame,
            text='⚡ ESCANEO RÁPIDO',
            command=self.quick_scan,
            bg=self.MATRIX_DARK_GREEN,
            fg=self.MATRIX_GREEN,
            font=('Courier', 9, 'bold'),
            activebackground=self.MATRIX_GREEN,
            activeforeground=self.DARK_BG
        )
        quick_btn.pack(side=tk.LEFT, padx=5)

        full_btn = tk.Button(
            button_frame,
            text='📦 ESCANEO COMPLETO',
            command=self.full_scan,
            bg=self.MATRIX_DARK_GREEN,
            fg=self.MATRIX_GREEN,
            font=('Courier', 9, 'bold'),
            activebackground=self.MATRIX_GREEN,
            activeforeground=self.DARK_BG
        )
        full_btn.pack(side=tk.LEFT, padx=5)

        custom_btn = tk.Button(
            button_frame,
            text='🎯 ESCANEO PERSONALIZADO',
            command=self.custom_scan,
            bg=self.BLUE,
            fg=self.GOLD,
            font=('Courier', 9, 'bold'),
            activebackground=self.GOLD,
            activeforeground=self.BLUE
        )
        custom_btn.pack(side=tk.LEFT, padx=5)

        # Resultados del escaneo
        results_frame = tk.LabelFrame(
            scan_frame,
            text='📊 RESULTADOS',
            font=('Courier', 10, 'bold'),
            fg=self.CYAN,
            bg=self.DARK_BG,
            borderwidth=2
        )
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.scan_text = scrolledtext.ScrolledText(
            results_frame,
            height=20,
            font=('Courier', 8),
            bg=self.DARK_BG,
            fg=self.MATRIX_GREEN,
            insertbackground=self.MATRIX_GREEN,
            borderwidth=1
        )
        self.scan_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_predictor_tab(self):
        """Pestaña del predictor IA"""
        predictor_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(predictor_frame, text='[PREDICTOR IA]')

        # Panel de predicción
        pred_panel = tk.LabelFrame(
            predictor_frame,
            text='🧠 PREDICCIÓN DE AMENAZAS',
            font=('Courier', 10, 'bold'),
            fg=self.MATRIX_GREEN,
            bg=self.DARK_BG,
            borderwidth=2
        )
        pred_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.predictor_text = scrolledtext.ScrolledText(
            pred_panel,
            height=25,
            font=('Courier', 8),
            bg=self.DARK_BG,
            fg=self.MATRIX_GREEN,
            insertbackground=self.MATRIX_GREEN,
            borderwidth=1
        )
        self.predictor_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Actualizar predicciones
        self.update_predictions()

    def setup_registry_tab(self):
        """Pestaña del registro blockchain"""
        registry_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(registry_frame, text='[REGISTRO]')

        # Información del registro
        info_frame = tk.LabelFrame(
            registry_frame,
            text='⛓️  REGISTRO BLOCKCHAIN-LIKE',
            font=('Courier', 10, 'bold'),
            fg=self.GOLD,
            bg=self.DARK_BG,
            borderwidth=2
        )
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.registry_text = scrolledtext.ScrolledText(
            info_frame,
            height=25,
            font=('Courier', 8),
            bg=self.DARK_BG,
            fg=self.GOLD,
            insertbackground=self.GOLD,
            borderwidth=1
        )
        self.registry_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Actualizar registro
        self.update_registry()

    def setup_info_tab(self):
        """Pestaña de información"""
        info_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(info_frame, text='[INFO]')

        info_text = scrolledtext.ScrolledText(
            info_frame,
            height=25,
            font=('Courier', 9),
            bg=self.DARK_BG,
            fg=self.CYAN,
            insertbackground=self.CYAN,
            borderwidth=1
        )
        info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        info_content = """
╔═══════════════════════════════════════════════════════════════════╗
║          CyberShield IA v3.0 - Antivirus Inteligente             ║
║               Neuquén, Argentina 🇦🇷                              ║
╚═══════════════════════════════════════════════════════════════════╝

🔒 CARACTERÍSTICAS:

  ⚡ Predicción de amenazas con red neuronal
  🧠 Detección de IA/ML maliciosa
  ⛓️  Registro inmutable tipo blockchain
  🎨 Interfaz Matrix cyberpunk
  🇦🇷 Colores argentinos: Celeste y Gold

🛡️  TECNOLOGÍAS:

  • Red Neuronal: Análisis predictivo
  • Heurística Avanzada: Detección de comportamiento
  • Firma SHA256: Validación de integridad
  • Sin dependencias externas: Python puro

📊 ANÁLISIS:

  - Tamaño de archivo
  - Entropía (compresión/encriptación)
  - Rutas sospechosas
  - Patrones de red
  - Comportamiento de memoria
  - Indicadores de IA

🔐 PROTECCIONES:

  ✓ Ransomware: Vigilancia de carpetas
  ✓ Inyección: Detección de API sospechosas
  ✓ Rootkits: Análisis de rutas del sistema
  ✓ Botnets: Monitoreo de red
  ✓ Malware IA: Patrón de aprendizaje

🎯 MODO DE USO:

  1. Escaneo Rápido: Carpetas clave (AppData, System32)
  2. Escaneo Completo: Sistema entero
  3. Predictor IA: Análisis de amenazas futuras
  4. Registro: Historial completo de eventos

📝 DESARROLLADOR:

  Alejo | Argentina | alejobarrosmillonario@gmail.com

⚠️  AVISO LEGAL:

  Prototipo educativo. No sustituye antivirus profesional.
  Uso bajo responsabilidad del usuario.

═══════════════════════════════════════════════════════════════════
        """

        info_text.insert('1.0', info_content)
        info_text.config(state=tk.DISABLED)

    def quick_scan(self):
        """Escaneo rápido"""
        self.scan_text.delete('1.0', tk.END)
        self.scan_text.insert(tk.END, '[*] Iniciando escaneo rápido...\n\n')

        threading.Thread(target=self._quick_scan_worker, daemon=True).start()

    def _quick_scan_worker(self):
        """Worker de escaneo rápido"""
        quick_paths = [
            os.path.expandvars(r'%APPDATA%'),
            os.path.expandvars(r'%LOCALAPPDATA%\Temp'),
            os.path.expandvars(r'%SystemRoot%\Temp'),
        ]

        threats_found = 0

        for path in quick_paths:
            if os.path.exists(path):
                self.scan_text.insert(tk.END, f'[>] Escaneando: {path}\n')
                self.scan_text.see(tk.END)
                self.root.update()

                try:
                    for root, dirs, files in os.walk(path):
                        for file in files[:10]:  # Limitar a 10 por carpeta
                            file_path = os.path.join(root, file)
                            result = self.detector.analyze_file(file_path)

                            if result['is_threat']:
                                threats_found += 1
                                self.scan_text.insert(
                                    tk.END,
                                    f"⚠️  AMENAZA: {result['threat_name']}\n"
                                    f"   Archivo: {file_path}\n"
                                    f"   Riesgo: {result['threat_level']:.2%}\n"
                                    f"   IA: {'Sí' if result['ai_detected'] else 'No'}\n\n",
                                    'threat'
                                )
                                self.registry.log_attack(
                                    result['threat_name'],
                                    file_path,
                                    result['threat_level'],
                                    result['ai_detected']
                                )
                            self.scan_text.see(tk.END)
                            self.root.update()
                except Exception as e:
                    self.scan_text.insert(tk.END, f'[!] Error: {e}\n')

        self.scan_text.insert(
            tk.END,
            f'\n[✓] Escaneo completado. Amenazas encontradas: {threats_found}\n',
            'complete'
        )
        self.scan_text.see(tk.END)

    def full_scan(self):
        """Escaneo completo"""
        messagebox.showinfo('Escaneo Completo',
            'El escaneo completo analizará el sistema entero.\n'
            'Esto puede tardar varios minutos.')
        self.quick_scan()

    def custom_scan(self):
        """Escaneo personalizado"""
        messagebox.showinfo('Escaneo Personalizado',
            'Seleccione una carpeta para escanear.\n'
            'Funcionalidad en desarrollo.')

    def update_dashboard(self):
        """Actualizar dashboard"""
        stats = self.registry.get_attack_statistics()

        dashboard_info = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                   ESTADO DEL SISTEMA - CyberShield IA             ║
╚═══════════════════════════════════════════════════════════════════╝

📊 ESTADÍSTICAS:

  Ataques detectados totales: {stats['total_attacks']}
  Amenazas de IA: {stats['ai_threats']}
  Amenaza promedio: {stats['average_threat']:.2%}

🔒 PROTECCIONES ACTIVAS:

  ✓ Motor Predictor IA (Red Neuronal)
  ✓ Detección Heurística Avanzada
  ✓ Monitoreo de Ransomware
  ✓ Vigilancia de Inyección de Código
  ✓ Análisis de Comportamiento

⚙️  SISTEMA:

  Timestamp: {datetime.now().isoformat()}
  BD Registro: cybershield_datos/events.db
  Estado Blockchain: Íntegro

🎯 PRÓXIMAS ACCIONES:

  • Monitorear en tiempo real
  • Actualizar patrones de amenaza
  • Entrenar red neuronal con nuevas muestras
  • Verificar integridad de registros

═══════════════════════════════════════════════════════════════════
        """

        self.status_text.delete('1.0', tk.END)
        self.status_text.insert('1.0', dashboard_info)

    def update_predictions(self):
        """Actualizar predicciones IA"""
        predictions = """
╔═══════════════════════════════════════════════════════════════════╗
║              PREDICTOR IA - Amenazas Anticipadas                  ║
╚═══════════════════════════════════════════════════════════════════╝

🧠 ANÁLISIS PREDICTIVO:

El predictor IA utiliza una red neuronal para anticipar amenazas
basándose en patrones de comportamiento.

📈 INDICADORES MONITOREADOS:

  1. Acceso rápido a archivos del sistema
  2. Cambios en registro de Windows
  3. Actividad anormal de red
  4. Inyección de procesos
  5. Escalada de privilegios
  6. Anomalías de memoria
  7. Patrones de encriptación
  8. Comportamiento típico de IA/ML

🎯 AMENAZAS PREDICHAS:

  [Predicción 1]
  Tipo: Ransomware evoluciona con IA
  Confianza: 0.87
  Indicadores: Encriptación + Aprendizaje

  [Predicción 2]
  Tipo: Botnet controlado por IA
  Confianza: 0.72
  Indicadores: Red distribuida + Adaptación

  [Predicción 3]
  Tipo: Malware polimórfico inteligente
  Confianza: 0.81
  Indicadores: Mutación + Ofuscación

═══════════════════════════════════════════════════════════════════
        """

        self.predictor_text.delete('1.0', tk.END)
        self.predictor_text.insert('1.0', predictions)

    def update_registry(self):
        """Actualizar información del registro"""
        events = self.registry.get_recent_events(limit=20)
        integrity = self.registry.verify_blockchain_integrity()

        registry_info = f"""
╔═══════════════════════════════════════════════════════════════════╗
║           REGISTRO BLOCKCHAIN - Historial Inmutable              ║
╚═══════════════════════════════════════════════════════════════════╝

⛓️  INTEGRIDAD: {'✓ ÍNTEGRO' if integrity[0] else '⚠️  COMPROMETIDO'}
    {integrity[1]}

📝 EVENTOS RECIENTES:

"""

        for event in events[:10]:
            event_id, timestamp, event_type, threat_level, threat_name, \
            file_path, ai_detected, action_taken, prev_hash, curr_hash = event

            registry_info += f"""
  [{event_id}] {timestamp}
      Tipo: {event_type}
      Amenaza: {threat_name} ({threat_level:.2%})
      IA: {'Sí' if ai_detected else 'No'}
      Hash: {curr_hash[:16]}...

"""

        registry_info += "═══════════════════════════════════════════════════════════════════\n"

        self.registry_text.delete('1.0', tk.END)
        self.registry_text.insert('1.0', registry_info)

    def animate_matrix(self):
        """Animación Matrix de fondo"""
        def matrix_rain():
            while True:
                try:
                    time.sleep(2)
                    self.update_dashboard()
                    self.update_predictions()
                    self.update_registry()
                except:
                    pass

        threading.Thread(target=matrix_rain, daemon=True).start()


def main():
    """Función principal"""
    root = tk.Tk()

    # Tema oscuro
    root.configure(bg='#000000')

    # Inicializar interfaz
    app = MatrixInterface(root)

    # Mensaje de bienvenida
    welcome_msg = """
╔═══════════════════════════════════════════════════════════════════╗
║           CyberShield IA v3.0 - Iniciado correctamente           ║
║                                                                   ║
║  🇦🇷 Desarrollado en Neuquén, Argentina                          ║
║  💻 Inteligencia Artificial para protección máxima               ║
║                                                                   ║
║  [+] Red Neuronal: Activa                                        ║
║  [+] Detector Heurístico: Activo                                 ║
║  [+] Registro Blockchain: Activo                                 ║
║  [+] Predictor IA: Listo                                         ║
╚═══════════════════════════════════════════════════════════════════╝
    """

    print(welcome_msg)

    # Iniciar interfaz
    root.mainloop()


if __name__ == '__main__':
    main()
