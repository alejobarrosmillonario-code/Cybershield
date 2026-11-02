#!/usr/bin/env python3
import os

filepath = "main.pyw"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Agregar pestaña de cuarentena en setup_ui
old_ui = "        self.setup_registry_tab()\n        self.setup_info_tab()"
new_ui = "        self.setup_registry_tab()\n        self.setup_quarantine_tab()\n        self.setup_info_tab()"
if old_ui in content:
    content = content.replace(old_ui, new_ui, 1)
    print("1. Pestaña cuarentena agregada a setup_ui")

# 2. Agregar setup_quarantine_tab antes de setup_predictor_tab
old_scan = "    def setup_predictor_tab(self):"
new_tab = '''    def setup_quarantine_tab(self):
        quarantine_frame = tk.Frame(self.notebook, bg=self.DARK_BG)
        self.notebook.add(quarantine_frame, text='[CUARENTENA]')

        options_frame = tk.LabelFrame(
            quarantine_frame, text='\\u1f6e1  OPCIONES DE CUARENTENA', font=('Courier', 10, 'bold'),
            fg=self.GOLD, bg=self.DARK_BG, borderwidth=2
        )
        options_frame.pack(fill=tk.X, padx=10, pady=10)

        button_frame = tk.Frame(options_frame, bg=self.DARK_BG)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.refresh_quarantine_btn = tk.Button(
            button_frame, text='\\u1f504 ACTUALIZAR LISTA', command=self.refresh_quarantine_list,
            bg=self.MATRIX_DARK_GREEN, fg=self.MATRIX_GREEN, font=('Courier', 9, 'bold')
        )
        self.refresh_quarantine_btn.pack(side=tk.LEFT, padx=5)

        self.delete_selected_btn = tk.Button(
            button_frame, text='\\u1f5d1 ELIMINAR SELECCIONADO', command=self.delete_selected_quarantine,
            bg='#CC0000', fg='white', font=('Courier', 9, 'bold')
        )
        self.delete_selected_btn.pack(side=tk.LEFT, padx=5)

        self.delete_all_btn = tk.Button(
            button_frame, text='\\u1f5d1 ELIMINAR TODO', command=self.delete_all_quarantine,
            bg='#AA0000', fg='white', font=('Courier', 9, 'bold')
        )
        self.delete_all_btn.pack(side=tk.LEFT, padx=5)

        self.quarantine_count_label = tk.Label(
            button_frame, text='Archivos en cuarentena: 0', font=('Courier', 9),
            fg=self.CYAN, bg=self.DARK_BG
        )
        self.quarantine_count_label.pack(side=tk.RIGHT, padx=10)

        list_frame = tk.LabelFrame(
            quarantine_frame, text='\\u1f4cb ARCHIVOS EN CUARENTENA', font=('Courier', 10, 'bold'),
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
            quarantine_frame, text='\\u1f4dd REGISTRO DE CUARENTENA', font=('Courier', 10, 'bold'),
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
        self.quarantine_log.insert(tk.END, '[+] Lista actualizada: ' + str(len(files)) + ' archivos\\n')
        self.quarantine_log.see(tk.END)

    def delete_selected_quarantine(self):
        selection = self.quarantine_listbox.curselection()
        if not selection:
            messagebox.showwarning('Atencion', 'Selecciona un archivo para eliminar')
            return
        idx = selection[0]
        files = self.show_quarantine()
        if idx < len(files):
            file_path = files[idx]
            if messagebox.askyesno('Confirmar', 'Eliminar permanentemente ' + os.path.basename(file_path) + '?'):
                if self.delete_quarantine(file_path):
                    self.quarantine_log.insert(tk.END, '[OK] Eliminado: ' + os.path.basename(file_path) + '\\n')
                    self.refresh_quarantine_list()
                else:
                    self.quarantine_log.insert(tk.END, '[X] Error al eliminar: ' + os.path.basename(file_path) + '\\n')
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
            self.quarantine_log.insert(tk.END, '[OK] Eliminados ' + str(deleted) + '/' + str(len(files)) + ' archivos\\n')
            self.refresh_quarantine_list()
        self.quarantine_log.see(tk.END)

    def setup_predictor_tab(self):'''

