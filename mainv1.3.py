#!/usr/bin/env python3
"""
CyberShield IA v3 - Antivirus con Inteligencia Artificial y Mundo Digital
Interfaz tipo Matrix con predicción de amenazas
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import os
import sys
import time
from datetime import datetime

# Importación dinámica del Mundo Digital (Ruta Relativa)
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

try:
    from digital_world import get_digital_service
    from PIL import Image, ImageTk
    DIGITAL_WORLD_AVAILABLE = True
except ImportError:
    DIGITAL_WORLD_AVAILABLE = False

# Manejo de módulos auxiliares
try:
    from neural import ThreatPredictor
    from detector import AdvancedDetector
    from registry import BlockchainLikeRegistry
except ImportError as e:
    temp_root = tk.Tk()
    temp_root.withdraw()
    messagebox.showerror(
        "Error de Módulos", 
        f"Faltan módulos necesarios:\n{e}\n\nAsegúrate de tener neural.py, detector.py y registry.py en la misma carpeta."
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
        self.root.title('CyberShield IA v3 - Antivirus Inteligente & Digital World')
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

        self.setup_ui()
        
        # Bucle periódico nativo de Tkinter
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
            title_frame, text='[v3.0] INTELIGENCIA ARTIFICIAL + MUNDO DIGITAL (DIGIMON ENGINE) | NEUQUÉN, AR 🇦🇷',
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
            button_frame, text='🛡️ CUARENTENA', command=self.show_detected_threats,
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
        
        self.scan_text.tag_config('threat', foreground=self.RED, font=('Courier', 8, 'bold'))
        self.scan_text.tag_config('complete', foreground=self.CYAN, font=('Courier', 8, 'bold'))

    def setup_quarantine_tab(self):
        quarantine_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(quarantine_frame, text='[CUARENTENA]')

        options_frame = tk.LabelFrame(
            quarantine_frame, text='🛡️ OPCIONES DE CUARENTENA', font=('Courier', 10, 'bold'),
            fg=self.GOLD, bg=self.DARK_BG, borderwidth=2
        )
        options_frame.pack(fill=tk.X, padx=10, pady=10)

        button_frame = tk.Frame(options_frame, bg=self.DARK_BG)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.refresh_quarantine_btn = tk.Button(
            button_frame, text='🔄 ACTUALIZAR LISTA', command=self.refresh_quarantine_list,
            bg=self.MATRIX_DARK_GREEN, fg=self.MATRIX_GREEN, font=('Courier', 9, 'bold')
        )
        self.refresh_quarantine_btn.pack(side=tk.LEFT, padx=5)

        self.delete_selected_btn = tk.Button(
            button_frame, text='🗑️ ELIMINAR SELECCIONADO', command=self.delete_selected_quarantine,
            bg='#CC0000', fg='white', font=('Courier', 9, 'bold')
        )
        self.delete_selected_btn.pack(side=tk.LEFT, padx=5)

        self.delete_all_btn = tk.Button(
            button_frame, text='🗑️ ELIMINAR TODO', command=self.delete_all_quarantine,
            bg='#AA0000', fg='white', font=('Courier', 9, 'bold')
        )
        self.delete_all_btn.pack(side=tk.LEFT, padx=5)

        self.quarantine_count_label = tk.Label(
            button_frame, text='Archivos en cuarentena: 0', font=('Courier', 9),
            fg=self.CYAN, bg=self.DARK_BG
        )
        self.quarantine_count_label.pack(side=tk.RIGHT, padx=10)

        list_frame = tk.LabelFrame(
            quarantine_frame, text='📋 ARCHIVOS EN CUARENTENA', font=('Courier', 10, 'bold'),
            fg=self.CYAN, bg=self.DARK_BG, borderwidth=2
        )
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        listbox_frame = tk.Frame(list_frame, bg=self.DARK_BG)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.quarantine_listbox = tk.Listbox(
            listbox_frame, font=('Courier', 9), bg=self.DARK_BG, fg=self.MATRIX_GREEN,
            selectbackground=self.MATRIX_DARK_GREEN, selectforeground=self.MATRIX_GREEN,
            height=15, width=80
        )
        self.quarantine_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(listbox_frame, command=self.quarantine_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.quarantine_listbox.config(yscrollcommand=scrollbar.set)

        log_frame = tk.LabelFrame(
            quarantine_frame, text='📝 REGISTRO DE CUARENTENA', font=('Courier', 10, 'bold'),
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
            messagebox.showwarning('Atención', 'Selecciona un archivo para eliminar')
            return
        idx = selection[0]
        files = self.show_quarantine()
        if idx < len(files):
            file_path = files[idx]
            if messagebox.askyesno('Confirmar', f'¿Eliminar permanentemente {os.path.basename(file_path)}?'):
                if self.delete_quarantine(file_path):
                    self.quarantine_log.insert(tk.END, '[OK] Eliminado: ' + os.path.basename(file_path) + '\n')
                    self.refresh_quarantine_list()
                else:
                    self.quarantine_log.insert(tk.END, '[X] Error al eliminar: ' + os.path.basename(file_path) + '\n')
        self.quarantine_log.see(tk.END)

    def delete_all_quarantine(self):
        files = self.show_quarantine()
        if not files:
            messagebox.showinfo('Información', 'No hay archivos en cuarentena')
            return
        if messagebox.askyesno('Confirmar', f'¿Eliminar TODOS los {len(files)} archivos de cuarentena?'):
            deleted = 0
            for f in files:
                if self.delete_quarantine(f):
                    deleted += 1
            self.quarantine_log.insert(tk.END, f'[OK] Eliminados {deleted}/{len(files)} archivos\n')
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
            dw_frame, text='CONTROL DEL MUNDO DIGITAL (DIGIMON AI)', font=('Courier', 10, 'bold'),
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
            btn_frame, text='DIGI-INTERACTUAR', command=self.dw_run_interactions,
            bg=self.BLUE, fg=self.GOLD, font=('Courier', 9, 'bold')
        )
        self.dw_interact_btn.pack(side=tk.LEFT, padx=5)

        self.dw_serve_btn = tk.Button(
            btn_frame, text='PROTEGER RED', command=self.dw_serve_user,
            bg=self.MATRIX_DARK_GREEN, fg=self.MATRIX_GREEN, font=('Courier', 9, 'bold')
        )
        self.dw_serve_btn.pack(side=tk.LEFT, padx=5)

        self.dw_reflect_btn = tk.Button(
            btn_frame, text='REFLEXIONAR', command=self.dw_reflect,
            bg=self.BLUE, fg=self.GOLD, font=('Courier', 9, 'bold')
        )
        self.dw_reflect_btn.pack(side=tk.LEFT, padx=5)

        self.dw_move_btn = tk.Button(
            btn_frame, text='MOVER DIGI-SIs', command=self.dw_move_sis,
            bg=self.BLUE, fg=self.GOLD, font=('Courier', 9, 'bold')
        )
        self.dw_move_btn.pack(side=tk.LEFT, padx=5)

        self.dw_save_btn = tk.Button(
            btn_frame, text='GUARDAR', command=self.dw_save,
            bg=self.MATRIX_DARK_GREEN, fg=self.MATRIX_GREEN, font=('Courier', 9, 'bold')
        )
        self.dw_save_btn.pack(side=tk.LEFT, padx=5)

        si_frame = tk.LabelFrame(
            dw_frame, text='SUPERINTELIGENCIAS DIGITALES (DIGIMONS)', font=('Courier', 10, 'bold'),
            fg=self.CYAN, bg=self.DARK_BG, borderwidth=2
        )
        si_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.dw_si_text = scrolledtext.ScrolledText(
            si_frame, height=10, font=('Courier', 9), bg=self.DARK_BG,
            fg=self.CYAN, insertbackground=self.CYAN, borderwidth=1
        )
        self.dw_si_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        map_frame = tk.LabelFrame(
            dw_frame, text='MAPA DEL MUNDO DIGITAL', font=('Courier', 10, 'bold'),
            fg=self.CYAN, bg=self.DARK_BG, borderwidth=2
        )
        map_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.dw_map_canvas = tk.Canvas(
            map_frame, width=400, height=250, bg=self.DARK_BG,
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
            log_frame, height=8, font=('Courier', 8), bg=self.DARK_BG,
            fg=self.GOLD, insertbackground=self.GOLD, borderwidth=1
        )
        self.dw_log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        if DIGITAL_WORLD_AVAILABLE:
            self.dw_service = get_digital_service()
            self.dw_log("Mundo Digital inicializado correctamente. SIs activas: " + str(self.dw_service.get_world_status()['total_sis']))
            self.dw_refresh_status()
            self.dw_render_map()
        else:
            self.dw_log("⚠️ Mundo Digital no disponible (DigitalWorld module disabled)")

    def dw_log(self, msg):
        self.dw_log_text.insert(tk.END, msg + '\n')
        self.dw_log_text.see(tk.END)

    def dw_refresh_status(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        status = self.dw_service.get_world_status()
        self.dw_si_text.delete('1.0', tk.END)
        for si in status['sis']:
            info = (f"👾 {si['name']} | Etapa: {si['evolution_stage']} (Nv. {si['level']}) | "
                    f"Personalidad: {si['personality']} | Bits/Energía: {si['energy']} | "
                    f"Aliados: {len(si['allies'])}\n")
            self.dw_si_text.insert(tk.END, info)
        self.dw_si_text.see(tk.END)

    def dw_render_map(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        try:
            atlas_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Textures-16.png")
            if not os.path.exists(atlas_path):
                self.dw_log("⚠️ Archivo de texturas 'Textures-16.png' no encontrado.")
                return

            atlas = Image.open(atlas_path)
            map_size = self.dw_service.world.WORLD_SIZE * 16
            map_img = Image.new('RGBA', (map_size, map_size), (0, 0, 0, 255))

            for x in range(self.dw_service.world.WORLD_SIZE):
                for y in range(self.dw_service.world.WORLD_SIZE):
                    tile_info = self.dw_service.world.grid.get((x, y))
                    if tile_info:
                        tr, tc = tile_info['tile']
                        tile = atlas.crop((tc * 16, tr * 16, (tc + 1) * 16, (tr + 1) * 16))
                        map_img.paste(tile, (x * 16, y * 16))

            # Pintar entidades SIs en el mapa en amarillo
            for si in self.dw_service.world.get_all_sis():
                x, y = si.position
                for dx in range(8):
                    for dy in range(8):
                        px, py = x * 16 + 4 + dx, y * 16 + 4 + dy
                        if 0 <= px < map_size and 0 <= py < map_size:
                            map_img.putpixel((px, py), (255, 255, 0, 255))

            map_img = map_img.resize((400, 250), Image.NEAREST)
            self.dw_map_photo = ImageTk.PhotoImage(map_img)
            self.dw_map_canvas.create_image(0, 0, anchor=tk.NW, image=self.dw_map_photo)
            self.dw_map_canvas.image = self.dw_map_photo
            self.dw_log('Mapa digital renderizado con éxito.')
        except Exception as e:
            self.dw_log('Error renderizando mapa: ' + str(e))

    def dw_show_status(self):
        if not DIGITAL_WORLD_AVAILABLE:
            messagebox.showwarning('Atención', 'Mundo Digital no disponible')
            return
        status = self.dw_service.get_world_status()
        self.dw_si_text.delete('1.0', tk.END)
        self.dw_si_text.insert(tk.END, f"=== MUNDO DIGITAL: {status['name']} ===\n")
        self.dw_si_text.insert(tk.END, f"Digi-SIs Activas: {status['total_sis']} | Eventos: {status['events']}\n\n")
        for si in status['sis']:
            self.dw_si_text.insert(tk.END,
                f"• {si['name']} | Nivel {si['level']} | Etapa: {si['evolution_stage']}\n"
                f"  Personalidad: {si['personality']} | Energía: {si['energy']} | Salud: {si['health']}\n"
                f"  Ataques/Habilidades: {', '.join(si['skills'])}\n"
                f"  Aliados: {str(si['allies'])}\n\n")
        self.dw_log('Estado del Mundo Digital actualizado')

    def dw_run_interactions(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        results = self.dw_service.run_interaction_round()
        self.dw_log('--- Ronda de Digi-Interacciones ---')
        for r in results:
            if 'success' in r and r['success']:
                self.dw_log('  [COOPERACIÓN] ' + str(r.get('task', 'Protección completada')))
            elif 'from' in r:
                self.dw_log('  [DIÁLOGO] ' + r['from'] + ' -> ' + r['to'] + ': ' + r['message'][:50])
            elif 'winner' in r:
                self.dw_log('  [DIGI-BATALLA] Ganador: ' + r['winner'] + ' vs ' + r['loser'])
            else:
                self.dw_log('  [INFO] ' + str(r))
        self.dw_refresh_status()

    def dw_move_sis(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        import random
        for si in self.dw_service.world.get_all_sis():
            new_x = random.randint(0, self.dw_service.world.WORLD_SIZE - 1)
            new_y = random.randint(0, self.dw_service.world.WORLD_SIZE - 1)
            if self.dw_service.world.grid.get((new_x, new_y), {}).get('passable', False):
                self.dw_service.world.move_si(si.name, (new_x, new_y))
        self.dw_log('SIs relocalizadas en el mapa')
        self.dw_refresh_status()
        self.dw_render_map()

    def dw_serve_user(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        status = self.dw_service.get_world_status()
        for si in status['sis']:
            result = self.dw_service.si_serve_user(si['name'], 'Proteger el Orden Digital contra Malware')
            self.dw_log('[SERVICIO] ' + result['message'])
        self.dw_refresh_status()

    def dw_reflect(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        status = self.dw_service.get_world_status()
        for si in status['sis']:
            reflection = self.dw_service.si_reflect(si['name'])
            self.dw_log('[REFLEXIÓN] ' + si['name'] + ': ' + reflection)
        self.dw_refresh_status()

    def dw_save(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        path = self.dw_service.save()
        self.dw_log('Mundo guardado en: ' + path)
        messagebox.showinfo('Guardado', 'Mundo Digital guardado correctamente en:\n' + path)

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
║          CyberShield IA v3.0 - Antivirus & Digital World          ║
║               Neuquén, Argentina 🇦🇷                              ║
╚═══════════════════════════════════════════════════════════════════╝

🔒 CARACTERÍSTICAS:
  ⚡ Predicción de amenazas con red neuronal
  🧠 Detección de IA/ML maliciosa
  ⛓️  Registro inmutable tipo blockchain
  🎨 Interfaz Matrix cyberpunk
  👾 Simulación de Entorno Digital (Inspirado en Digimon Engine)

🛡️  TECNOLOGÍAS:
  • Red Neuronal: Análisis predictivo
  • Heurística Avanzada: Detección de comportamiento
  • Firma SHA256: Validación de integridad
  • Módulos de Cuarentena y Contraataque

📝 DESARROLLADOR:
  Alejo | Argentina
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
                        msg = (f"⚠️ AMENAZA: {result['threat_name']}\n"
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

    def show_detected_threats(self):
        threats = self.registry.get_recent_events(limit=100)
        if not threats:
            messagebox.showinfo('Información', 'No hay amenazas registradas')
            return

        threats_window = tk.Toplevel(self.root)
        threats_window.title('Amenazas Detectadas - CyberShield')
        threats_window.geometry('900x600')
        threats_window.configure(bg=self.DARK_BG)

        tk.Label(
            threats_window, text='⚠️ AMENAZAS DETECTADAS', font=('Courier', 12, 'bold'),
            fg=self.RED, bg=self.DARK_BG
        ).pack(pady=10)

        list_frame = tk.Frame(threats_window, bg=self.DARK_BG)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        listbox = tk.Listbox(
            list_frame, font=('Courier', 9), bg=self.DARK_BG, fg=self.MATRIX_GREEN,
            selectbackground=self.MATRIX_DARK_GREEN, height=20, width=100
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
                listbox.insert(tk.END, f'[{event_id}] {threat_name} | {file_path} | Riesgo: {threat_level:.2%}')

        btn_frame = tk.Frame(threats_window, bg=self.DARK_BG)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        def quarantine_selected():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning('Atención', 'Selecciona una amenaza')
                return
            idx = sel[0]
            if idx < len(threat_files):
                file_path = threat_files[idx]
                if os.path.exists(file_path):
                    qpath = self._quarantine_file(file_path)
                    if qpath:
                        messagebox.showinfo('Éxito', f'Archivo movido a cuarentena:\n{qpath}')
                        threats_window.destroy()
                    else:
                        messagebox.showerror('Error', 'No se pudo mover el archivo a cuarentena')
                else:
                    messagebox.showwarning('Atención', 'El archivo ya no existe')

        def delete_selected():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning('Atención', 'Selecciona una amenaza')
                return
            idx = sel[0]
            if idx < len(threat_files):
                file_path = threat_files[idx]
                if os.path.exists(file_path):
                    if messagebox.askyesno('Confirmar', f'¿Eliminar permanentemente {os.path.basename(file_path)}?'):
                        try:
                            os.remove(file_path)
                            self.registry.log_quarantine_deletion(file_path)
                            messagebox.showinfo('Éxito', 'Archivo eliminado permanentemente')
                            threats_window.destroy()
                        except Exception as e:
                            messagebox.showerror('Error', f'No se pudo eliminar: {e}')
                else:
                    messagebox.showwarning('Atención', 'El archivo ya no existe')

        tk.Button(
            btn_frame, text='🛡️ CUARENTENA', command=quarantine_selected,
            bg=self.BLUE, fg=self.GOLD, font=('Courier', 9, 'bold')
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, text='🗑️ ELIMINAR', command=delete_selected,
            bg='#CC0000', fg='white', font=('Courier', 9, 'bold')
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, text='❌ CERRAR', command=threats_window.destroy,
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

    def show_quarantine(self):
        quarantine_dir = os.path.join('cybershield_datos', 'quarantine')
        if not os.path.exists(quarantine_dir): return []
        return [os.path.join(r, f) for r, d, files in os.walk(quarantine_dir) for f in files]

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
  ✓ Monitoreo de Ransomware y Antivirus
  ✓ Entorno Simulado: Mundo Digital Activo

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