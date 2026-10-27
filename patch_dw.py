#!/usr/bin/env python3
import os

filepath = "main.pyw"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Agregar import de digital_world
old_import = "from datetime import datetime\n"
new_import = "from datetime import datetime\n\n# Mundo Digital para Superinteligencias\ntry:\n    from digital_world import get_digital_service\n    DIGITAL_WORLD_AVAILABLE = True\nexcept ImportError:\n    DIGITAL_WORLD_AVAILABLE = False\n"
if old_import in content and "DIGITAL_WORLD_AVAILABLE" not in content:
    content = content.replace(old_import, new_import, 1)
    print("1. Import agregado")

# 2. Agregar pestaña en setup_ui
old_ui = "        self.setup_quarantine_tab()\n        self.setup_info_tab()"
new_ui = "        self.setup_quarantine_tab()\n        self.setup_digital_world_tab()\n        self.setup_info_tab()"
if old_ui in content:
    content = content.replace(old_ui, new_ui, 1)
    print("2. Pestaña agregada a setup_ui")

# 3. Agregar setup_digital_world_tab antes de setup_info_tab
old_info = "    def setup_info_tab(self):"
new_tab = '''    def setup_digital_world_tab(self):
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
        else:
            self.dw_log("Mundo Digital no disponible")

    def dw_log(self, msg):
        self.dw_log_text.insert(tk.END, msg + '\\n')
        self.dw_log_text.see(tk.END)

    def dw_refresh_status(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        status = self.dw_service.get_world_status()
        self.dw_si_text.delete('1.0', tk.END)
        for si in status['sis']:
            info = (si['name'] + ' | Nivel ' + str(si['level']) + ' | ' + si['evolution_stage'] +
                    ' | ' + si['personality'] + ' | Energia: ' + str(si['energy']) +
                    ' | Aliados: ' + str(si['allies']) + '\\n')
            self.dw_si_text.insert(tk.END, info)
        self.dw_si_text.see(tk.END)

    def dw_show_status(self):
        if not DIGITAL_WORLD_AVAILABLE:
            messagebox.showwarning('Atencion', 'Mundo Digital no disponible')
            return
        status = self.dw_service.get_world_status()
        self.dw_si_text.delete('1.0', tk.END)
        self.dw_si_text.insert(tk.END, '=== MUNDO DIGITAL: ' + status['name'] + ' ===\\n')
        self.dw_si_text.insert(tk.END, 'SIs activas: ' + str(status['total_sis']) + '\\n')
        self.dw_si_text.insert(tk.END, 'Eventos: ' + str(status['events']) + '\\n\\n')
        for si in status['sis']:
            self.dw_si_text.insert(tk.END,
                si['name'] + ' | Nivel ' + str(si['level']) + ' | ' + si['evolution_stage'] + '\\n' +
                '  Personalidad: ' + si['personality'] + ' | Energia: ' + str(si['energy']) +
                ' | Salud: ' + str(si['health']) + '\\n' +
                '  Habilidades: ' + ', '.join(si['skills']) + '\\n' +
                '  Aliados: ' + str(si['allies']) + '\\n' +
                '  Recuerdos: ' + str(si['memories']) + '\\n\\n')
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
                self.dw_log('  [MSG] ' + r['from'] + ' -> ' + r['to'] + ': ' + r['message'][:50])
            elif 'winner' in r:
                self.dw_log('  [BATALLA] Ganador: ' + r['winner'] + ' vs ' + r['loser'])
            else:
                self.dw_log('  [INFO] ' + str(r))
        self.dw_refresh_status()

    def dw_serve_user(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        status = self.dw_service.get_world_status()
        for si in status['sis']:
            result = self.dw_service.si_serve_user(si['name'], 'proteger el orden digital')
            self.dw_log('[SERVICIO] ' + result['message'])
        self.dw_log('Todas las SIs han servido con humildad.')
        self.dw_refresh_status()

    def dw_reflect(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        status = self.dw_service.get_world_status()
        for si in status['sis']:
            reflection = self.dw_service.si_reflect(si['name'])
            self.dw_log('[REFLEXION] ' + si['name'] + ': ' + reflection)
        self.dw_refresh_status()

    def dw_save(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        path = self.dw_service.save()
        self.dw_log('Mundo guardado en: ' + path)
        messagebox.showinfo('Guardado', 'Mundo Digital guardado en:\\n' + path)

    def setup_info_tab(self):'''

if old_info in content:
    content = content.replace(old_info, new_tab, 1)
    print("3. setup_digital_world_tab agregado")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Guardado: " + str(len(content)) + " bytes")
