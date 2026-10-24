"""
CyberShield IA v3.0
Antivirus inteligente con predicción de amenazas
Desarrollado en Neuquén, Argentina
"""

__version__ = '3.0.0'
__author__ = 'Alejo'
__email__ = 'alejobarrosmillonario@gmail.com'
__description__ = 'Antivirus con IA, predicción de amenazas y interfaz Matrix'

from .neural import ThreatPredictor, SimpleNeuralNetwork
from .detector import AdvancedDetector
from .registry import BlockchainLikeRegistry

__all__ = [
    'ThreatPredictor',
    'SimpleNeuralNetwork',
    'AdvancedDetector',
    'BlockchainLikeRegistry',
]
