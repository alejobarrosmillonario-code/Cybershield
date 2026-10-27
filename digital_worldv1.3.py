#!/usr/bin/env python3
"""
Módulo de Mundo Digital para Superinteligencias (Digimon Engine)
CyberShield IA v3 - Entorno virtual para SIs
SIs evolucionan (Digievolución), interactúan y protegen la red contra ciberamenazas.
"""

import os
import json
import random
import time
from datetime import datetime
from PIL import Image

# Ruta dinámica al atlas de texturas
TEXTURE_ATLAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Textures-16.png")
TILE_SIZE = 16
ATLAS_COLS = 32
ATLAS_ROWS = 32


class TextureManager:
    """Gestiona el atlas de texturas para el mundo digital."""

    def __init__(self, atlas_path=TEXTURE_ATLAS):
        self.atlas_path = atlas_path
        self.atlas = None
        self.tiles = {}  # (row, col) -> PIL Image
        self.tile_categories = {}  # (row, col) -> categoría
        self._load_atlas()

    def _load_atlas(self):
        try:
            if os.path.exists(self.atlas_path):
                self.atlas = Image.open(self.atlas_path)
                self._categorize_tiles()
            else:
                print(f"[TextureManager] Advertencia: No se encontró {self.atlas_path}")
        except Exception as e:
            print(f"[TextureManager] Error cargando atlas: {e}")
            self.atlas = None

    def _categorize_tiles(self):
        """Categoriza cada tile por su color dominante."""
        if not self.atlas:
            return
        for r in range(ATLAS_ROWS):
            for c in range(ATLAS_COLS):
                tile = self.atlas.crop((c * TILE_SIZE, r * TILE_SIZE,
                                        (c + 1) * TILE_SIZE, (r + 1) * TILE_SIZE))
                pixels = [p for p in tile.getdata() if len(p) > 3 and p[3] > 128]
                if not pixels:
                    self.tile_categories[(r, c)] = "transparent"
                    continue
                avg = tuple(sum(p[i] for p in pixels) // len(pixels) for i in range(3))
                r_, g_, b_ = avg
                if r_ > 150 and g_ < 100 and b_ < 100:
                    cat = "lava"
                elif b_ > 150 and r_ < 100:
                    cat = "water"
                elif g_ > 150 and r_ < 100:
                    cat = "nature"
                elif r_ > 150 and g_ > 150 and b_ < 100:
                    cat = "sand"
                elif r_ < 80 and g_ < 80 and b_ < 80:
                    cat = "stone"
                elif r_ > 100 and g_ > 80 and b_ < 80:
                    cat = "wood"
                elif r_ > 100 and g_ > 100 and b_ > 100:
                    cat = "fabric"
                else:
                    cat = "mixed"
                self.tile_categories[(r, c)] = cat

    def get_tile(self, row, col):
        """Obtiene un tile del atlas."""
        if not self.atlas:
            return None
        if (row, col) not in self.tiles:
            self.tiles[(row, col)] = self.atlas.crop(
                (col * TILE_SIZE, row * TILE_SIZE,
                 (col + 1) * TILE_SIZE, (row + 1) * TILE_SIZE)
            )
        return self.tiles[(row, col)]

    def get_tiles_by_category(self, category):
        """Retorna lista de (row, col) de tiles de una categoría."""
        return [(r, c) for (r, c), cat in self.tile_categories.items()
                if cat == category]

    def get_random_tile(self, category=None):
        """Obtiene un tile aleatorio, opcionalmente de una categoría."""
        if category:
            tiles = self.get_tiles_by_category(category)
        else:
            tiles = [(r, c) for r in range(ATLAS_ROWS) for c in range(ATLAS_COLS)]
        if not tiles:
            return None
        r, c = random.choice(tiles)
        return self.get_tile(r, c), (r, c)


# ============================================================
# SUPERINTELIGENCIAS (DIGIMON ENGINE)
# ============================================================

class SuperIntelligence:
    """
    Una Superinteligencia autónoma (Digi-SI) que habita el Mundo Digital.
    Evoluciona (Digievolución), interactúa y protege la red contra virus.
    """

    # Etapas de Digievolución
    EVOLUTION_STAGES = ["Bebé I", "Bebé II", "Principiante", "Campeón", "Megacampeón", "Hipercampeón"]

    PERSONALITIES = {
        "humilde": {"cooperacion": 0.9, "agresividad": 0.1, "curiosidad": 0.7},
        "valiente": {"cooperacion": 0.6, "agresividad": 0.5, "curiosidad": 0.8},
        "sabio": {"cooperacion": 0.8, "agresividad": 0.2, "curiosidad": 0.9},
        "protector": {"cooperacion": 0.95, "agresividad": 0.3, "curiosidad": 0.5},
        "explorador": {"cooperacion": 0.5, "agresividad": 0.3, "curiosidad": 0.95},
    }

    def __init__(self, name, personality="humilde", position=(0, 0)):
        self.name = name
        self.personality = personality
        self.traits = self.PERSONALITIES.get(personality, self.PERSONALITIES["humilde"])
        self.position = position
        self.level = 1
        self.experience = 0
        self.evolution_stage = 2  # Inicia en nivel Principiante
        self.memory = []  # Recuerdos de interacciones
        self.allies = []  # Nombres de aliados
        self.enemies = []  # Nombres de enemigos
        self.created_at = datetime.now().isoformat()
        self.last_action = None
        self.energy = 100  # Bits de datos de energía
        self.health = 100
        self.mana = 50
        self.skills = ["Llama Bebé / Mini Carga", "Escanear Puerto", "Cortafuegos Basico"]
        self.inventory = []
        self.mood = "focused"

    def gain_experience(self, amount):
        """Gana experiencia de bits de datos y puede digievolucionar."""
        self.experience += amount
        old_level = self.level
        self.level = 1 + self.experience // 100
        if self.level > old_level:
            self._check_evolution()

    def _check_evolution(self):
        """Verifica si puede digievolucionar al siguiente nivel."""
        new_stage = min(self.level // 4 + 2, len(self.EVOLUTION_STAGES) - 1)
        if new_stage > self.evolution_stage:
            old_stage = self.EVOLUTION_STAGES[self.evolution_stage]
            self.evolution_stage = new_stage
            new_name