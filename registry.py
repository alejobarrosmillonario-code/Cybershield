"""
Registro blockchain-like de eventos
Historial inmutable de todas las amenazas y defensas
"""

import sqlite3
import hashlib
import json
from datetime import datetime
import os

class BlockchainLikeRegistry:
    """Registro inmutable tipo blockchain"""

    def __init__(self, db_path='cybershield_datos/events.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Inicializa la base de datos"""
        os.makedirs(os.path.dirname(self.db_path) or '.', exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabla principal de eventos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                event_type TEXT,
                threat_level REAL,
                threat_name TEXT,
                file_path TEXT,
                ai_detected BOOLEAN,
                action_taken TEXT,
                previous_hash TEXT,
                current_hash TEXT
            )
        ''')

        # Tabla de ataques detectados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attacks (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                threat_name TEXT,
                file_path TEXT,
                threat_level REAL,
                ai_detected BOOLEAN
            )
        ''')

        # Tabla de defensas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS defenses (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                action TEXT,
                target_file TEXT,
                success BOOLEAN
            )
        ''')

        # Tabla de predicciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                predicted_threat TEXT,
                confidence REAL,
                status TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def calculate_event_hash(self, event_data, previous_hash=''):
        """Calcula hash del evento (blockchain)"""
        event_str = json.dumps(event_data, sort_keys=True)
        combined = previous_hash + event_str
        return hashlib.sha256(combined.encode()).hexdigest()

    def log_event(self, event_type, threat_level=0.0, threat_name='',
                  file_path='', ai_detected=False, action_taken=''):
        """Registra un evento"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()

        # Obtener hash anterior
        cursor.execute('SELECT current_hash FROM events ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        previous_hash = result[0] if result else ''

        # Crear hash del evento
        event_data = {
            'timestamp': timestamp,
            'event_type': event_type,
            'threat_level': threat_level,
            'threat_name': threat_name,
            'file_path': file_path,
            'ai_detected': ai_detected,
        }
        current_hash = self.calculate_event_hash(event_data, previous_hash)

        # Insertar evento
        cursor.execute('''
            INSERT INTO events (timestamp, event_type, threat_level, threat_name,
                              file_path, ai_detected, action_taken, previous_hash,
                              current_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, event_type, threat_level, threat_name, file_path,
              ai_detected, action_taken, previous_hash, current_hash))

        conn.commit()
        conn.close()

    def log_attack(self, threat_name, file_path, threat_level, ai_detected=False):
        """Registra un ataque detectado"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO attacks (timestamp, threat_name, file_path, threat_level, ai_detected)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, threat_name, file_path, threat_level, ai_detected))

        conn.commit()
        conn.close()

        self.log_event('ATTACK_DETECTED', threat_level, threat_name, file_path, ai_detected)

    def log_defense(self, action, target_file, success=True):
        """Registra una acción de defensa"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO defenses (timestamp, action, target_file, success)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, action, target_file, success))

        self.log_event('DEFENSE_EXECUTED', action_taken=action)

        conn.commit()
        conn.close()

    def log_prediction(self, predicted_threat, confidence, status='pending'):
        """Registra una predicción de IA"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO predictions (timestamp, predicted_threat, confidence, status)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, predicted_threat, confidence, status))

        self.log_event('PREDICTION', threat_level=confidence)

        conn.commit()
        conn.close()

    def get_recent_events(self, limit=100):
        """Obtiene eventos recientes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM events ORDER BY id DESC LIMIT ?
        ''', (limit,))

        events = cursor.fetchall()
        conn.close()

        return events

    def get_attack_statistics(self):
        """Obtiene estadísticas de ataques"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM attacks')
        total_attacks = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM attacks WHERE ai_detected = 1')
        ai_attacks = cursor.fetchone()[0]

        cursor.execute('SELECT AVG(threat_level) FROM attacks')
        avg_threat = cursor.fetchone()[0] or 0.0

        conn.close()

        return {
            'total_attacks': total_attacks,
            'ai_threats': ai_attacks,
            'average_threat': avg_threat,
        }

    def verify_blockchain_integrity(self):
        """Verifica la integridad del blockchain"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM events ORDER BY id')
        events = cursor.fetchall()

        previous_hash = ''
        for event in events:
            event_id, timestamp, event_type, threat_level, threat_name, \
            file_path, ai_detected, action_taken, stored_prev_hash, current_hash = event

            # Verificar hash anterior
            if stored_prev_hash != previous_hash:
                conn.close()
                return False, f"Integridad comprometida en evento {event_id}"

            previous_hash = current_hash

        conn.close()
        return True, "Blockchain íntegro"


    # --- Métodos para cuarentena y contraguarda ---
    def log_quarantine(self, file_path, quarantine_path):
        """Registra un archivo en cuarentena"""
        self.log_event('QUARANTINE', action_taken=f'Moved to {quarantine_path}')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO defenses (timestamp, action, target_file, success) VALUES (?, ?, ?, ?)',
                       (datetime.now().isoformat(), 'QUARANTINE', file_path, True))
        conn.commit()
        conn.close()

    def log_quarantine_error(self, file_path, error):
        """Registra error al cuarentenar"""
        self.log_event('QUARANTINE_ERROR', action_taken=f'Error: {error}')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO defenses (timestamp, action, target_file, success) VALUES (?, ?, ?, ?)',
                       (datetime.now().isoformat(), 'QUARANTINE_ERROR', file_path, False))
        conn.commit()
        conn.close()

    def log_quarantine_deletion(self, file_path):
        """Registra eliminación de archivo en cuarentena"""
        self.log_event('QUARANTINE_DELETE', action_taken='Deleted from quarantine')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO defenses (timestamp, action, target_file, success) VALUES (?, ?, ?, ?)',
                       (datetime.now().isoformat(), 'DELETE', file_path, True))
        conn.commit()
        conn.close()

    def log_quarantine_deletion_error(self, file_path, error):
        """Registra error al eliminar de cuarentena"""
        self.log_event('QUARANTINE_DELETE_ERROR', action_taken=f'Error: {error}')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO defenses (timestamp, action, target_file, success) VALUES (?, ?, ?, ?)',
                       (datetime.now().isoformat(), 'DELETE_ERROR', file_path, False))
        conn.commit()
        conn.close()

    def log_counter_attack(self, attacker_info):
        """Registra un contraataque"""
        self.log_event('COUNTER_ATTACK', action_taken=str(attacker_info))
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO defenses (timestamp, action, target_file, success) VALUES (?, ?, ?, ?)',
                       (datetime.now().isoformat(), 'COUNTER_ATTACK', str(attacker_info), True))
        conn.commit()
        conn.close()

    def log_attacker_localized(self, result):
        """Registra localización exitosa de atacante"""
        self.log_event('ATTACKER_LOCALIZED', action_taken=str(result))
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO defenses (timestamp, action, target_file, success) VALUES (?, ?, ?, ?)',
                       (datetime.now().isoformat(), 'LOCALIZED', str(result), True))
        conn.commit()
        conn.close()

    def log_attacker_not_localized(self, result):
        """Registra fallo en localización de atacante"""
        self.log_event('ATTACKER_NOT_LOCALIZED', action_taken=str(result))
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO defenses (timestamp, action, target_file, success) VALUES (?, ?, ?, ?)',
                       (datetime.now().isoformat(), 'NOT_LOCALIZED', str(result), False))
        conn.commit()
        conn.close()
