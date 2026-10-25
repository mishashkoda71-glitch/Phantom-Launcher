import customtkinter as ctk
import os
import json
import random
import subprocess
import shutil
from tkinter import messagebox

# --- НАСТРОЙКИ ПУТЕЙ ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODS_DIR = os.path.join(BASE_DIR, "mods")
INTERNAL_DIR = os.path.join(BASE_DIR, "internal")
CONFIG_DIR = os.path.join(BASE_DIR, "configs")

# Автоматический поиск папки .minecraft на ЛЮБОМ ПК с Windows
APPDATA_PATH = os.getenv('APPDATA')
if APPDATA_PATH:
    MINECRAFT_DIR = os.path.join(APPDATA_PATH, ".minecraft")
else:
    MINECRAFT_DIR = r"C:\Users\Default\AppData\Roaming\.minecraft"

# Список читов
CHEATS = [
    "Phantom (Наш клиент)",
    "Nursultan", "Celestial Premium", "Haruka", "Pulse", "Wild", "Expensive", 
    "Akrien", "Zamorozka", "Wurst", "Impact", "LiquidBounce", "Sigma", 
    "Aristois", "Rich Client", "ReallyWorld (Crack)", "FunTime Client (Crack)", 
    "Excellent", "Midnight", "Envy", "WeepCraft", "Delta Client", "Rockstar", 
    "Night", "SpookyTime", "VonTam", "FTHelper", "HollyWorld", "Sunrise", 
    "Ares", "Krypton", "Astral", "Novo", "Void"
]

# Список модулей
MODULES = [
    "AIAura", "AutoMace Combo", "AutoTotem Smart", "FastItemScroll", 
    "KillAura", "Velocity", "Criticals", "Speed", "Fly", "NoFall", 
    "GlowESP", "Chams", "Tracers", "FullBright"
]

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("red")

class LauncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Phantom Launcher")
        self.geometry("700x850")
        
        os.makedirs(MODS_DIR, exist_ok=True)
        os.makedirs(INTERNAL_DIR, exist_ok=True)
        os.makedirs(CONFIG_DIR, exist_ok=True)

        self.canvas = ctk.CTkCanvas(self, width=700, height=850, bg="#1a1a1a", highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.setup_ui()
        self.create_snow()

    def setup_ui(self):
        ctk.CTkLabel(self, text="PHANTOM LAUNCHER", font=("Impact", 40, "bold"), text_color="#ff3333").pack(pady=15)

        self.cheat_var = ctk.StringVar(value=CHEATS[0])
        self.combobox = ctk.CTkComboBox(self, values=CHEATS, variable=self.cheat_var, width=400, font=("Arial", 14))
        self.combobox.pack(pady=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=500, height=200, label_text="Модули для конфига")
        self.scroll_frame.pack(pady=10)

        self.module_vars = {}
        for mod in MODULES:
            var = ctk.BooleanVar(value=True)
            cb = ctk.CTkCheckBox(self.scroll_frame, text=mod, variable=var, font=("Arial", 12))
            cb.pack(anchor="w", pady=1)
            self.module_vars[mod] = var

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        self.btn_save = ctk.CTkButton(self.btn_frame, text="💾 СОХРАНИТЬ КОНФИГ", font=("Arial", 14, "bold"), 
                                      fg_color="#0055ff", hover_color="#0033cc", width=200,
                                      command=self.save_config)
        self.btn_save.grid(row=0, column=0, padx=10)

        self.btn_launch = ctk.CTkButton(self.btn_frame, text="▶ ЗАПУСТИТЬ ИГРУ", font=("Arial", 14, "bold"), 
                                        fg_color="#cc0000", hover_color="#990000", width=200,
                                        command=self.launch_game)
        self.btn_launch.grid(row=0, column=1, padx=10)

        self.log_box = ctk.CTkTextbox(self, width=600, height=150, font=("Consolas", 12), text_color="#00ff00")
        self.log_box.pack(pady=10)
        self.log_box.insert("end", "> Лаунчер готов. Phantom встроен в систему.\n")
        self.log_box.configure(state="disabled")

    def create_snow(self):
        self.snowflakes = []
        for _ in range(50):
            x = random.randint(0, 700)
            y = random.randint(-850, 850)
            size = random.randint(2, 5)
            speed = random.uniform(0.5, 2.0)
            snowflake = self.canvas.create_oval(x, y, x+size, y+size, fill="white", outline="")
            self.snowflakes.append((snowflake, speed))
        self.animate_snow()

    def animate_snow(self):
        for snowflake, speed in self.snowflakes:
            self.canvas.move(snowflake, 0, speed)
            pos = self.canvas.coords(snowflake)
            if pos[1] > 850:
                x = random.randint(0, 700)
                self.canvas.coords(snowflake, x, -10, x + 4, -6)
        self.after(50, self.animate_snow)

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"> {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def save_config(self):
        enabled = [mod for mod, var in self.module_vars.items() if var.get()]
        config_path = os.path.join(CONFIG_DIR, "phantom_config.json")
        with open(config_path, "w") as f:
            json.dump({"modules": enabled}, f, indent=4)
        self.log(f"Конфиг сохранен! Включено: {len(enabled)} модулей.")

    def launch_game(self):
        cheat_name = self.cheat_var.get()
        
        if cheat_name == "Phantom (Наш клиент)":
            phantom_internal = os.path.join(INTERNAL_DIR, "Phantom.jar")
            phantom_mods = os.path.join(MODS_DIR, "Phantom.jar")
            
            if not os.path.exists(phantom_internal):
                self.log("❌ ОШИБКА: Phantom.jar не найден в папке internal!")
                messagebox.showerror("Ошибка", "Положи собранный Phantom.jar в папку internal!")
                return
            
            shutil.copy(phantom_internal, phantom_mods)
            self.log("✅ Phantom.jar установлен в mods.")

        else:
            filename = f"{cheat_name.replace(' ', '_')}.jar"
            jar_path = os.path.join(MODS_DIR, filename)
            if not os.path.exists(jar_path):
                self.log(f"❌ ОШИБКА: Файл {filename} не найден в папке mods!")
                return

        self.log(f"▶ Запуск игры с {cheat_name}...")
        try:
            java_path = "javaw.exe" 
            args = [
                f"-Xmx4G",
                f"-Djava.library.path={MINECRAFT_DIR}\\natives",
                "-cp", f"{MINECRAFT_DIR}\\libraries\\*;{MINECRAFT_DIR}\\versions\\1.21.4\\1.21.4.jar",
                "net.fabricmc.loader.impl.launch.knot.KnotClient"
            ]
            subprocess.Popen([java_path] + args, cwd=MINECRAFT_DIR)
            self.log("✅ Игра успешно запущена!")
        except Exception as e:
            self.log(f"❌ ОШИБКА ЗАПУСКА: {e}")

if __name__ == "__main__":
    app = LauncherApp()
    app.mainloop()
