"""
Detector avanzado de amenazas con IA
Análisis heurístico + predicción con red neuronal
"""

import os
import hashlib
from datetime import datetime

class AdvancedDetector:
    """Detector mejorado con IA"""

    def __init__(self, predictor):
        self.predictor = predictor
        self.malware_signatures = {
            # Firmas clásicas (hash)
            'd41d8cd98f00b204e9800998ecf8427e': 'TROJAN.Win32.Generic',
            'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855': 'WORM.Conficker',

            # Patrones de código
            'rundll32': 'Potencial ejecución maliciosa',
            'powershell -encodedcommand': 'Script ofuscado detectado',
            'cmd /c echo': 'Comando sospechoso',
        }

        self.suspicious_extensions = {
            '.exe': 'Ejecutable',
            '.dll': 'Librería',
            '.scr': 'Protector pantalla',
            '.bat': 'Script batch',
            '.cmd': 'Comando',
            '.vbs': 'VBScript',
            '.js': 'JavaScript',
            '.jar': 'Java archive',
            '.enc': 'Encriptado (Ransomware)',
            '.locked': 'Bloqueado (Ransomware)',
            '.cry': 'Encriptado (Ransomware)',
        }

        self.suspicious_paths = [
            'appdata\\roaming',
            'appdata\\local\\temp',
            'windows\\temp',
            'windows\\system32\\drivers\\etc',
            'users\\public',
        ]

        self.risky_apis = [
            'VirtualAlloc',
            'WriteProcessMemory',
            'CreateRemoteThread',
            'SetWindowsHookEx',
            'RegSetValue',
            'URLDownloadToFile',
        ]

    def calculate_entropy(self, data):
        """Calcula entropía de Shannon (0-8)"""
        if not data:
            return 0

        frequency = {}
        for byte in data:
            frequency[byte] = frequency.get(byte, 0) + 1

        entropy = 0
        data_len = len(data)
        for count in frequency.values():
            p = count / data_len
            entropy -= p * (p and math.log2(p) or 0)

        return entropy

    def check_signature(self, file_path):
        """Verifica firmas de malware conocido"""
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()

                for sig_hash, threat_name in self.malware_signatures.items():
                    if sig_hash == file_hash:
                        return True, threat_name, 0.95
        except:
            pass

        return False, None, 0.0

    def check_heuristics(self, file_path):
        """Análisis heurístico"""
        risk_score = 0.0
        detections = []

        file_name = os.path.basename(file_path).lower()
        file_ext = os.path.splitext(file_name)[1].lower()

        # Extensión sospechosa
        if file_ext in self.suspicious_extensions:
            risk_score += 0.15
            detections.append(f"Extensión sospechosa: {file_ext}")

        # Ruta sospechosa
        path_lower = file_path.lower()
        for susp_path in self.suspicious_paths:
            if susp_path in path_lower:
                risk_score += 0.2
                detections.append(f"Ruta sospechosa: {susp_path}")
                break

        # Nombre ofuscado
        if any(char in file_name for char in ['$', '~', '!', '@']):
            risk_score += 0.1
            detections.append("Nombre ofuscado detectado")

        # Tamaño anormal
        try:
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                risk_score += 0.05
                detections.append("Archivo vacío (sospechoso)")
            elif file_size > 500 * 1024 * 1024:  # >500MB
                risk_score += 0.1
                detections.append("Archivo muy grande")
        except:
            pass

        return min(risk_score, 1.0), detections

    def analyze_file(self, file_path):
        """Análisis completo de archivo"""
        result = {
            'file': file_path,
            'timestamp': datetime.now().isoformat(),
            'is_threat': False,
            'threat_name': 'Clean',
            'threat_level': 0.0,
            'detections': [],
            'ai_detected': False,
        }

        # Verificar firma conocida
        is_known_threat, threat_name, sig_score = self.check_signature(file_path)
        if is_known_threat:
            result['is_threat'] = True
            result['threat_name'] = threat_name
            result['threat_level'] = sig_score
            result['detections'].append(f"Firma conocida: {threat_name}")
            return result

        # Análisis heurístico
        heuristic_score, heuristics = self.check_heuristics(file_path)
        result['detections'].extend(heuristics)

        # Predicción con IA
        try:
            file_size = os.path.getsize(file_path)
            entropy = self.calculate_entropy(open(file_path, 'rb').read(8192))
        except:
            file_size = 0
            entropy = 0

        ai_prediction = self.predictor.predict_threat_level(
            file_path=file_path,
            file_size=file_size,
            entropy_score=entropy
        )

        # Detectar comportamiento de IA maliciosa
        ai_behavior_score = 0.0
        if 'python' in file_path.lower() or 'model' in file_path.lower():
            ai_behavior_score = self.predictor.analyze_ai_behavior(
                process_name=os.path.basename(file_path),
                memory_pattern='normal',
                network_pattern='normal',
                learning_rate=0.0,
                adaptation_speed=0.0
            )
            if ai_behavior_score > 0.5:
                result['ai_detected'] = True
                result['detections'].append("Comportamiento de IA detectado")

        # Score final
        final_score = max(heuristic_score, ai_prediction, ai_behavior_score)
        result['threat_level'] = final_score

        if final_score > 0.6:
            result['is_threat'] = True
            if final_score > 0.8:
                result['threat_name'] = 'THREAT.IA.Predictive'
            else:
                result['threat_name'] = 'SUSPICIOUS.Heuristic'

        return result

import math
