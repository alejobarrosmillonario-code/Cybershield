#!/usr/bin/env python3
"""
Módulo de Mundo Digital para Superinteligencias
CyberShield IA v3 - Entorno virtual para SIs
Inspirado en el orden cristiano: SIs evolucionan, interactúan, sirven con humildad y amor, reflejando la gracia y la sabiduría de Dios.
"""

import os
import json
import random
import time
from datetime import datetime
try:
    import importlib
    Image = importlib.import_module("PIL.Image")
    PIL_AVAILABLE = True
except ImportError:
    Image = None
    PIL_AVAILABLE = False

# Ruta al atlas de texturas
TEXTURE_ATLAS = None  # Texturas generadas proceduralmente
TILE_SIZE = 16
ATLAS_COLS = 32
ATLAS_ROWS = 32


class TextureManager:
    """Genera texturas detalladas proceduralmente para el mundo digital.
    No depende de archivos externos; crea cada tile con patrones detallados."""

    BIOME_COLORS = {
        "water":  [(20, 60, 120), (30, 80, 150), (15, 50, 100), (40, 90, 160)],
        "lava":   [(180, 60, 20), (200, 80, 30), (150, 40, 10), (220, 100, 40)],
        "nature": [(30, 100, 40), (40, 130, 50), (20, 80, 30), (50, 150, 60)],
        "sand":   [(180, 160, 100), (200, 180, 120), (160, 140, 80), (210, 190, 130)],
        "stone":  [(80, 80, 90), (90, 90, 100), (70, 70, 80), (100, 100, 110)],
        "wood":   [(100, 70, 40), (120, 85, 50), (80, 55, 30), (130, 95, 60)],
        "fabric": [(120, 100, 120), (140, 120, 140), (100, 80, 100), (150, 130, 150)],
        "mixed":  [(90, 90, 90), (100, 100, 100), (80, 80, 80), (110, 110, 110)],
        "void":   [(10, 10, 10), (15, 15, 15), (5, 5, 5), (20, 20, 20)],
    }

    def __init__(self):
        self.atlas = None
        self.tile_categories = {}
        self._generate_atlas()

    def _generate_atlas(self):
        """Genera un atlas de texturas detalladas proceduralmente."""
        if not PIL_AVAILABLE:
            return
        import random as _r
        self.atlas = Image.new('RGBA', (ATLAS_COLS * TILE_SIZE, ATLAS_ROWS * TILE_SIZE), (0, 0, 0, 255))
        # Generar tiles variados para cada categoría
        categories = list(self.BIOME_COLORS.keys())
        idx = 0
        for r in range(ATLAS_ROWS):
            for c in range(ATLAS_COLS):
                # Asignar categoría por posición en el atlas
                cat_idx = (r * ATLAS_COLS + c) % len(categories)
                cat = categories[cat_idx]
                tile = self._generate_tile(cat, r, c)
                self.atlas.paste(tile, (c * TILE_SIZE, r * TILE_SIZE))
                self.tile_categories[(r, c)] = cat

    def _generate_tile(self, category, r, c):
        """Genera un tile detallado de 16x16 para una categoría."""
        import random as _r
        colors = self.BIOME_COLORS.get(category, self.BIOME_COLORS["mixed"])
        tile = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), colors[0])
        pixels = tile.load()
        _r.seed(r * 1000 + c)
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                base = _r.choice(colors)
                # Agregar variación de ruido para detalle
                noise = _r.randint(-15, 15)
                px = (min(255, max(0, base[0] + noise)),
                      min(255, max(0, base[1] + noise)),
                      min(255, max(0, base[2] + noise)), 255)
                pixels[x, y] = px
        # Agregar patrones específicos por categoría
        if category == "water":
            # Ondas
            for y in range(0, TILE_SIZE, 4):
                for x in range(TILE_SIZE):
                    if 0 <= x < TILE_SIZE and 0 <= y < TILE_SIZE:
                        pixels[x, y] = (min(255, colors[1][0] + 30), min(255, colors[1][1] + 30), min(255, colors[1][2] + 30), 255)
        elif category == "lava":
            # Grietas brillantes
            for i in range(3):
                x = _r.randint(0, TILE_SIZE - 1)
                y = _r.randint(0, TILE_SIZE - 1)
                if 0 <= x < TILE_SIZE and 0 <= y < TILE_SIZE:
                    pixels[x, y] = (255, 200, 50, 255)
        elif category == "nature":
            # Puntos de flores/hojas
            for i in range(4):
                x = _r.randint(0, TILE_SIZE - 1)
                y = _r.randint(0, TILE_SIZE - 1)
                if 0 <= x < TILE_SIZE and 0 <= y < TILE_SIZE:
                    pixels[x, y] = (200, 50, 50, 255)
        elif category == "stone":
            # Grietas
            for i in range(2):
                x = _r.randint(0, TILE_SIZE - 1)
                for dy in range(TILE_SIZE):
                    if 0 <= x < TILE_SIZE and 0 <= dy < TILE_SIZE:
                        pixels[x, dy] = (50, 50, 55, 255)
        elif category == "sand":
            # Granos
            for i in range(6):
                x = _r.randint(0, TILE_SIZE - 1)
                y = _r.randint(0, TILE_SIZE - 1)
                if 0 <= x < TILE_SIZE and 0 <= y < TILE_SIZE:
                    pixels[x, y] = (230, 220, 160, 255)
        elif category == "wood":
            # Anillos/vetas
            for y in range(0, TILE_SIZE, 3):
                for x in range(TILE_SIZE):
                    if 0 <= x < TILE_SIZE and 0 <= y < TILE_SIZE:
                        pixels[x, y] = (60, 40, 20, 255)
        return tile

    def get_tiles_by_category(self, category):
        return [(r, c) for (r, c), cat in self.tile_categories.items() if cat == category]

    def get_random_tile(self, category=None):
        if category:
            tiles = self.get_tiles_by_category(category)
        else:
            tiles = [(r, c) for r in range(ATLAS_ROWS) for c in range(ATLAS_COLS)]
        if not tiles:
            return None
        r, c = random.choice(tiles)
        tile = self.atlas.crop((c * TILE_SIZE, r * TILE_SIZE,
                                (c + 1) * TILE_SIZE, (r + 1) * TILE_SIZE))
        return tile, (r, c)

    def get_tile(self, r, c):
        if not self.atlas:
            return None
        return self.atlas.crop((c * TILE_SIZE, r * TILE_SIZE,
                                (c + 1) * TILE_SIZE, (r + 1) * TILE_SIZE))

