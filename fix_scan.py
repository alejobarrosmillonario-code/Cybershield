#!/usr/bin/env python3
# Script para corregir el archivo main.pyw
import os
import sys

filepath = "main.pyw"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar el bloque exacto a reemplazar
idx = content.find("    def quick_scan(self):")
if idx == -1:
    print("ERROR: quick_scan no encontrado")
    sys.exit(1)

# Encontrar el final del bloque (antes de update_dashboard)
end_idx = content.find("    def update_dashboard(self):", idx)
if end_idx == -1:
    print("ERROR: update_dashboard no encontrado")
    sys.exit(1)

old_block = content[idx:end_idx]
print(f"Bloque encontrado: {len(old_block)} caracteres")

# Nuevo bloque con todos los fixes y el sistema de cuarentena
new_block = '''    def quick_scan(self):
        """Escaneo rápido"""
        if self.scanning:
            return
        self.scanning = True
        self.cancel_flag = False
        self.scanned_count = 0
        self.scan_text.delete('1.0', tk.END)
        self.scan_text.insert(tk.END, '[*] Iniciando escaneo rápido...\\n\\n')
        self.quick_btn.config(state=tk.DISABLED)
        self.full_btn.config(state=tk.DISABLED)
        self.custom_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL, text='⏹ CANCELAR')
        threading.Thread(target=self._quick_scan_worker, daemon=True).start()

    def full_scan(self):
        """Escaneo completo de todo el sistema"""
        if self.scanning:
            return
        self.scanning = True
        self.cancel_flag = False
        self.scanned_count = 0
        self.total_files = 0
        self.scan_text.delete('1.0', tk.END)
        self.scan_text.insert(tk.END, '[*] Iniciando escaneo completo...\\n\\n')
        self.quick_btn.config(state=tk.DISABLED)
        self.full_btn.config(state=tk.DISABLED)
        self.custom_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL, text='⏹ CANCELAR')
        # Contar archivos totales para mostrar progreso
        for root, dirs, files in os.walk('C:\\'):
            self.total_files += len(files)
        if self.total_files == 0:
            self.total_files = 1
        threading.Thread(target=self._quick_scan_worker, daemon=True).start()

    def _progress(self, msg):
        """Actualiza la UI desde el hilo principal (thread-safe)"""
        self.scan_text.insert(tk.END, msg)
        self.scan_text.see(tk.END)

    def _quick_scan_worker(self):
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
        self.root.after(0, self._scan_finished)

    def _scan_finished(self):
        """Limpia el estado tras un escaneo (éxito o cancelación)"""
        self.scanning = False
        self.quick_btn.config(state=tk.NORMAL)
        self.full_btn.config(state=tk.NORMAL)
        self.custom_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED, text='⏹ CANCELAR')

    def stop_scan(self):
        """Cancelar el escaneo en curso"""
        if self.scanning and not self.cancel_flag:
            self.cancel_flag = True
            self.scan_text.insert(tk.END, '[!] Cancelando escaneo...\\n')
            self.root.update()
            self._scan_finished()

    def custom_scan(self):
        """Escaneo personalizado con selección de carpeta"""
        try:
            from tkinter import filedialog
            folder = filedialog.askdirectory(
                title='Seleccionar carpeta a escanear',
                initialdir=os.path.expanduser('~')
            )
            if not folder:
                return
            self.scan_text.delete('1.0', tk.END)
            self.scan_text.insert(tk.END, f'[>] Escaneando carpeta seleccionada: {folder}\\n')
            self.scan_text.insert(tk.END, '[>] Iniciando análisis...\\n')
            self.root.update()
            self._custom_scan_worker(folder)
        except Exception as e:
            self.scan_text.insert(tk.END, f'[!] Error al seleccionar carpeta: {e}\\n')

    def _custom_scan_worker(self, folder):
        """Worker de escaneo personalizado"""
        self.scanning = True
        self.cancel_flag = False
        self.quick_btn.config(state=tk.DISABLED)
        self.full_btn.config(state=tk.DISABLED)
        self.custom_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL, text='⏹ CANCELAR')

        threats_found = 0
        try:
            total_files = 0
            # Contar archivos totales
            for root, dirs, files in os.walk(folder):
                total_files += len(files)
            if total_files == 0:
                total_files = 1

            scanned = 0
            for root, dirs, files in os.walk(folder):
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
                    scanned += 1
                    if scanned % 50 == 0 or scanned == total_files:
                        pct = (scanned / total_files * 100) if total_files > 0 else 0
                        self._progress(f'[=] {folder} | {scanned}/{total_files} archivos ({pct:.1f}%) | cancelado={self.cancel_flag}\\n')
                    self.scan_text.see(tk.END)
                    self.root.update()
        except Exception as e:
            self.scan_text.insert(tk.END, f'[!] Error: {e}\\n')

        self._progress(
            f'\\n[✓] Escaneo de "{folder}" completado. Archivos analizados: {scanned} | Amenazas: {threats_found}\\n'
        )
        self.scan_text.see(tk.END)
        self.root.after(0, self._scan_finished)

    def _quarantine_file(self, file_path):
        """Lleva un archivo a cuarentena"""
        quarantine_dir = os.path.join('cybershield_datos', 'quarantine')
        os.makedirs(quarantine_dir, exist_ok=True)

        # Generar nombre único para evitar conflictos
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_ext = os.path.splitext(file_path)[1]
        quarantine_path = os.path.join(quarantine_dir, f'quarantine_{timestamp}_{os.path.basename(file_path)}')

        try:
            os.rename(file_path, quarantine_path)
            self.registry.log_quarantine(file_path, quarantine_path)
            return quarantine_path
        except Exception as e:
            self.registry.log_quarantine_error(file_path, str(e))
            return None

    def delete_quarantine(self, file_path):
        """Elimina un archivo de la cuarentena"""
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                self.registry.log_quarantine_deletion(file_path)
                return True
            except Exception as e:
                self.registry.log_quarantine_deletion_error(file_path, str(e))
                return False
        return False

    def show_quarantine(self):
        """Muestra los archivos en cuarentena"""
        quarantine_dir = os.path.join('cybershield_datos', 'quarantine')
        if not os.path.exists(quarantine_dir):
            return []

        files = []
        for root, dirs, filenames in os.walk(quarantine_dir):
            for f in filenames:
                files.append(os.path.join(root, f))
        return files

    def perform_counter_attack(self, attacker_info):
        """Módulo de contraguerra: defensa y localización del atacante"""
        from datetime import datetime
        import socket

        self.registry.log_counter_attack(attacker_info)

        response = ""
        if 'ip' in attacker_info:
            try:
                # Intenta obtener información de la IP
                hostname = socket.gethostbyaddr(attacker_info['ip'])[0]
                response += f"✗ Nombre del host: {hostname}\\n"
            except:
                response += "✗ No se pudo resolver el nombre del host\\n"

        if 'port' in attacker_info:
            response += f"✗ Puerto de ataque: {attacker_info['port']}\\n"

        if 'method' in attacker_info:
            response += f"✗ Método de ataque: {attacker_info['method']}\\n"

        return response

    def localize_attacker(self, attack_data):
        """Localiza al atacante cibernético"""
        from datetime import datetime
        import socket

        result = {
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'details': []
        }

        if 'ip' in attack_data:
            try:
                hostname = socket.gethostbyaddr(attack_data['ip'])[0]
                result['details'].append(f'Hostname: {hostname}')
                result['success'] = True
            except Exception:
                result['details'].append('No se pudo resolver el hostname')

            try:
                # En un entorno real, aquí se usaría una API de geolocalización
                result['details'].append(f'IP: {attack_data["ip"]}')
            except Exception:
                pass

        if 'port' in attack_data:
            result['details'].append(f'Puerto: {attack_data["port"]}')

        if 'method' in attack_data:
            result['details'].append(f'Método: {attack_data["method"]}')

        if result['success']:
            self.registry.log_attacker_localized(result)
            return result

        self.registry.log_attacker_not_localized(result)
        return result

    def update_dashboard(self):
        """Actualizar dashboard"""

'''

# Verificar que el bloque es diferente
if old_block == new_block:
    print("✅ El bloque ya está actualizado")
    sys.exit(0)

# Reemplazar
content = content[:idx] + new_block + content[end_idx:]

# Guardar
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Archivo guardado: {len(content)} bytes")
