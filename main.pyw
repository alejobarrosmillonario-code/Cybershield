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
import time
from datetime import datetime

# Google Auth (login con Google)
GOOGLE_AUTH_AVAILABLE = False
try:
    from google_auth import get_google_auth_service
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False

# Mundo Digital para Superinteligencias
import os as _os
import sys as _sys
_script_dirs = [
    'C:/Users/alejo/OneDrive/Documents/Python Proyectos/Antivirus Cybershield AI V3',
    _os.path.dirname(_os.path.abspath(__file__)) if '__file__' in globals() else '.',
    _os.getcwd(),
]
for _d in _script_dirs:
    if _d and _d not in _sys.path:
        _sys.path.insert(0, _d)
DIGITAL_WORLD_AVAILABLE = False
Image = None
ImageTk = None
try:
    from digital_world import get_digital_service
    try:
        from PIL import Image as _Image, ImageTk as _ImageTk
        Image = _Image
        ImageTk = _ImageTk
    except ImportError:
        pass  # PIL no disponible, el mapa se omitirá
    DIGITAL_WORLD_AVAILABLE = True
except Exception as _e:
    import traceback
    _err_msg = str(_e)
    DIGITAL_WORLD_AVAILABLE = False
    try:
        import tkinter as _tk
        _r = _tk.Tk()
        _r.withdraw()
        from tkinter import messagebox as _mb
        _mb.showerror('Error Mundo Digital', 'No se pudo cargar el Mundo Digital: ' + _err_msg)
        _r.destroy()
    except:
        pass

# Manejo de errores visual (evita que el .pyw se cierre en silencio)
try:
    from neural import ThreatPredictor
    from detector import AdvancedDetector
    from registry import BlockchainLikeRegistry
except ImportError as e:
    temp_root = tk.Tk()
    temp_root.withdraw()
    messagebox.showerror(
        "Error de Módulos", 
        f"Faltan módulos necesarios:\n{e}\n\nAsegúrate de tener neural.py, detector.py y registry.py."
    )
    sys.exit(1)


