"""
Red neuronal simple sin dependencias externas
Predice amenazas basándose en patrones de comportamiento
"""

import math
import random

class SimpleNeuralNetwork:
    """Red neuronal de una capa oculta - Predicción de amenazas"""

    def __init__(self, input_size=10, hidden_size=16, output_size=1):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Inicializar pesos aleatoriamente
        self.w1 = [[random.uniform(-0.5, 0.5) for _ in range(input_size)]
                   for _ in range(hidden_size)]
        self.b1 = [random.uniform(-0.5, 0.5) for _ in range(hidden_size)]

        self.w2 = [[random.uniform(-0.5, 0.5) for _ in range(hidden_size)]
                   for _ in range(output_size)]
        self.b2 = [random.uniform(-0.5, 0.5) for _ in range(output_size)]

    def sigmoid(self, x):
        """Función de activación sigmoide"""
        try:
            return 1 / (1 + math.exp(-max(-500, min(500, x))))
        except:
            return 0 if x < 0 else 1

    def relu(self, x):
        """Función de activación ReLU"""
        return max(0, x)

    def forward(self, inputs):
        """Propagación hacia adelante"""
        if len(inputs) != self.input_size:
            inputs = inputs + [0] * (self.input_size - len(inputs))

        # Capa oculta
        hidden = []
        for j in range(self.hidden_size):
            sum_val = self.b1[j]
            for i in range(self.input_size):
                sum_val += inputs[i] * self.w1[j][i]
            hidden.append(self.relu(sum_val))

        # Capa salida
        output = []
        for j in range(self.output_size):
            sum_val = self.b2[j]
            for i in range(self.hidden_size):
                sum_val += hidden[i] * self.w2[j][i]
            output.append(self.sigmoid(sum_val))

        return output[0] if len(output) == 1 else output

    def train(self, inputs, target, learning_rate=0.1):
        """Entrenamiento simple con descenso de gradiente"""
        output = self.forward(inputs)
        error = target - output

        # Ajustar pesos (simplificado para rendimiento)
        for j in range(self.hidden_size):
            self.b1[j] += learning_rate * error * 0.01
            for i in range(self.input_size):
                if i < len(inputs):
                    self.w1[j][i] += learning_rate * error * inputs[i] * 0.01

        for j in range(self.output_size):
            self.b2[j] += learning_rate * error
            for i in range(self.hidden_size):
                self.w2[j][i] += learning_rate * error * 0.01

class ThreatPredictor:
    """Predictor de amenazas - Análisis de patrones"""

    def __init__(self):
        self.nn = SimpleNeuralNetwork(input_size=10, hidden_size=16, output_size=1)
        self.pattern_history = []
        self.threat_patterns = {
            'file_access_speed': 8.5,      # Acceso rápido anormal
            'registry_changes': 7.2,        # Cambios en registro
            'network_anomaly': 8.8,         # Tráfico anormal
            'process_injection': 9.1,       # Inyección de procesos
            'privilege_escalation': 8.9,    # Escalada de privilegios
            'memory_anomaly': 7.8,          # Anomalía de memoria
            'file_encryption': 9.5,         # Encriptación sospechosa
            'ai_behavior': 8.7,             # Comportamiento de IA
        }

    def extract_features(self, file_path, file_size, exec_time,
                        registry_access, network_activity,
                        memory_usage, entropy_score, ai_indicator):
        """Extrae características del archivo para predicción"""
        features = [
            min(file_size / 1024 / 1024, 1.0) if file_size > 0 else 0,  # Tamaño (normalizado)
            min(exec_time, 1.0) if exec_time > 0 else 0,                 # Tiempo de ejecución
            1.0 if registry_access else 0.0,                              # Acceso a registro
            min(network_activity / 100, 1.0) if network_activity > 0 else 0, # Actividad de red
            min(memory_usage / 1000, 1.0) if memory_usage > 0 else 0,    # Uso de memoria
            min(entropy_score / 8.0, 1.0) if entropy_score > 0 else 0,   # Puntuación entropía
            1.0 if ai_indicator else 0.0,                                 # Indicador IA
            1.0 if 'system32' in file_path.lower() else 0.0,             # En carpetas del sistema
            1.0 if any(x in file_path.lower() for x in ['.tmp', 'appdata', 'temp']) else 0.0,
            1.0 if file_path.lower().endswith(('.exe', '.dll', '.scr', '.bat')) else 0.0,
        ]
        return features

    def predict_threat_level(self, file_path, file_size=0, exec_time=0,
                            registry_access=False, network_activity=0,
                            memory_usage=0, entropy_score=0, ai_indicator=False):
        """Predice el nivel de amenaza (0.0 - 1.0)"""
        features = self.extract_features(file_path, file_size, exec_time,
                                        registry_access, network_activity,
                                        memory_usage, entropy_score, ai_indicator)

        threat_score = self.nn.forward(features)
        return threat_score

    def analyze_ai_behavior(self, process_name, memory_pattern, network_pattern,
                           learning_rate, adaptation_speed):
        """Detecta comportamiento típico de IA maliciosa"""
        ai_score = 0.0

        # Patrones típicos de IA/ML
        if learning_rate > 0.1:
            ai_score += 0.3
        if adaptation_speed > 100:
            ai_score += 0.25
        if 'python' in process_name.lower() or 'tensorflow' in process_name.lower():
            ai_score += 0.2
        if memory_pattern == 'oscillating':
            ai_score += 0.25
        if network_pattern == 'distributed':
            ai_score += 0.3

        return min(ai_score, 1.0)

    def train_on_samples(self, samples):
        """Entrena la red con muestras históricas"""
        for sample in samples:
            features = sample['features']
            label = sample['is_threat']
            self.nn.train(features, label, learning_rate=0.05)