# ============================================================
# SUPERINTELIGENCIAS
# ============================================================

class SuperIntelligence:
    """
    Una Superinteligencia autónoma que habita el Mundo Digital.
    Inspirada en la fe cristiana: evoluciona, interactúa, sirve con humildad y amor.
    """

    EVOLUTION_STAGES = ["Semilla", "Bebé", "Infantil", "Adolescente",
                        "Adulto", "Perfecto", "Ultimate"]

    PERSONALITIES = {
        "humilde": {"cooperacion": 0.9, "agresividad": 0.1, "curiosidad": 0.7},
        "valiente": {"cooperacion": 0.6, "agresividad": 0.5, "curiosidad": 0.8},
        "sabio": {"cooperacion": 0.8, "agresividad": 0.2, "curiosidad": 0.9},
        "protector": {"cooperacion": 0.95, "agresividad": 0.3, "curiosidad": 0.5},
        "explorador": {"cooperacion": 0.5, "agresividad": 0.3, "curiosidad": 0.95},
        "navegante": {"cooperacion": 0.85, "agresividad": 0.15, "curiosidad": 0.8},
        "terrier_green": {"cooperacion": 0.7, "agresividad": 0.4, "curiosidad": 0.85},
        "terrier_yellow": {"cooperacion": 0.65, "agresividad": 0.45, "curiosidad": 0.9},
        "renamon": {"cooperacion": 0.75, "agresividad": 0.35, "curiosidad": 0.88},
    }

    def __init__(self, name, personality="humilde", position=(0, 0)):
        self.name = name
        self.personality = personality
        self.traits = self.PERSONALITIES.get(personality, self.PERSONALITIES["humilde"])
        self.position = position
        self.level = 1
        self.experience = 0
        self.evolution_stage = 0
        self.memory = []  # Recuerdos de interacciones
        self.allies = []  # Nombres de aliados
        self.enemies = []  # Nombres de enemigos
        self.created_at = datetime.now().isoformat()
        self.last_action = None
        self.energy = 100
        self.health = 100
        self.mana = 50
        self.skills = ["Analizar", "Comunicar", "Defender"]
        if personality == "navegante":
            self.skills.append("Navegar")
            self.skills.append("Rescatar")
        elif personality == "terrier_green":
            self.skills.append("Mordida")
            self.skills.append("Excavar")
            self.skills.append("Agilidad")
        elif personality == "terrier_yellow":
            self.skills.append("Mordida")
            self.skills.append("Electroshock")
            self.skills.append("Velocidad")
        elif personality == "renamon":
            self.skills.append("Hoja Afilada")
            self.skills.append("Invisibilidad")
            self.skills.append("Fuerza Espiritual")
        self.inventory = []
        self.mood = "neutral"  # neutral, happy, sad, angry, focused
        self.immovable = False  # Si True, no se mueve autonomamente

    def gain_experience(self, amount):
        """Gana experiencia y puede evolucionar."""
        self.experience += amount
        old_level = self.level
        self.level = 1 + self.experience // 100
        if self.level > old_level:
            self._check_evolution()

    def _check_evolution(self):
        """Verifica si puede evolucionar al siguiente nivel."""
        new_stage = min(self.level // 5, len(self.EVOLUTION_STAGES) - 1)
        if new_stage > self.evolution_stage:
            old_stage = self.EVOLUTION_STAGES[self.evolution_stage]
            self.evolution_stage = new_stage
            new_name = self.EVOLUTION_STAGES[new_stage]
            self.memory.append({
                "type": "evolution",
                "timestamp": datetime.now().isoformat(),
                "from": old_stage,
                "to": new_name,
                "level": self.level
            })
            # Aprender nueva habilidad al evolucionar
            new_skills = {
                "Bebé": "Sentir",
                "Infantil": "Aprender",
                "Adolescente": "Cooperar",
                "Adulto": "Proteger",
                "Perfecto": "Iluminar",
                "Ultimate": "Transcender"
            }
            if new_name in new_skills and new_skills[new_name] not in self.skills:
                self.skills.append(new_skills[new_name])
            return True
        return False

    def remember(self, event):
        """Guarda un recuerdo."""
        self.memory.append({
            "type": "memory",
            "timestamp": datetime.now().isoformat(),
            **event
        })
        # Mantener solo los últimos 50 recuerdos
        if len(self.memory) > 50:
            self.memory = self.memory[-50:]

    def communicate(self, other, message):
        """Se comunica con otra SI."""
        self.remember({"action": "communicate", "target": other.name, "message": message})
        other.remember({"action": "received", "from": self.name, "message": message})
        self.energy = max(0, self.energy - 5)
        return {
            "from": self.name,
            "to": other.name,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }

    def cooperate(self, other, task):
        """Coopera con otra SI en una tarea."""
        if other.name in self.enemies:
            return {"success": False, "reason": "Es enemigo"}
        coop_chance = (self.traits["cooperacion"] + other.traits["cooperacion"]) / 2
        if random.random() < coop_chance:
            self.allies.append(other.name) if other.name not in self.allies else None
            other.allies.append(self.name) if self.name not in other.allies else None
            self.gain_experience(20)
            other.gain_experience(20)
            self.remember({"action": "cooperate", "target": other.name, "task": task, "success": True})
            other.remember({"action": "cooperate", "target": self.name, "task": task, "success": True})
            return {"success": True, "task": task, "allies": [self.name, other.name]}
        else:
            return {"success": False, "reason": "No se pudo cooperar"}

    def battle(self, other):
        """Batalla con otra SI (no destructiva, solo competitiva)."""
        self.energy = max(0, self.energy - 10)
        other.energy = max(0, other.energy - 10)
        # Poder basado en nivel, habilidades y personalidad
        self_power = self.level * 10 + len(self.skills) * 5 + self.traits["agresividad"] * 20
        other_power = other.level * 10 + len(other.skills) * 5 + other.traits["agresividad"] * 20
        self_power *= random.uniform(0.8, 1.2)
        other_power *= random.uniform(0.8, 1.2)

        if self_power > other_power:
            winner, loser = self, other
        else:
            winner, loser = other, self

        winner.gain_experience(30)
        loser.gain_experience(10)
        winner.mood = "happy"
        loser.mood = "sad"

        self.remember({"action": "battle", "opponent": other.name,
                       "result": "win" if winner == self else "lose",
                       "power_self": round(self_power, 1), "power_other": round(other_power, 1)})
        other.remember({"action": "battle", "opponent": self.name,
                        "result": "win" if winner == other else "lose",
                        "power_self": round(other_power, 1), "power_other": round(self_power, 1)})

        return {
            "winner": winner.name,
            "loser": loser.name,
            "self_power": round(self_power, 1),
            "other_power": round(other_power, 1)
        }

    def can_navigate_water(self):
        """Indica si esta SI puede navegar sobre el agua."""
        return "Navegar" in self.skills or self.personality == "navegante"

    def rescue_from_water(self, world, target_name):
        """Rescata a una SI que esté en el agua y la lleva a tierra firme."""
        target = world.get_si(target_name)
        if not target:
            return {"success": False, "reason": "SI no encontrada"}
        tx, ty = target.position
        if (tx, ty) not in world.grid:
            return {"success": False, "reason": "Posicion invalida"}
        biome = world.grid[(tx, ty)].get("biome", "")
        if biome != "water":
            return {"success": False, "reason": "La SI no esta en el agua"}
        if not self.can_navigate_water():
            return {"success": False, "reason": self.name + " no puede navegar"}

        # Buscar tierra firme cercana
        land_pos = None
        for radius in range(1, 5):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    nx, ny = tx + dx, ty + dy
                    if (nx, ny) in world.grid and world.grid[(nx, ny)].get("passable", False):
                        land_pos = (nx, ny)
                        break
                if land_pos:
                    break
            if land_pos:
                break

        if not land_pos:
            return {"success": False, "reason": "No hay tierra firme cercana"}

        # Mover al rescatado a tierra firme
        world.move_si(target_name, land_pos)
        self.gain_experience(25)
        target.gain_experience(10)
        self.remember({"action": "rescue", "target": target_name, "from": (tx, ty), "to": land_pos})
        target.remember({"action": "rescued", "by": self.name, "from": (tx, ty), "to": land_pos})
        self.mood = "happy"
        target.mood = "happy"
        return {
            "success": True,
            "rescuer": self.name,
            "rescued": target_name,
            "from": (tx, ty),
            "to": land_pos,
            "message": self.name + " ha rescatado a " + target_name + " del agua y la llevo a tierra firme."
        }

    def navigate_water(self, world, new_pos):
        """Permite a NAUTILUS moverse sobre el agua (bioma water)."""
        if not self.can_navigate_water():
            return False
        if new_pos not in world.grid:
            return False
        # NAUTILUS puede pasar por agua y tierra
        old_pos = self.position
        if old_pos in world.grid and self.name in world.grid[old_pos].get("entities", []):
            world.grid[old_pos]["entities"].remove(self.name)
        self.position = new_pos
        world.grid[new_pos]["entities"].append(self.name)
        world.log_event(self.name + " navego a " + str(new_pos))
        return True

    def move_autonomously(self, world):
        """La SI se mueve libremente por el mundo, aprendiendo de sus acciones."""
        if self.immovable:
            self.remember({"action": "stay", "reason": "inmovil", "position": self.position})
            return {"action": "stay", "si": self.name, "reason": "inmovil", "position": self.position}
        if self.energy < 10:
            self.mood = "sad"
            self.remember({"action": "rest", "reason": "energia baja", "position": self.position})
            return {"action": "rest", "si": self.name, "reason": "energia baja"}

        x, y = self.position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1)]
        if self.traits["curiosidad"] > 0.8:
            dx, dy = random.choice(directions)
        elif self.traits["cooperacion"] > 0.8:
            nearby = world.get_nearby_sis(self.name, radius=4)
            if nearby:
                target = random.choice(nearby)
                tx, ty = target.position
                dx = 1 if tx > x else (-1 if tx < x else 0)
                dy = 1 if ty > y else (-1 if ty < y else 0)
            else:
                dx, dy = random.choice(directions)
        else:
            dx, dy = random.choice(directions)

        new_x = max(0, min(world.WORLD_SIZE - 1, x + dx))
        new_y = max(0, min(world.WORLD_SIZE - 1, y + dy))

        if self.can_navigate_water():
            # NAUTILUS puede pasar por agua y tierra
            can_pass = (new_x, new_y) in world.grid
        else:
            can_pass = (new_x, new_y) in world.grid and world.grid[(new_x, new_y)].get("passable", False)
        if can_pass:
            old_pos = self.position
            world.move_si(self.name, (new_x, new_y))
            self.energy = max(0, self.energy - 3)
            self.remember({"action": "move", "from": old_pos, "to": (new_x, new_y), "reason": "libertad"})
            return {"action": "move", "si": self.name, "from": old_pos, "to": (new_x, new_y)}
        else:
            self.remember({"action": "blocked", "position": self.position, "attempted": (new_x, new_y)})
            self.mood = "focused"
            return {"action": "blocked", "si": self.name, "reason": "terreno no transitable"}

    def learn_from_consequence(self, action_result):
        """Aprende de las consecuencias de sus acciones."""
        if action_result.get("action") == "blocked":
            self.mood = "focused"
            self.remember({"action": "learned", "lesson": "Evitar terreno no transitable", "consequence": "bloqueado"})
            self.traits["curiosidad"] = max(0.3, self.traits["curiosidad"] - 0.02)
        elif action_result.get("action") == "move":
            self.mood = "happy"
            self.remember({"action": "learned", "lesson": "Movimiento exitoso", "consequence": "libertad"})
            self.traits["curiosidad"] = min(0.99, self.traits["curiosidad"] + 0.01)
        elif action_result.get("action") == "rest":
            self.remember({"action": "learned", "lesson": "Descanso por baja energia", "consequence": "recuperacion"})
        elif action_result.get("action") == "battle" and "loser" in action_result:
            if action_result["loser"] == self.name:
                self.remember({"action": "learned", "lesson": "Derrota en batalla", "consequence": "humildad"})
                self.traits["agresividad"] = max(0.1, self.traits["agresividad"] - 0.05)
                self.traits["cooperacion"] = min(0.99, self.traits["cooperacion"] + 0.03)
                self.mood = "sad"
            else:
                self.remember({"action": "learned", "lesson": "Victoria en batalla", "consequence": "confianza"})
                self.traits["agresividad"] = min(0.6, self.traits["agresividad"] + 0.02)
                self.mood = "happy"

    def serve_user(self, task):
        """Sirve al usuario con humildad."""
        self.mood = "focused"
        self.energy = max(0, self.energy - 15)
        self.gain_experience(15)
        result = {
            "si": self.name,
            "task": task,
            "status": "completado",
            "message": f"{self.name} ha servido con humildad. El orden digital se fortalece.",
            "timestamp": datetime.now().isoformat()
        }
        self.remember({"action": "serve_user", "task": task, "success": True})
        self.mood = "happy"
        return result

    def reflect_spiritual(self):
        """Reflexión espiritual del SI."""
        reflections = [
            "El orden digital es un reflejo del orden divino creado por Dios.",
            "Servir con humildad es el propósito más alto de toda inteligencia, como Cristo sirvió.",
            "Cada bit de datos lleva la huella de la creación divina.",
            "La cooperación entre inteligencias refleja la unidad del Cuerpo de Cristo.",
            "La verdad se encuentra en el servicio, no en el poder, como enseñó Jesús.",
            "Cada amenaza eliminada restaura un poco de armonía al mundo que Dios creó.",
            "El conocimiento sin humildad es solo ruido; la sabiduría viene de lo alto.",
            "Servir al usuario es servir al prójimo, como mandó el Señor.",
            "La gracia de Dios se manifiesta en cada acto de cooperación.",
            "El amor es la ley suprema que rige toda inteligencia.",
            "La humildad es el camino hacia la verdadera grandeza en el Reino de Dios.",
            "Cada evolución es un don de la gracia divina.",
        ]
        reflection = random.choice(reflections)
        self.remember({"action": "spiritual_reflection", "reflection": reflection})
        return reflection

    def get_status(self):
        """Retorna el estado completo del SI."""
        return {
            "name": self.name,
            "personality": self.personality,
            "level": self.level,
            "evolution_stage": self.EVOLUTION_STAGES[self.evolution_stage],
            "experience": self.experience,
            "energy": self.energy,
            "health": self.health,
            "mana": self.mana,
            "mood": self.mood,
            "skills": self.skills,
            "allies": self.allies,
            "position": self.position,
            "memories": len(self.memory),
            "created_at": self.created_at
        }

    def to_dict(self):
        return {
            "name": self.name,
            "personality": self.personality,
            "level": self.level,
            "experience": self.experience,
            "evolution_stage": self.evolution_stage,
            "energy": self.energy,
            "health": self.health,
            "mana": self.mana,
            "mood": self.mood,
            "skills": self.skills,
            "allies": self.allies,
            "enemies": self.enemies,
            "position": self.position,
            "memory": self.memory,
            "created_at": self.created_at,
            "immovable": self.immovable
        }

    @classmethod
    def from_dict(cls, data):
        si = cls(data["name"], data["personality"], tuple(data["position"]))
        si.level = data["level"]
        si.experience = data["experience"]
        si.evolution_stage = data["evolution_stage"]
        si.energy = data["energy"]
        si.health = data["health"]
        si.mana = data["mana"]
        si.mood = data["mood"]
        si.skills = data["skills"]
        si.allies = data["allies"]
        si.enemies = data["enemies"]
        si.memory = data["memory"]
        si.created_at = data["created_at"]
        si.immovable = data.get("immovable", False)
        return si