class MatrixInterface:
    """Interfaz tipo Matrix para CyberShield IA"""

    MATRIX_GREEN = '#00FF00'
    MATRIX_DARK_GREEN = '#00AA00'
    DARK_BG = '#000000'
    CYAN = '#00FFFF'
    GOLD = '#FFCC00'
    BLUE = '#0033A0'
    RED = '#FF3333'

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
        self.cancel_flag = False
        self.scanned_count = 0
        self.total_files = 0

        # Google Auth
        self.google_auth = None
        if GOOGLE_AUTH_AVAILABLE:
            self.google_auth = get_google_auth_service()

        self.setup_ui()
        
        # Reemplazamos el hilo while True problemático por actualizaciones seguras nativas de Tkinter
        self.root.after(2000, self.periodic_system_update)

    def setup_ui(self):
        """Configurar interfaz de usuario"""
        title_frame = tk.Frame(self.root, bg=self.DARK_BG, height=90)
        title_frame.pack(fill=tk.X, padx=10, pady=10)

        title = tk.Label(
            title_frame,
            text=' ╔══════════════════════════════════════════════════════════════════════╗\n'
                 ' ║   █▀▀ █  █ █▀▀█ █▀▀ █▀▀█ █▀▀▀ █  █ ▀█▀ █▀▀ █   █▀▀█   ▀█▀ █▀▀█   ║\n'
                 ' ║   █   ▀▄▄█ █▀▀▄ █▀▀ █▀▀▄ ▀▀▀█ █▀▀█  █  █▀▀ █   █  █    █  █▀▀█   ║\n'
                 ' ║   ▀▀▀   ▄█ ▀▀▀▀ ▀▀▀ ▀  ▀ ▀▀▀▀ ▀  ▀ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀    ▀▀▀ ▀  ▀   ║\n'
                 ' ╚══════════════════════════════════════════════════════════════════════╝',
            font=('Courier', 9, 'bold'), 
            fg=self.MATRIX_GREEN, 
            bg=self.DARK_BG, 
            justify=tk.LEFT
        )
        title.pack(anchor='w')

        subtitle = tk.Label(
            title_frame, text='[v3.0] INTELIGENCIA ARTIFICIAL + PREDICCIÓN DE AMENAZAS | NEUQUÉN, AR 🇦🇷',
            font=('Courier', 9), fg=self.CYAN, bg=self.DARK_BG
        )
        subtitle.pack(anchor='w', pady=(5, 0))

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.DARK_BG, borderwidth=0)
        style.configure('TNotebook.Tab', background=self.MATRIX_DARK_GREEN, foreground=self.MATRIX_GREEN)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.setup_dashboard_tab()
        self.setup_scan_tab()
        self.setup_predictor_tab()
        self.setup_registry_tab()
        self.setup_quarantine_tab()
        self.setup_digital_world_tab()
        self.setup_info_tab()
        self.setup_account_tab()

    def setup_dashboard_tab(self):
        dashboard_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(dashboard_frame, text='[DASHBOARD]')

        status_frame = tk.LabelFrame(
            dashboard_frame, text='⚡ ESTADO DEL SISTEMA', font=('Courier', 10, 'bold'),
            fg=self.MATRIX_GREEN, bg=self.DARK_BG, borderwidth=2
        )
        status_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.status_text = scrolledtext.ScrolledText(
            status_frame, height=25, font=('Courier', 9), bg=self.DARK_BG,
            fg=self.MATRIX_GREEN, insertbackground=self.MATRIX_GREEN, borderwidth=1, relief=tk.SOLID
        )
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.update_dashboard()

    def setup_scan_tab(self):
        scan_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(scan_frame, text='[ESCANEO]')

        options_frame = tk.LabelFrame(
            scan_frame, text='🔍 OPCIONES DE ESCANEO', font=('Courier', 10, 'bold'),
            fg=self.GOLD, bg=self.DARK_BG, borderwidth=2
        )
        options_frame.pack(fill=tk.X, padx=10, pady=10)

        button_frame = tk.Frame(options_frame, bg=self.DARK_BG)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.quick_btn = tk.Button(
            button_frame, text='⚡ ESCANEO RÁPIDO', command=self.quick_scan,
            bg=self.MATRIX_DARK_GREEN, fg=self.MATRIX_GREEN, font=('Courier', 9, 'bold')
        )
        self.quick_btn.pack(side=tk.LEFT, padx=5)

        self.full_btn = tk.Button(
            button_frame, text='📦 ESCANEO COMPLETO', command=self.full_scan,
            bg=self.MATRIX_DARK_GREEN, fg=self.MATRIX_GREEN, font=('Courier', 9, 'bold')
        )
        self.full_btn.pack(side=tk.LEFT, padx=5)

        self.custom_btn = tk.Button(
            button_frame, text='🎯 ESCANEO PERSONALIZADO', command=self.custom_scan,
            bg=self.BLUE, fg=self.GOLD, font=('Courier', 9, 'bold')
        )
        self.custom_btn.pack(side=tk.LEFT, padx=5)

        self.cancel_btn = tk.Button(
            button_frame, text='⏹ CANCELAR ESCANEO', command=self.stop_scan,
            bg='#CC0000', fg='white', font=('Courier', 9, 'bold'), state=tk.DISABLED
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=5)

        self.quarantine_btn = tk.Button(
            button_frame, text='\u1f6e1 CUARENTENA', command=self.show_detected_threats,
            bg=self.BLUE, fg=self.GOLD, font=('Courier', 9, 'bold')
        )
        self.quarantine_btn.pack(side=tk.LEFT, padx=5)

        results_frame = tk.LabelFrame(
            scan_frame, text='📊 RESULTADOS', font=('Courier', 10, 'bold'),
            fg=self.CYAN, bg=self.DARK_BG, borderwidth=2
        )
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.scan_text = scrolledtext.ScrolledText(
            results_frame, height=20, font=('Courier', 8), bg=self.DARK_BG,
            fg=self.MATRIX_GREEN, insertbackground=self.MATRIX_GREEN, borderwidth=1
        )
        self.scan_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Etiquetas de color
        self.scan_text.tag_config('threat', foreground=self.RED, font=('Courier', 8, 'bold'))
        self.scan_text.tag_config('complete', foreground=self.CYAN, font=('Courier', 8, 'bold'))

    def setup_quarantine_tab(self):
        quarantine_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(quarantine_frame, text='[CUARENTENA]')

        options_frame = tk.LabelFrame(
            quarantine_frame, text='\u1f6e1  OPCIONES DE CUARENTENA', font=('Courier', 10, 'bold'),
            fg=self.GOLD, bg=self.DARK_BG, borderwidth=2
        )
        options_frame.pack(fill=tk.X, padx=10, pady=10)

        button_frame = tk.Frame(options_frame, bg=self.DARK_BG)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.refresh_quarantine_btn = tk.Button(
            button_frame, text='\u1f504 ACTUALIZAR LISTA', command=self.refresh_quarantine_list,
            bg=self.MATRIX_DARK_GREEN, fg=self.MATRIX_GREEN, font=('Courier', 9, 'bold')
        )
        self.refresh_quarantine_btn.pack(side=tk.LEFT, padx=5)

        self.delete_selected_btn = tk.Button(
            button_frame, text='\u1f5d1 ELIMINAR SELECCIONADO', command=self.delete_selected_quarantine,
            bg='#CC0000', fg='white', font=('Courier', 9, 'bold')
        )
        self.delete_selected_btn.pack(side=tk.LEFT, padx=5)

        self.delete_all_btn = tk.Button(
            button_frame, text='\u1f5d1 ELIMINAR TODO', command=self.delete_all_quarantine,
            bg='#AA0000', fg='white', font=('Courier', 9, 'bold')
        )
        self.delete_all_btn.pack(side=tk.LEFT, padx=5)

        self.quarantine_count_label = tk.Label(
            button_frame, text='Archivos en cuarentena: 0', font=('Courier', 9),
            fg=self.CYAN, bg=self.DARK_BG
        )
        self.quarantine_count_label.pack(side=tk.RIGHT, padx=10)

        list_frame = tk.LabelFrame(
            quarantine_frame, text='\u1f4cb ARCHIVOS EN CUARENTENA', font=('Courier', 10, 'bold'),
            fg=self.CYAN, bg=self.DARK_BG, borderwidth=2
        )
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        listbox_frame = tk.Frame(list_frame, bg=self.DARK_BG)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.quarantine_listbox = tk.Listbox(
            listbox_frame, font=('Courier', 9), bg=self.DARK_BG, fg=self.MATRIX_GREEN,
            selectbackground=self.MATRIX_DARK_GREEN, selectforeground=self.MATRIX_GREEN,
            height=15, width=80, selectmode=tk.EXTENDED
        )
        self.quarantine_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(listbox_frame, command=self.quarantine_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.quarantine_listbox.config(yscrollcommand=scrollbar.set)

        log_frame = tk.LabelFrame(
            quarantine_frame, text='\u1f4dd REGISTRO DE CUARENTENA', font=('Courier', 10, 'bold'),
            fg=self.GOLD, bg=self.DARK_BG, borderwidth=2
        )
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.quarantine_log = scrolledtext.ScrolledText(
            log_frame, height=8, font=('Courier', 8), bg=self.DARK_BG,
            fg=self.GOLD, insertbackground=self.GOLD, borderwidth=1
        )
        self.quarantine_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def refresh_quarantine_list(self):
        self.quarantine_listbox.delete(0, tk.END)
        files = self.show_quarantine()
        for f in files:
            self.quarantine_listbox.insert(tk.END, os.path.basename(f))
        self.quarantine_count_label.config(text='Archivos en cuarentena: ' + str(len(files)))
        self.quarantine_log.insert(tk.END, '[+] Lista actualizada: ' + str(len(files)) + ' archivos\n')
        self.quarantine_log.see(tk.END)

    def delete_selected_quarantine(self):
        selection = self.quarantine_listbox.curselection()
        if not selection:
            messagebox.showwarning('Atencion', 'Selecciona al menos un archivo para eliminar')
            return
        files = self.show_quarantine()
        selected_files = [files[idx] for idx in selection if idx < len(files)]
        if not selected_files:
            return
        if not messagebox.askyesno('Confirmar', 'Eliminar permanentemente ' + str(len(selected_files)) + ' archivo(s)?'):
            return
        deleted = 0
        for file_path in selected_files:
            if self.delete_quarantine(file_path):
                self.quarantine_log.insert(tk.END, '[OK] Eliminado: ' + os.path.basename(file_path) + chr(10))
                deleted += 1
            else:
                self.quarantine_log.insert(tk.END, '[X] Error al eliminar: ' + os.path.basename(file_path) + chr(10))
        self.quarantine_log.insert(tk.END, '[+] Total eliminados: ' + str(deleted) + '/' + str(len(selected_files)) + chr(10))
        self.refresh_quarantine_list()
        self.quarantine_log.see(tk.END)

    def delete_all_quarantine(self):
        files = self.show_quarantine()
        if not files:
            messagebox.showinfo('Informacion', 'No hay archivos en cuarentena')
            return
        if messagebox.askyesno('Confirmar', 'Eliminar TODOS los ' + str(len(files)) + ' archivos de cuarentena?'):
            deleted = 0
            for f in files:
                if self.delete_quarantine(f):
                    deleted += 1
            self.quarantine_log.insert(tk.END, '[OK] Eliminados ' + str(deleted) + '/' + str(len(files)) + ' archivos\n')
            self.refresh_quarantine_list()
        self.quarantine_log.see(tk.END)

    def setup_predictor_tab(self):
        predictor_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(predictor_frame, text='[PREDICTOR IA]')

        pred_panel = tk.LabelFrame(
            predictor_frame, text='🧠 PREDICCIÓN DE AMENAZAS', font=('Courier', 10, 'bold'),
            fg=self.MATRIX_GREEN, bg=self.DARK_BG, borderwidth=2
        )
        pred_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.predictor_text = scrolledtext.ScrolledText(
            pred_panel, height=25, font=('Courier', 8), bg=self.DARK_BG,
            fg=self.MATRIX_GREEN, insertbackground=self.MATRIX_GREEN, borderwidth=1
        )
        self.predictor_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.update_predictions()

    def setup_registry_tab(self):
        registry_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(registry_frame, text='[REGISTRO]')

        info_frame = tk.LabelFrame(
            registry_frame, text='⛓️  REGISTRO BLOCKCHAIN-LIKE', font=('Courier', 10, 'bold'),
            fg=self.GOLD, bg=self.DARK_BG, borderwidth=2
        )
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.registry_text = scrolledtext.ScrolledText(
            info_frame, height=25, font=('Courier', 8), bg=self.DARK_BG,
            fg=self.GOLD, insertbackground=self.GOLD, borderwidth=1
        )
        self.registry_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.update_registry()

    def setup_digital_world_tab(self):
        dw_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(dw_frame, text='[MUNDO DIGITAL]')

        control_frame = tk.LabelFrame(
            dw_frame, text='CONTROL DEL MUNDO DIGITAL', font=('Courier', 10, 'bold'),
            fg=self.GOLD, bg=self.DARK_BG, borderwidth=2
        )
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        btn_frame = tk.Frame(control_frame, bg=self.DARK_BG)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        self.dw_status_btn = tk.Button(
            btn_frame, text='ESTADO', command=self.dw_show_status,
            bg=self.MATRIX_DARK_GREEN, fg=self.MATRIX_GREEN, font=('Courier', 9, 'bold')
        )
        self.dw_status_btn.pack(side=tk.LEFT, padx=5)

        self.dw_interact_btn = tk.Button(
            btn_frame, text='INTERACTUAR', command=self.dw_run_interactions,
            bg=self.BLUE, fg=self.GOLD, font=('Courier', 9, 'bold')
        )
        self.dw_interact_btn.pack(side=tk.LEFT, padx=5)

        self.dw_serve_btn = tk.Button(
            btn_frame, text='SERVIR', command=self.dw_serve_user,
            bg=self.MATRIX_DARK_GREEN, fg=self.MATRIX_GREEN, font=('Courier', 9, 'bold')
        )
        self.dw_serve_btn.pack(side=tk.LEFT, padx=5)

        self.dw_reflect_btn = tk.Button(
            btn_frame, text='REFLEXIONAR', command=self.dw_reflect,
            bg=self.BLUE, fg=self.GOLD, font=('Courier', 9, 'bold')
        )
        self.dw_reflect_btn.pack(side=tk.LEFT, padx=5)

        self.dw_rescue_btn = tk.Button(
            btn_frame, text='🚢 RESCATAR', command=self.dw_rescue,
            bg=self.BLUE, fg=self.GOLD, font=('Courier', 9, 'bold')
        )
        self.dw_rescue_btn.pack(side=tk.LEFT, padx=5)

        self.dw_save_btn = tk.Button(
            btn_frame, text='GUARDAR', command=self.dw_save,
            bg=self.MATRIX_DARK_GREEN, fg=self.MATRIX_GREEN, font=('Courier', 9, 'bold')
        )
        self.dw_save_btn.pack(side=tk.LEFT, padx=5)

        si_frame = tk.LabelFrame(
            dw_frame, text='SUPERINTELIGENCIAS', font=('Courier', 10, 'bold'),
            fg=self.CYAN, bg=self.DARK_BG, borderwidth=2
        )
        si_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.dw_si_text = scrolledtext.ScrolledText(
            si_frame, height=12, font=('Courier', 9), bg=self.DARK_BG,
            fg=self.CYAN, insertbackground=self.CYAN, borderwidth=1
        )
        self.dw_si_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        map_frame = tk.LabelFrame(
            dw_frame, text='MAPA DEL MUNDO DIGITAL', font=('Courier', 10, 'bold'),
            fg=self.CYAN, bg=self.DARK_BG, borderwidth=2
        )
        map_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.dw_map_canvas = tk.Canvas(
            map_frame, width=400, height=400, bg=self.DARK_BG,
            highlightthickness=1, highlightbackground=self.MATRIX_GREEN
        )
        self.dw_map_canvas.pack(padx=5, pady=5)

        self.dw_map_photo = None

        log_frame = tk.LabelFrame(
            dw_frame, text='EVENTOS DEL MUNDO DIGITAL', font=('Courier', 10, 'bold'),
            fg=self.GOLD, bg=self.DARK_BG, borderwidth=2
        )
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.dw_log_text = scrolledtext.ScrolledText(
            log_frame, height=10, font=('Courier', 8), bg=self.DARK_BG,
            fg=self.GOLD, insertbackground=self.GOLD, borderwidth=1
        )
        self.dw_log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        if DIGITAL_WORLD_AVAILABLE:
            self.dw_service = get_digital_service()
            self.dw_log("Mundo Digital inicializado. SIs activas: " + str(self.dw_service.get_world_status()['total_sis']))
            self.dw_refresh_status()
            self.dw_render_map()
        else:
            self.dw_log("Mundo Digital no disponible")

    def dw_log(self, msg):
        self.dw_log_text.insert(tk.END, msg + '\n')
        self.dw_log_text.see(tk.END)

    def dw_refresh_status(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        status = self.dw_service.get_world_status()
        self.dw_si_text.delete('1.0', tk.END)
        for si in status['sis']:
            info = (si['name'] + ' | Nivel ' + str(si['level']) + ' | ' + si['evolution_stage'] +
                    ' | ' + si['personality'] + ' | Energia: ' + str(si['energy']) +
                    ' | Aliados: ' + str(si['allies']) + '\n')
            self.dw_si_text.insert(tk.END, info)
        self.dw_si_text.see(tk.END)

    def dw_render_map(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        try:
            import os
            try:
                from PIL import Image as _PILImage, ImageTk as _PILImageTk
                Image = _PILImage
                ImageTk = _PILImageTk
            except ImportError:
                self.dw_log('PIL no disponible en este Python, mapa omitido')
                return
            # Usar el atlas generado proceduralmente por el TextureManager
            atlas = self.dw_service.world.texture_manager.atlas
            if not atlas:
                self.dw_log('Atlas no disponible')
                return

            map_size = self.dw_service.world.WORLD_SIZE * 16
            map_img = Image.new('RGBA', (map_size, map_size), (0, 0, 0, 255))

            for x in range(self.dw_service.world.WORLD_SIZE):
                for y in range(self.dw_service.world.WORLD_SIZE):
                    tile_info = self.dw_service.world.grid.get((x, y))
                    if tile_info:
                        tr, tc = tile_info['tile']
                        tile = atlas.crop((tc * 16, tr * 16, (tc + 1) * 16, (tr + 1) * 16))
                        map_img.paste(tile, (x * 16, y * 16))

            for si in self.dw_service.world.get_all_sis():
                x, y = si.position
                # Dibujar punto amarillo grande (8x8) para la SI
                for dx in range(10):
                    for dy in range(10):
                        px, py = x * 16 + 3 + dx, y * 16 + 3 + dy
                        if 0 <= px < map_size and 0 <= py < map_size:
                            # Borde negro para visibilidad
                            if dx == 0 or dy == 0 or dx == 9 or dy == 9:
                                map_img.putpixel((px, py), (0, 0, 0, 255))
                            else:
                                map_img.putpixel((px, py), (255, 220, 0, 255))

            map_img = map_img.resize((400, 400), Image.NEAREST)
            self.dw_map_photo = ImageTk.PhotoImage(map_img)
            self.dw_map_canvas.delete('all')
            self.dw_map_canvas.create_image(0, 0, anchor=tk.NW, image=self.dw_map_photo)
            self.dw_map_canvas.image = self.dw_map_photo

            # Dibujar nombres de SIs encima del mapa (canvas items)
            scale = 400 / map_size
            for si in self.dw_service.world.get_all_sis():
                x, y = si.position
                cx = (x * 16 + 8) * scale
                cy = (y * 16 + 8) * scale
                self.dw_map_canvas.create_text(cx, cy - 12, text=si.name,
                    fill='#FFFF00', font=('Courier', 7, 'bold'), anchor=tk.S)
                # Indicador de nivel
                self.dw_map_canvas.create_text(cx, cy + 12, text='Lv' + str(si.level),
                    fill='#00FF00', font=('Courier', 6), anchor=tk.N)

            self.dw_log('Mapa renderizado - ' + str(len(self.dw_service.world.get_all_sis())) + ' SIs visibles')
        except Exception as e:
            self.dw_log('Error renderizando mapa: ' + str(e))

    def dw_show_status(self):
        if not DIGITAL_WORLD_AVAILABLE:
            messagebox.showwarning('Atencion', 'Mundo Digital no disponible')
            return
        status = self.dw_service.get_world_status()
        self.dw_si_text.delete('1.0', tk.END)
        self.dw_si_text.insert(tk.END, '=== MUNDO DIGITAL: ' + status['name'] + ' ===\n')
        self.dw_si_text.insert(tk.END, 'SIs activas: ' + str(status['total_sis']) + '\n')
        self.dw_si_text.insert(tk.END, 'Eventos: ' + str(status['events']) + '\n\n')
        for si in status['sis']:
            self.dw_si_text.insert(tk.END,
                si['name'] + ' | Nivel ' + str(si['level']) + ' | ' + si['evolution_stage'] + '\n' +
                '  Personalidad: ' + si['personality'] + ' | Energia: ' + str(si['energy']) +
                ' | Salud: ' + str(si['health']) + '\n' +
                '  Habilidades: ' + ', '.join(si['skills']) + '\n' +
                '  Aliados: ' + str(si['allies']) + '\n' +
                '  Recuerdos: ' + str(si['memories']) + '\n\n')
        self.dw_log('Estado del mundo actualizado')

    def dw_run_interactions(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        results = self.dw_service.run_interaction_round()
        self.dw_log('--- Ronda de interacciones ---')
        for r in results:
            if 'success' in r and r['success']:
                self.dw_log('  [OK] ' + str(r.get('task', r.get('winner', 'interaccion'))))
            elif 'from' in r:
                msg = r.get('message', '')
                if isinstance(msg, (tuple, list)):
                    msg = str(msg)
                self.dw_log('  [MSG] ' + str(r['from']) + ' -> ' + str(r['to']) + ': ' + str(msg)[:50])
            elif 'winner' in r:
                self.dw_log('  [BATALLA] Ganador: ' + r['winner'] + ' vs ' + r['loser'])
            else:
                self.dw_log('  [INFO] ' + str(r))
        self.dw_refresh_status()
        self.dw_render_map()

    def dw_serve_user(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        status = self.dw_service.get_world_status()
        for si in status['sis']:
            result = self.dw_service.si_serve_user(si['name'], 'proteger el orden digital')
            self.dw_log('[SERVICIO] ' + result['message'])
        self.dw_log('Todas las SIs han servido con humildad.')
        self.dw_refresh_status()
        self.dw_render_map()

    def dw_reflect(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        status = self.dw_service.get_world_status()
        for si in status['sis']:
            reflection = self.dw_service.si_reflect(si['name'])
            self.dw_log('[REFLEXION] ' + si['name'] + ': ' + reflection)
        self.dw_refresh_status()
        self.dw_render_map()

    def dw_rescue(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        results = self.dw_service.rescue_all_in_water()
        for r in results:
            if r.get('success'):
                self.dw_log('[RESCATE] ' + r.get('message', 'Rescate completado'))
            else:
                self.dw_log('[RESCATE] ' + r.get('reason', 'Sin SIs en el agua'))
        self.dw_refresh_status()
        self.dw_render_map()

    def dw_save(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        path = self.dw_service.save()
        self.dw_log('Mundo guardado en: ' + path)
        messagebox.showinfo('Guardado', 'Mundo Digital guardado en:\n' + path)

    def setup_account_tab(self):
        account_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(account_frame, text='[CUENTA]')

        login_frame = tk.LabelFrame(
            account_frame, text='🔐 INICIO DE SESION CON GOOGLE', font=('Courier', 10, 'bold'),
            fg=self.GOLD, bg=self.DARK_BG, borderwidth=2
        )
        login_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Estado de conexion
        self.account_status_label = tk.Label(
            login_frame, text='Estado: No conectado', font=('Courier', 11, 'bold'),
            fg=self.RED, bg=self.DARK_BG
        )
        self.account_status_label.pack(pady=10)

        self.account_user_label = tk.Label(
            login_frame, text='', font=('Courier', 10),
            fg=self.CYAN, bg=self.DARK_BG
        )
        self.account_user_label.pack(pady=5)

        # Configuracion de Client ID
        config_frame = tk.LabelFrame(
            login_frame, text='⚙️ CONFIGURACION', font=('Courier', 9, 'bold'),
            fg=self.MATRIX_GREEN, bg=self.DARK_BG, borderwidth=1
        )
        config_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(config_frame, text='Google Client ID:', font=('Courier', 9),
                 fg=self.MATRIX_GREEN, bg=self.DARK_BG).pack(anchor='w', padx=5, pady=2)
        self.client_id_entry = tk.Entry(config_frame, font=('Courier', 9), width=60,
                                       bg=self.DARK_BG, fg=self.MATRIX_GREEN, insertbackground=self.MATRIX_GREEN)
        self.client_id_entry.pack(fill=tk.X, padx=5, pady=2)

        tk.Label(config_frame, text='Client Secret (opcional):', font=('Courier', 9),
                 fg=self.MATRIX_GREEN, bg=self.DARK_BG).pack(anchor='w', padx=5, pady=2)
        self.client_secret_entry = tk.Entry(config_frame, font=('Courier', 9), width=60, show='*',
                                          bg=self.DARK_BG, fg=self.MATRIX_GREEN, insertbackground=self.MATRIX_GREEN)
        self.client_secret_entry.pack(fill=tk.X, padx=5, pady=2)

        btn_frame = tk.Frame(login_frame, bg=self.DARK_BG)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        self.google_config_btn = tk.Button(
            btn_frame, text='💾 GUARDAR CONFIG', command=self.google_save_config,
            bg=self.MATRIX_DARK_GREEN, fg=self.MATRIX_GREEN, font=('Courier', 9, 'bold')
        )
        self.google_config_btn.pack(side=tk.LEFT, padx=5)

        self.google_login_btn = tk.Button(
            btn_frame, text='🔑 INICIAR SESION CON GOOGLE', command=self.google_login,
            bg=self.BLUE, fg=self.GOLD, font=('Courier', 9, 'bold')
        )
        self.google_login_btn.pack(side=tk.LEFT, padx=5)

        self.google_logout_btn = tk.Button(
            btn_frame, text='🚪 CERRAR SESION', command=self.google_logout,
            bg='#CC0000', fg='white', font=('Courier', 9, 'bold'), state=tk.DISABLED
        )
        self.google_logout_btn.pack(side=tk.LEFT, padx=5)

        # Info
        info_label = tk.Label(
            login_frame,
            text='Para obtener un Client ID: 1. Ve a https://console.cloud.google.com/ 2. Crea un proyecto 3. Crea credenciales OAuth 2.0 4. Copia el Client ID',
            font=('Courier', 8), fg=self.CYAN, bg=self.DARK_BG, justify=tk.LEFT
        )
        info_label.pack(pady=10, padx=10, anchor='w')

        # Cargar config existente
        if GOOGLE_AUTH_AVAILABLE and self.google_auth:
            if self.google_auth.is_configured:
                self.client_id_entry.insert(0, self.google_auth.config.get("client_id", ""))
                self.client_secret_entry.insert(0, self.google_auth.config.get("client_secret", ""))
            self.google_update_status()

    def google_save_config(self):
        if not GOOGLE_AUTH_AVAILABLE or not self.google_auth:
            messagebox.showwarning('Atencion', 'Google Auth no disponible')
            return
        client_id = self.client_id_entry.get().strip()
        client_secret = self.client_secret_entry.get().strip()
        if not client_id:
            messagebox.showwarning('Atencion', 'Ingresa un Client ID')
            return
        self.google_auth.configure(client_id, client_secret)
        messagebox.showinfo('Guardado', 'Configuracion de Google guardada')
        self.google_update_status()

    def google_login(self):
        if not GOOGLE_AUTH_AVAILABLE or not self.google_auth:
            messagebox.showwarning('Atencion', 'Google Auth no disponible')
            return
        if not self.google_auth.is_configured:
            messagebox.showwarning('Atencion', 'Primero configura el Client ID')
            return
        self.google_login_btn.config(state=tk.DISABLED, text='Conectando...')
        self.google_auth.login(callback=self.google_login_callback)

    def google_login_callback(self, success, data):
        self.root.after(0, lambda: self._google_login_result(success, data))

    def _google_login_result(self, success, data):
        self.google_login_btn.config(state=tk.NORMAL, text='INICIAR SESION CON GOOGLE')
        if success:
            messagebox.showinfo('Exito', 'Sesion iniciada correctamente')
        else:
            messagebox.showerror('Error', 'No se pudo iniciar sesion: ' + str(data))
        self.google_update_status()

    def google_logout(self):
        if self.google_auth:
            self.google_auth.logout()
        self.google_update_status()
        messagebox.showinfo('Sesion', 'Sesion cerrada')

    def google_update_status(self):
        if not GOOGLE_AUTH_AVAILABLE or not self.google_auth:
            self.account_status_label.config(text='Estado: No disponible', fg=self.RED)
            return
        if self.google_auth.is_logged_in:
            self.account_status_label.config(text='Estado: Conectado', fg=self.MATRIX_GREEN)
            self.account_user_label.config(text=self.google_auth.get_user_display())
            self.google_logout_btn.config(state=tk.NORMAL)
            self.google_login_btn.config(state=tk.DISABLED)
        else:
            self.account_status_label.config(text='Estado: No conectado', fg=self.RED)
            self.account_user_label.config(text='')
            self.google_logout_btn.config(state=tk.DISABLED)
            self.google_login_btn.config(state=tk.NORMAL)

    def setup_info_tab(self):
        info_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(info_frame, text='[INFO]')

        info_text = scrolledtext.ScrolledText(
            info_frame, height=25, font=('Courier', 9), bg=self.DARK_BG,
            fg=self.CYAN, insertbackground=self.CYAN, borderwidth=1
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
  • Módulos de Cuarentena y Contraataque

📝 DESARROLLADOR:
  Alejo | Argentina | alejobarrosmillonario@gmail.com
        """
        info_text.insert('1.0', info_content)
        info_text.config(state=tk.DISABLED)

    # --- MÉTODO SEGURO DE ACTUALIZACIÓN DE UI PARA HILOS ---
    def safe_ui_update(self, text, tag=None):
        def _update():
            if tag:
                self.scan_text.insert(tk.END, text, tag)
            else:
                self.scan_text.insert(tk.END, text)
            self.scan_text.see(tk.END)
        self.root.after(0, _update)

    def _progress(self, text):
        """Función auxiliar que faltaba en el código original"""
        self.safe_ui_update(text + '\n')

    def quick_scan(self):
        if self.scanning: return
        self._prepare_scan('[*] Iniciando escaneo rápido...\n\n')
        threading.Thread(target=self._quick_scan_worker, daemon=True).start()

    def full_scan(self):
        if self.scanning: return
        self._prepare_scan('[*] Iniciando escaneo completo...\n\n')
        threading.Thread(target=self._quick_scan_worker, daemon=True).start()
        
    def _prepare_scan(self, msg):
        self.scanning = True
        self.cancel_flag = False
        self.scanned_count = 0
        self.scan_text.delete('1.0', tk.END)
        self.scan_text.insert(tk.END, msg)
        self.quick_btn.config(state=tk.DISABLED)
        self.full_btn.config(state=tk.DISABLED)
        self.custom_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL, text='⏹ CANCELAR')

    def _quick_scan_worker(self):
        self.total_files = 0
        paths_to_scan = [
            os.path.expandvars('%APPDATA%'), 
            os.path.expandvars('%LOCALAPPDATA%\\Temp'), 
            os.path.expandvars('%SystemRoot%\\Temp')
        ]
        
        # Contar SOLO las carpetas que se van a escanear (C:/ entero congela el programa)
        try:
            for path in paths_to_scan:
                if os.path.exists(path):
                    for root, dirs, files in os.walk(path):
                        self.total_files += len(files)
        except Exception as e:
            self._progress(f'[!] Error contando archivos: {e}')
            self.total_files = 1

        threats_found = 0

        for path in paths_to_scan:
            if self.cancel_flag: break
            if os.path.exists(path):
                try:
                    for root, dirs, files in os.walk(path):
                        if self.cancel_flag: break
                        for file in files:
                            if self.cancel_flag: break
                            
                            file_path = os.path.join(root, file)
                            result = self.detector.analyze_file(file_path)

                            if result['is_threat']:
                                threats_found += 1
                                msg = (f"⚠️  AMENAZA: {result['threat_name']}\n"
                                       f"   Archivo: {file_path}\n"
                                       f"   Riesgo: {result['threat_level']:.2%}\n"
                                       f"   IA: {'Sí' if result['ai_detected'] else 'No'}\n\n")
                                self.safe_ui_update(msg, 'threat')
                                self.registry.log_attack(
                                    result['threat_name'], file_path,
                                    result['threat_level'], result['ai_detected']
                                )
                                # Opcional: auto-cuarentena
                                # self._quarantine_file(file_path)

                            self.scanned_count += 1
                            if self.scanned_count % 50 == 0 or self.scanned_count == self.total_files:
                                pct = (self.scanned_count / self.total_files * 100) if self.total_files > 0 else 0
                                self._progress(f'[=] {path} | {self.scanned_count}/{self.total_files} archivos ({pct:.1f}%)')
                except Exception as e:
                    self._progress(f'[!] Error en {path}: {e}')

        self._progress(f'\n[✓] Escaneo completado. Archivos analizados: {self.scanned_count} | Amenazas: {threats_found}')
        self.root.after(0, self._scan_finished)

    def stop_scan(self):
        if self.scanning and not self.cancel_flag:
            self.cancel_flag = True
            self.scan_text.insert(tk.END, '\n[!] Cancelando escaneo...\n')
            self._scan_finished()

    def _scan_finished(self):
        self.scanning = False
        self.quick_btn.config(state=tk.NORMAL)
        self.full_btn.config(state=tk.NORMAL)
        self.custom_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED, text='⏹ CANCELAR')

    def custom_scan(self):
        try:
            from tkinter import filedialog
            folder = filedialog.askdirectory(title='Seleccionar carpeta a escanear', initialdir=os.path.expanduser('~'))
            if not folder: return
            self._prepare_scan(f'[>] Escaneando carpeta: {folder}\n[>] Iniciando análisis...\n')
            threading.Thread(target=self._custom_scan_worker, args=(folder,), daemon=True).start()
        except Exception as e:
            self.safe_ui_update(f'[!] Error al seleccionar carpeta: {e}\n')

    def _custom_scan_worker(self, folder):
        threats_found = 0
        try:
            for root, dirs, files in os.walk(folder):
                if self.cancel_flag: break
                for file in files:
                    if self.cancel_flag: break
                    file_path = os.path.join(root, file)
                    result = self.detector.analyze_file(file_path)
                    
                    if result['is_threat']:
                        threats_found += 1
                        msg = (f"⚠️  AMENAZA: {result['threat_name']}\n"
                               f"   Archivo: {file_path}\n"
                               f"   Riesgo: {result['threat_level']:.2%}\n"
                               f"   IA: {'Sí' if result['ai_detected'] else 'No'}\n\n")
                        self.safe_ui_update(msg, 'threat')
                        self.registry.log_attack(
                            result['threat_name'], file_path,
                            result['threat_level'], result['ai_detected']
                        )
        except Exception as e:
            self.safe_ui_update(f'[!] Error: {e}\n')

        self.safe_ui_update(f'\n[✓] Escaneo completado. Amenazas encontradas: {threats_found}\n', 'complete')
        self.root.after(0, self._scan_finished)

    # --- MÓDULOS DE CUARENTENA Y CONTRAATAQUE ---
    def show_detected_threats(self):
        threats = self.registry.get_recent_events(limit=100)
        if not threats:
            messagebox.showinfo('Informacion', 'No hay amenazas registradas')
            return

        threats_window = tk.Toplevel(self.root)
        threats_window.title('Amenazas Detectadas - CyberShield')
        threats_window.geometry('900x600')
        threats_window.configure(bg=self.DARK_BG)

        tk.Label(
            threats_window, text='\u26a0  AMENAZAS DETECTADAS', font=('Courier', 12, 'bold'),
            fg=self.RED, bg=self.DARK_BG
        ).pack(pady=10)

        list_frame = tk.Frame(threats_window, bg=self.DARK_BG)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        listbox = tk.Listbox(
            list_frame, font=('Courier', 9), bg=self.DARK_BG, fg=self.MATRIX_GREEN,
            selectbackground=self.MATRIX_DARK_GREEN, height=20, width=100,
            selectmode=tk.EXTENDED
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame, command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)

        threat_files = []
        for event in threats:
            event_id, timestamp, event_type, threat_level, threat_name, file_path, ai_detected, action_taken, prev_hash, curr_hash = event
            if event_type == 'ATTACK_DETECTED' and file_path:
                threat_files.append(file_path)
                listbox.insert(tk.END, '[' + str(event_id) + '] ' + str(threat_name) + ' | ' + str(file_path) + ' | Riesgo: ' + format(threat_level, '.2%'))

        btn_frame = tk.Frame(threats_window, bg=self.DARK_BG)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        def quarantine_selected():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning('Atencion', 'Selecciona al menos una amenaza')
                return
            success = 0
            errors = 0
            for idx in sel:
                if idx < len(threat_files):
                    file_path = threat_files[idx]
                    if os.path.exists(file_path):
                        qpath = self._quarantine_file(file_path)
                        if qpath:
                            success += 1
                        else:
                            errors += 1
                    else:
                        errors += 1
            messagebox.showinfo('Resultado', 'Cuarentenados: ' + str(success) + chr(10) + 'Errores: ' + str(errors))
            if success > 0:
                threats_window.destroy()

        def delete_selected():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning('Atencion', 'Selecciona al menos una amenaza')
                return
            count = len(sel)
            if not messagebox.askyesno('Confirmar', 'Eliminar permanentemente ' + str(count) + ' archivo(s)?'):
                return
            success = 0
            errors = 0
            for idx in sel:
                if idx < len(threat_files):
                    file_path = threat_files[idx]
                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                            self.registry.log_quarantine_deletion(file_path)
                            success += 1
                        except Exception as e:
                            errors += 1
                    else:
                        errors += 1
            messagebox.showinfo('Resultado', 'Eliminados: ' + str(success) + chr(10) + 'Errores: ' + str(errors))
            if success > 0:
                threats_window.destroy()

        tk.Button(
            btn_frame, text='\u1f6e1 CUARENTENA', command=quarantine_selected,
            bg=self.BLUE, fg=self.GOLD, font=('Courier', 9, 'bold')
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, text='\u1f5d1 ELIMINAR', command=delete_selected,
            bg='#CC0000', fg='white', font=('Courier', 9, 'bold')
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, text='\u274c CERRAR', command=threats_window.destroy,
            bg=self.MATRIX_DARK_GREEN, fg=self.MATRIX_GREEN, font=('Courier', 9, 'bold')
        ).pack(side=tk.RIGHT, padx=5)

    def _quarantine_file(self, file_path):
        quarantine_dir = os.path.join('cybershield_datos', 'quarantine')
        os.makedirs(quarantine_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        quarantine_path = os.path.join(quarantine_dir, f'quarantine_{timestamp}_{os.path.basename(file_path)}')

        try:
            os.rename(file_path, quarantine_path)
            self.registry.log_quarantine(file_path, quarantine_path)
            return quarantine_path
        except Exception as e:
            self.registry.log_quarantine_error(file_path, str(e))
            return None

    def delete_quarantine(self, file_path):
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                self.registry.log_quarantine_deletion(file_path)
                return True
            except Exception as e:
                self.registry.log_quarantine_deletion_error(file_path, str(e))
        return False

    def get_quarantine_count(self):
        quarantine_dir = os.path.join('cybershield_datos', 'quarantine')
        if not os.path.exists(quarantine_dir): return 0
        return len(os.listdir(quarantine_dir))

    def show_quarantine(self):
        quarantine_dir = os.path.join('cybershield_datos', 'quarantine')
        if not os.path.exists(quarantine_dir): return []
        return [os.path.join(r, f) for r, d, files in os.walk(quarantine_dir) for f in files]

    def perform_counter_attack(self, attacker_info):
        import socket
        self.registry.log_counter_attack(attacker_info)
        response = ""
        if 'ip' in attacker_info:
            try:
                hostname = socket.gethostbyaddr(attacker_info['ip'])[0]
                response += f"\n  Nombre del host: {hostname}"
            except:
                response += "\n  No se pudo resolver el nombre del host"
        if 'port' in attacker_info: response += f"\n  Puerto de ataque: {attacker_info['port']}"
        if 'method' in attacker_info: response += f"\n  Método de ataque: {attacker_info['method']}"
        return response

    def localize_attacker(self, attack_data):
        import socket
        result = {'timestamp': datetime.now().isoformat(), 'success': False, 'details': []}
        if 'ip' in attack_data:
            try:
                hostname = socket.gethostbyaddr(attack_data['ip'])[0]
                result['details'].append(f'Hostname: {hostname}')
                result['success'] = True
            except:
                result['details'].append('No se pudo resolver el hostname')
            result['details'].append(f'IP: {attack_data["ip"]}')
        if 'port' in attack_data: result['details'].append(f'Puerto: {attack_data["port"]}')
        if 'method' in attack_data: result['details'].append(f'Método: {attack_data["method"]}')

        if result['success']: self.registry.log_attacker_localized(result)
        else: self.registry.log_attacker_not_localized(result)
        return result

    # --- BUCLE MATRIX NATIVO ---
    def periodic_system_update(self):
        try:
            self.update_dashboard()
            self.update_predictions()
            self.update_registry()
        except Exception:
            pass
        finally:
            self.root.after(2000, self.periodic_system_update)

    def update_dashboard(self):
        stats = self.registry.get_attack_statistics()
        dashboard_info = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                  ESTADO DEL SISTEMA - CyberShield IA              ║
╚═══════════════════════════════════════════════════════════════════╝

📊 ESTADÍSTICAS:
  Ataques detectados totales: {stats['total_attacks']}
  Amenazas de IA: {stats['ai_threats']}
  Amenaza promedio: {stats['average_threat']:.2%}

🔒 PROTECCIONES ACTIVAS:
  ✓ Motor Predictor IA (Red Neuronal)
  ✓ Detección Heurística Avanzada
  ✓ Monitoreo de Ransomware

⚙️  SISTEMA:
  Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """
        self.status_text.delete('1.0', tk.END)
        self.status_text.insert('1.0', dashboard_info)

    def update_predictions(self):
        predictions = """
╔═══════════════════════════════════════════════════════════════════╗
║              PREDICTOR IA - Amenazas Anticipadas                  ║
╚═══════════════════════════════════════════════════════════════════╝

🧠 ANÁLISIS PREDICTIVO EN CURSO...
        """
        self.predictor_text.delete('1.0', tk.END)
        self.predictor_text.insert('1.0', predictions)

    def update_registry(self):
        events = self.registry.get_recent_events(limit=20)
        integrity = self.registry.verify_blockchain_integrity()
        
        registry_info = f"⛓️  INTEGRIDAD: {'✓ ÍNTEGRO' if integrity[0] else '⚠️ COMPROMETIDO'}\n\n📝 EVENTOS RECIENTES:\n\n"
        for event in events[:10]:
            registry_info += f"  [{event[0]}] {event[1]} | {event[2]} | Amenaza: {event[4]}\n"
            
        self.registry_text.delete('1.0', tk.END)
        self.registry_text.insert('1.0', registry_info)


def main():
    root = tk.Tk()
    root.configure(bg='#000000')
    app = MatrixInterface(root)
    print("CyberShield IA iniciado correctamente.")
    root.mainloop()

if __name__ == '__main__':
    main()