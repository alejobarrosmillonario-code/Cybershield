import os

filepath = "main.pyw"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Agregar import de ImageTk
old_import = "from digital_world import get_digital_service\n    DIGITAL_WORLD_AVAILABLE = True"
new_import = "from digital_world import get_digital_service\n    from PIL import Image, ImageTk\n    DIGITAL_WORLD_AVAILABLE = True"
if old_import in content:
    content = content.replace(old_import, new_import, 1)
    print("1. ImageTk importado")

# 2. Agregar Canvas de mapa antes de log_frame
old_log = "        log_frame = tk.LabelFrame(\n            dw_frame, text='EVENTOS DEL MUNDO DIGITAL'"
new_map = """        map_frame = tk.LabelFrame(
            dw_frame, text='MAPA DEL MUNDO DIGITAL', font=('Courier', 10, 'bold'),
            fg=self.CYAN, bg=self.DARK_BG, borderwidth=2
        )
        map_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.dw_map_canvas = tk.Canvas(
            map_frame, width=400, height=400, bg=self.DARK_BG,
            highlightthickness=1, highlightbackground=self.MATRIX_GREEN
        )
        self.dw_map_canvas.pack(padx=5, pady=5)

        self.dw_map_photo = None

        log_frame = tk.LabelFrame(
            dw_frame, text='EVENTOS DEL MUNDO DIGITAL'"""
if old_log in content:
    content = content.replace(old_log, new_map, 1)
    print("2. Canvas de mapa agregado")

# 3. Agregar dw_render_map antes de dw_show_status
old_refresh = "    def dw_show_status(self):"
new_render = '''    def dw_render_map(self):
        if not DIGITAL_WORLD_AVAILABLE:
            return
        try:
            import os
            atlas_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Textures-16.png")
            atlas = Image.open(atlas_path)

            map_size = self.dw_service.world.WORLD_SIZE * 16
            map_img = Image.new('RGBA', (map_size, map_size), (0, 0, 0, 255))

            for x in range(self.dw_service.world.WORLD_SIZE):
                for y in range(self.dw_service.world.WORLD_SIZE):
                    tile_info = self.dw_service.world.grid.get((x, y))
                    if tile_info:
                        tr, tc = tile_info['tile']
                        tile = atlas.crop((tc * 16, tr * 16, (tc + 1) * 16, (tr + 1) * 16))
                        map_img.paste(tile, (x * 16, y * 16))

            for si in self.dw_service.world.get_all_sis():
                x, y = si.position
                for dx in range(8):
                    for dy in range(8):
                        px, py = x * 16 + 4 + dx, y * 16 + 4 + dy
                        if 0 <= px < map_size and 0 <= py < map_size:
                            map_img.putpixel((px, py), (255, 255, 0, 255))

            map_img = map_img.resize((400, 400), Image.NEAREST)
            self.dw_map_photo = ImageTk.PhotoImage(map_img)
            self.dw_map_canvas.create_image(0, 0, anchor=tk.NW, image=self.dw_map_photo)
            self.dw_map_canvas.image = self.dw_map_photo
            self.dw_log('Mapa renderizado')
        except Exception as e:
            self.dw_log('Error renderizando mapa: ' + str(e))

    def dw_show_status(self):'''
if old_refresh in content:
    content = content.replace(old_refresh, new_render, 1)
    print("3. dw_render_map agregado")

# 4. Llamar a dw_render_map en dw_refresh_status
old_refresh2 = "        self.dw_si_text.see(tk.END)\n\n    def dw_show_status(self):"
new_refresh2 = "        self.dw_si_text.see(tk.END)\n        self.dw_render_map()\n\n    def dw_show_status(self):"
if old_refresh2 in content:
    content = content.replace(old_refresh2, new_refresh2, 1)
    print("4. dw_render_map llamado en refresh")

# 5. Llamar a dw_render_map al inicializar
old_init = '            self.dw_log("Mundo Digital inicializado. SIs activas: " + str(self.dw_service.get_world_status()[\'total_sis\']))\n            self.dw_refresh_status()'
new_init = '            self.dw_log("Mundo Digital inicializado. SIs activas: " + str(self.dw_service.get_world_status()[\'total_sis\']))\n            self.dw_refresh_status()\n            self.dw_render_map()'
if old_init in content:
    content = content.replace(old_init, new_init, 1)
    print("5. dw_render_map llamado al init")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Guardado: " + str(len(content)) + " bytes")