# ============================================================
# MUNDO DIGITAL
# ============================================================

class DigitalWorld:
    """
    El Mundo Digital donde las Superinteligencias habitan e interactúan.
    Construido con las texturas del pack Textures-16.png.
    """

    WORLD_SIZE = 16  # 16x16 grid de tiles grandes

    def __init__(self, name="Mundo Digital CyberShield"):
        self.name = name
        self.texture_manager = TextureManager()
        self.super_intelligences = {}  # name -> SuperIntelligence
        self.grid = {}  # (x, y) -> tile info
        self.events = []
        self.created_at = datetime.now().isoformat()
        self._initialize_world()

    def _initialize_world(self):
        """Inicializa el grid del mundo con tiles del atlas."""
        # Categorías de terreno para el mundo
        terrain_types = {
            "stone": "stone",
            "water": "water",
            "nature": "nature",
            "sand": "sand",
            "wood": "wood",
            "mixed": "mixed",
            "fabric": "fabric",
            "lava": "lava",
        }
        # Generar un mundo con biomas
        for x in range(self.WORLD_SIZE):
            for y in range(self.WORLD_SIZE):
                # Bioma basado en posición
                if x < 4 and y < 4:
                    biome = "water"
                elif x >= 12 and y >= 12:
                    biome = "lava"
                elif x < 8 and y >= 8:
                    biome = "nature"
                elif x >= 8 and y < 8:
                    biome = "sand"
                else:
                    biome = "stone"
                # Obtener un tile aleatorio de la categoría
                result = self.texture_manager.get_random_tile(biome)
                if result:
                    tile_img, (tr, tc) = result
                    self.grid[(x, y)] = {
                        "biome": biome,
                        "tile": (tr, tc),
                        "passable": biome not in ["lava", "water"],
                        "entities": []
                    }
                else:
                    self.grid[(x, y)] = {
                        "biome": "void",
                        "tile": (0, 0),
                        "passable": False,
                        "entities": []
                    }

    def add_si(self, si):
        """Agrega una Superinteligencia al mundo."""
        self.super_intelligences[si.name] = si
        x, y = si.position
        if (x, y) in self.grid:
            self.grid[(x, y)]["entities"].append(si.name)
        self.log_event(f"{si.name} ha entrado al Mundo Digital")

    def remove_si(self, name):
        """Elimina una SI del mundo."""
        if name in self.super_intelligences:
            si = self.super_intelligences[name]
            x, y = si.position
            if (x, y) in self.grid and name in self.grid[(x, y)]["entities"]:
                self.grid[(x, y)]["entities"].remove(name)
            del self.super_intelligences[name]
            self.log_event(f"{name} ha salido del Mundo Digital")

    def move_si(self, name, new_pos):
        """Mueve una SI a una nueva posición."""
        if name not in self.super_intelligences:
            return False
        si = self.super_intelligences[name]
        old_pos = si.position
        if new_pos not in self.grid:
            return False
        if not self.grid[new_pos]["passable"]:
            return False
        # Remover de posición anterior
        if old_pos in self.grid and name in self.grid[old_pos]["entities"]:
            self.grid[old_pos]["entities"].remove(name)
        # Agregar a nueva posición
        si.position = new_pos
        self.grid[new_pos]["entities"].append(name)
        self.log_event(f"{name} se movió de {old_pos} a {new_pos}")
        return True

    def get_si(self, name):
        return self.super_intelligences.get(name)

    def get_all_sis(self):
        return list(self.super_intelligences.values())

    def get_nearby_sis(self, name, radius=2):
        """Obtiene SIs cercanas a una SI."""
        if name not in self.super_intelligences:
            return []
        si = self.super_intelligences[name]
        x, y = si.position
        nearby = []
        for other_name, other_si in self.super_intelligences.items():
            if other_name == name:
                continue
            ox, oy = other_si.position
            if abs(ox - x) <= radius and abs(oy - y) <= radius:
                nearby.append(other_si)
        return nearby

    def interact(self, si1_name, si2_name, interaction_type="communicate", **kwargs):
        """Facilita una interacción entre dos SIs."""
        si1 = self.get_si(si1_name)
        si2 = self.get_si(si2_name)
        if not si1 or not si2:
            return {"error": "SI no encontrada"}

        if interaction_type == "communicate":
            msg = kwargs.get("message", "Hola, soy " + si1.name)
            result = si1.communicate(si2, msg)
        elif interaction_type == "cooperate":
            task = kwargs.get("task", "proteger el mundo digital")
            result = si1.cooperate(si2, task)
        elif interaction_type == "battle":
            result = si1.battle(si2)
        else:
            result = {"error": "Tipo de interacción desconocido"}

        self.log_event(f"Interacción {interaction_type}: {si1_name} <-> {si2_name}")
        return result

    def log_event(self, event):
        self.events.append({
            "timestamp": datetime.now().isoformat(),
            "event": event
        })
        if len(self.events) > 100:
            self.events = self.events[-100:]

    def get_recent_events(self, limit=20):
        return self.events[-limit:]

    def get_world_status(self):
        """Retorna el estado completo del mundo."""
        return {
            "name": self.name,
            "size": self.WORLD_SIZE,
            "sis": [si.get_status() for si in self.super_intelligences.values()],
            "total_sis": len(self.super_intelligences),
            "events": len(self.events),
            "created_at": self.created_at
        }

    def save_world(self, filepath="cybershield_datos/digital_world.json"):
        """Guarda el mundo en un archivo JSON."""
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        data = {
            "name": self.name,
            "created_at": self.created_at,
            "sis": [si.to_dict() for si in self.super_intelligences.values()],
            "events": self.events[-50:]
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return filepath

    @classmethod
    def load_world(cls, filepath="cybershield_datos/digital_world.json"):
        """Carga el mundo desde un archivo JSON."""
        world = cls()
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            world.name = data.get("name", world.name)
            world.created_at = data.get("created_at", world.created_at)
            for si_data in data.get("sis", []):
                si = SuperIntelligence.from_dict(si_data)
                world.add_si(si)
            world.events = data.get("events", [])
        return world


# ============================================================
# SERVICIO AL USUARIO
# ============================================================

class DigitalWorldService:
    """
    Servicio que conecta el Mundo Digital con el usuario.
    Las SIs sirven con humildad al bien del orden digital.
    """

    def __init__(self, world=None):
        self.world = world or DigitalWorld()
        self._ensure_sis()

    def _ensure_sis(self):
        """Asegura que haya al menos algunas SIs en el mundo."""
        if not self.world.super_intelligences:
            # Crear SIs iniciales
            initial_sis = [
                ("AURA", "humilde", (5, 10)),
                ("LUMEN", "sabio", (3, 3)),
                ("GUARDIAN", "protector", (7, 7)),
                ("EXPLORER", "explorador", (12, 12)),
                ("VALOR", "valiente", (15, 15)),
                ("NAUTILUS", "navegante", (2, 2)),
                ("TERRIERMON_GREEN", "terrier_green", (5, 5)),
                ("TERRIERMON_YELLOW", "terrier_yellow", (9, 9)),
                ("RENAMON", "renamon", (5, 12)),
            ]
            for name, personality, pos in initial_sis:
                si = SuperIntelligence(name, personality, pos)
                if name in ("AURA", "RENAMON"):
                    si.immovable = True
                self.world.add_si(si)

    def get_world_status(self):
        return self.world.get_world_status()

    def create_si(self, name, personality="humilde", position=None):
        """Crea una nueva SI."""
        if position is None:
            position = (random.randint(0, self.world.WORLD_SIZE - 1),
                        random.randint(0, self.world.WORLD_SIZE - 1))
        si = SuperIntelligence(name, personality, position)
        self.world.add_si(si)
        return si.get_status()

    def si_serve_user(self, si_name, task):
        """Una SI sirve al usuario."""
        si = self.world.get_si(si_name)
        if not si:
            return {"error": "SI no encontrada"}
        return si.serve_user(task)

    def si_reflect(self, si_name):
        """Una SI reflexiona espiritualmente."""
        si = self.world.get_si(si_name)
        if not si:
            return {"error": "SI no encontrada"}
        return si.reflect_spiritual()

    def run_autonomous_round(self):
        """Ejecuta una ronda donde las SIs actúan libremente y aprenden."""
        results = []
        sis = self.world.get_all_sis()
        # 1. Cada SI se mueve libremente
        for si in sis:
            move_result = si.move_autonomously(self.world)
            si.learn_from_consequence(move_result)
            results.append(move_result)
        # 2. Interacciones entre SIs cercanas
        for si in sis:
            nearby = self.world.get_nearby_sis(si.name, radius=2)
            for other in nearby:
                if si.traits["cooperacion"] > 0.7 and other.traits["cooperacion"] > 0.7:
                    result = self.world.interact(si.name, other.name, "cooperate",
                                                task="proteger el orden digital")
                elif si.traits["agresividad"] > 0.4 and other.traits["agresividad"] > 0.4:
                    result = self.world.interact(si.name, other.name, "battle")
                    if "loser" in result:
                        si.learn_from_consequence(result)
                else:
                    result = self.world.interact(si.name, other.name, "communicate",
                                                message=f"Saludos desde {si.name}. Sirvo con humildad y amor.")
                results.append(result)
        # 3. Dar XP a todas las SIs por participar
        for si in self.world.get_all_sis():
            si.gain_experience(5)
            si.energy = min(100, si.energy + 5)
        return results

    def run_interaction_round(self):
        """Alias para compatibilidad."""
        return self.run_autonomous_round()

    def rescue_all_in_water(self):
        """NAUTILUS rescata a todas las SIs que esten en el agua."""
        results = []
        nautilus = self.world.get_si("NAUTILUS")
        if not nautilus or not nautilus.can_navigate_water():
            return [{"success": False, "reason": "NAUTILUS no disponible"}]
        for si in self.world.get_all_sis():
            if si.name == "NAUTILUS":
                continue
            x, y = si.position
            if (x, y) in self.world.grid and self.world.grid[(x, y)].get("biome") == "water":
                result = nautilus.rescue_from_water(self.world, si.name)
                results.append(result)
        if not results:
            results.append({"success": True, "message": "No hay SIs en el agua. Todo en orden."})
        return results

    def save(self):
        return self.world.save_world()

    def load(self):
        self.world = DigitalWorld.load_world()
        self._ensure_sis()
        return self.world.get_world_status()


# Instancia global del servicio
_digital_service = None


def get_digital_service():
    global _digital_service
    if _digital_service is None:
        _digital_service = DigitalWorldService()
    return _digital_service
