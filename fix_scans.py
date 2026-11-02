#!/usr/bin/env python3
# Corrección de main.pyw - escaneo funcional + cuarentena + contraguarda
import os

filepath = "main.pyw"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. quick_scan: agregar scanned_count
old1 = """        self.cancel_flag = False
        self.scan_text.delete('1.0', tk.END)
        self.scan_text.insert(tk.END, '[*] Iniciando escaneo rápido..."""
new1 = """        self.cancel_flag = False
        self.scanned_count = 0
        self.scan_text.delete('1.0', tk.END)
        self.scan_text.insert(tk.END, '[*] Iniciando escaneo rápido..."""
if old1 in content:
    content = content.replace(old1, new1, 1)
    print("1. quick_scan: scanned_count añadido")
else:
    print("1. quick_scan: NO encontrado")

# 2. full_scan: agregar contadores y total_files
old2 = """        self.cancel_flag = False
        self.scan_text.delete('1.0', tk.END)
        self.scan_text.insert(tk.END, '[*] Iniciando escaneo completo..."""
new2 = """        self.cancel_flag = False
        self.scanned_count = 0
        self.total_files = 0
        self.scan_text.delete('1.0', tk.END)
        self.scan_text.insert(tk.END, '[*] Iniciando escaneo completo..."""
if old2 in content:
    content = content.replace(old2, new2, 1)
    print("2. full_scan: contadores añadidos")
else:
    print("2. full_scan: NO encontrado")

# 3. Reemplazar _quick_scan_worker (con scanned_count y progreso)
old_worker = '''    def _quick_scan_worker(self):
        """Worker de escaneo rápido"""
        quick_paths = [
            os.path.expandvars(r'%APPDATA%'),
            os.path.expandvars(r'%LOCALAPPDATA%\\Temp'),
            os.path.expandvars(r'%SystemRoot%\\Temp'),
        ]

        threats_found = 0

        for path in quick_paths:
            if self.cancel_flag:
                break
            if os.path.exists(path):
                self.scan_text.insert(tk.END, f'[>] Escaneando: {path}\\n')
                self.scan_text.see(tk.END)
                self.root.update()

                try:
                    for root, dirs, files in os.walk(path):
                        if self.cancel_flag:
                            break
                        for file in files:
                            if self.cancel_flag:
                                break
                            file_path = os.path.join(root, file)
                            result = self.detector.analyze_file(file_path)

                            if result['is_threat']:
                                threats_found += 1
                                self.scan_text.insert(
                                    tk.END,
                                    f"⚠️  AMENAZA: {result['threat_name']}\\n"
                                    f"   Archivo: {file_path}\\n"
                                    f"   Riesgo: {result['threat_level']:.2%}\\n"
                                    f"   IA: {'Sí' if result['ai_detected'] else 'No'}\\n\\n",
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
                    self.scan_text.insert(tk.END, f'[!] Error: {e}\\n')

        self.scan_text.insert(
            tk.END,
            f'\\n[✓] Escaneo completado. Amenazas encontradas: {threats_found}\\n',
            'complete'
        )
        self.scan_text.see(tk.END)
        self.root.after(0, self._scan_finished)'''

new_worker = '''    def _quick_scan_worker(self):
        """Worker de escaneo rápido"""
        self.total_files = 0
        # Contar archivos totales para mostrar progreso
        try:
            for root, dirs, files in os.walk('C:\\'):
                self.total_files += len(files)
        except Exception as e:
            self._progress(f'[!] Error contando archivos: {e}\\n')
            self.total_files = 1

        threats_found = 0

        for path in ['%APPDATA%', '%LOCALAPPDATA%\\Temp', '%SystemRoot%\\Temp']:
            if self.cancel_flag:
                break
            path = os.path.expandvars(path)
            if os.path.exists(path):
                try:
                    for root, dirs, files in os.walk(path):
                        if self.cancel_flag:
                            break
                        for file in files:
                            if self.cancel_flag:
                                break
                            file_path = os.path.join(root, file)
                            result = self.detector.analyze_file(file_path)

                            if result['is_threat']:
                                threats_found += 1
                                self.scan_text.insert(
                                    tk.END,
                                    f"⚠️  AMENAZA: {result['threat_name']}\\n"
                                    f"   Archivo: {file_path}\\n"
                                    f"   Riesgo: {result['threat_level']:.2%}\\n"
                                    f"   IA: {'Sí' if result['ai_detected'] else 'No'}\\n\\n",
                                    'threat'
                                )
                                self.registry.log_attack(
                                    result['threat_name'],
                                    file_path,
                                    result['threat_level'],
                                    result['ai_detected']
                                )

                            self.scanned_count += 1
                            # Actualizar progreso cada 50 archivos o al final
                            if self.scanned_count % 50 == 0 or self.scanned_count == self.total_files:
                                pct = (self.scanned_count / self.total_files * 100) if self.total_files > 0 else 0
                                self._progress(
                                    f'[=] {path} | {self.scanned_count}/{self.total_files} archivos ({pct:.1f}%) | cancelado={self.cancel_flag}\\n'
                                )
                except Exception as e:
                    self._progress(f'[!] Error en {path}: {e}\\n')

        self._progress(
            f'\\n[✓] Escaneo completado. Archivos analizados: {self.scanned_count} | Amenazas: {threats_found}\\n'
        )
        self.scan_text.see(tk.END)
        self.root.after(0, self._scan_finished)'''

if old_worker in content:
    content = content.replace(old_worker, new_worker, 1)
    print("3. _quick_scan_worker corregido correctamente")
else:
    print("3. _quick_scan_worker: NO encontrado")
    # Buscar y mostrar las primeras líneas
    idx = content.find("    def _quick_scan_worker(self):")
    if idx != -1:
        print(repr(content[idx:idx+400]))

# Guardar
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# Verificar
with open(filepath, 'r', encoding='utf-8') as f:
    content2 = f.read()

idx = content2.find("    def quick_scan(self):")
block = content2[idx:idx+700]
print(f"\n=== Verificación quick_scan ===")
print(f"scanned_count = 0: {'self.scanned_count = 0' in block}")

idx2 = content2.find("    def full_scan(self):")
block2 = content2[idx2:idx2+800]
print(f"total_files = 0: {'self.total_files = 0' in block2}")
print(f"scanned_count = 0: {'self.scanned_count = 0' in block2}")

print(f"Archivo guardado: {len(content2)} bytes")