if old_scan in content:
    content = content.replace(old_scan, new_tab, 1)
    print("2. setup_quarantine_tab agregado")

# 3. Agregar boton de cuarentena en scan tab
old_cancel = "        self.cancel_btn.pack(side=tk.LEFT, padx=5)\n\n        results_frame"
new_cancel = """        self.cancel_btn.pack(side=tk.LEFT, padx=5)

        self.quarantine_btn = tk.Button(
            button_frame, text='\\u1f6e1 CUARENTENA', command=self.show_detected_threats,
            bg=self.BLUE, fg=self.GOLD, font=('Courier', 9, 'bold')
        )
        self.quarantine_btn.pack(side=tk.LEFT, padx=5)

        results_frame"""
if old_cancel in content:
    content = content.replace(old_cancel, new_cancel, 1)
    print("3. Boton cuarentena en scan tab")

# 4. Agregar show_detected_threats antes de _quarantine_file
old_q = "    def _quarantine_file(self, file_path):"
new_method = '''    def show_detected_threats(self):
        threats = self.registry.get_recent_events(limit=100)
        if not threats:
            messagebox.showinfo('Informacion', 'No hay amenazas registradas')
            return

        threats_window = tk.Toplevel(self.root)
        threats_window.title('Amenazas Detectadas - CyberShield')
        threats_window.geometry('900x600')
        threats_window.configure(bg=self.DARK_BG)

        tk.Label(
            threats_window, text='\\u26a0  AMENAZAS DETECTADAS', font=('Courier', 12, 'bold'),
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
                listbox.insert(tk.END, '[' + str(event_id) + '] ' + str(threat_name) + ' | ' + str(file_path) + ' | Riesgo: ' + format(threat_level, '.2%'))

        btn_frame = tk.Frame(threats_window, bg=self.DARK_BG)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        def quarantine_selected():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning('Atencion', 'Selecciona una amenaza')
                return
            idx = sel[0]
            if idx < len(threat_files):
                file_path = threat_files[idx]
                if os.path.exists(file_path):
                    qpath = self._quarantine_file(file_path)
                    if qpath:
                        messagebox.showinfo('Exito', 'Archivo movido a cuarentena:\\n' + qpath)
                        threats_window.destroy()
                    else:
                        messagebox.showerror('Error', 'No se pudo cuarentenar el archivo')
                else:
                    messagebox.showwarning('Atencion', 'El archivo ya no existe')

        def delete_selected():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning('Atencion', 'Selecciona una amenaza')
                return
            idx = sel[0]
            if idx < len(threat_files):
                file_path = threat_files[idx]
                if os.path.exists(file_path):
                    if messagebox.askyesno('Confirmar', 'Eliminar permanentemente ' + os.path.basename(file_path) + '?'):
                        try:
                            os.remove(file_path)
                            self.registry.log_quarantine_deletion(file_path)
                            messagebox.showinfo('Exito', 'Archivo eliminado permanentemente')
                            threats_window.destroy()
                        except Exception as e:
                            messagebox.showerror('Error', 'No se pudo eliminar: ' + str(e))
                else:
                    messagebox.showwarning('Atencion', 'El archivo ya no existe')

        tk.Button(
            btn_frame, text='\\u1f6e1 CUARENTENA', command=quarantine_selected,
            bg=self.BLUE, fg=self.GOLD, font=('Courier', 9, 'bold')
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, text='\\u1f5d1 ELIMINAR', command=delete_selected,
            bg='#CC0000', fg='white', font=('Courier', 9, 'bold')
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame, text='\\u274c CERRAR', command=threats_window.destroy,
            bg=self.MATRIX_DARK_GREEN, fg=self.MATRIX_GREEN, font=('Courier', 9, 'bold')
        ).pack(side=tk.RIGHT, padx=5)

    def _quarantine_file(self, file_path):'''

if old_q in content:
    content = content.replace(old_q, new_method, 1)
    print("4. show_detected_threats agregado")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Guardado: " + str(len(content)) + " bytes")
