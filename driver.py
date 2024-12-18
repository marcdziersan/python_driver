import tkinter as tk
from PIL import Image, ImageTk
import math
import time

class FahrzeugSteuerung:
    def __init__(self, master):
        self.master = master
        self.master.title("Fahrzeugsteuerung")
        self.master.geometry("800x600")

        # Canvas für das Fahrzeug
        self.canvas = tk.Canvas(self.master, bg="white", width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Runden-Counter
        self.runden_label = tk.Label(self.master, text="Spieler Runden: 0 | KI Runden: 0", fg="black", font=("Arial", 14))
        self.runden_label.pack(anchor="nw", padx=10, pady=10)

        # Rennstrecke zeichnen
        self.zeichne_rennstrecke()

        # Spielerfahrzeug laden
        self.original_image = Image.open("auto.png").resize((50, 50))
        self.auto_image = self.original_image
        self.auto_tk_image = ImageTk.PhotoImage(self.auto_image)
        self.auto = self.canvas.create_image(100, 300, image=self.auto_tk_image)

        # Computerfahrzeug laden
        self.original_ai_image = Image.open("debug.png").resize((50, 50))
        self.ai_image = self.original_ai_image
        self.ai_tk_image = ImageTk.PhotoImage(self.ai_image)
        self.ai_auto = self.canvas.create_image(150, 300, image=self.ai_tk_image)

        # Initiale Positionen und Winkel
        self.x, self.y = 100, 300
        self.ai_x, self.ai_y = 150, 300
        self.angle = 0
        self.ai_angle = 0

        # Geschwindigkeit
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.5
        self.friction = 0.2
        self.brake_force = 1.0
        self.turn_speed = 3.5

        self.ai_speed = 1
        self.ai_active = False

        # Steuerungszustand
        self.keys = {"w": False, "s": False, "a": False, "d": False, "space": False,
                     "Up": False, "Down": False, "Left": False, "Right": False,
                     "KP_8": False, "KP_2": False, "KP_4": False, "KP_6": False}

        # Fahrzeuggrenzen
        self.auto_width = 50
        self.auto_height = 50
        self.canvas_width = 800
        self.canvas_height = 600

        # Runden-Counter
        self.spieler_runden = 0
        self.ai_runden = 0
        self.startlinie_gekreuzt_spieler = False
        self.startlinie_gekreuzt_ai = False

        # Ereignisse für Fenstergrößenänderung
        self.master.bind("<Configure>", self.aktualisiere_fenstergroesse)

        # Tasteneingaben binden
        self.master.bind("<KeyPress>", self.taste_druecken)
        self.master.bind("<KeyRelease>", self.taste_loslassen)

        # Update-Schleife
        self.last_time = time.time()
        self.frame_count = 0
        self.update()

    def zeichne_rennstrecke(self):
        # Rennstrecke als Oval mit einem inneren "Grasbereich"
        self.strecke_aussen = self.canvas.create_oval(50, 50, 750, 550, outline="red", dash=(5, 20), width=5)
        self.strecke_innen = self.canvas.create_oval(200, 150, 600, 450, outline="red", dash=(5, 20), width=5)

        # Rennstrecke einfärben
        self.canvas.create_oval(51, 51, 749, 549, fill="gray", outline="")
        self.canvas.create_oval(201, 151, 599, 449, fill="green", outline="")

        # Start- und Ziellinie hinzufügen
        start_x, start_y = 50, 300
        laenge = 150
        winkel = math.radians(0)

        # Neue Endkoordinaten berechnen
        end_x = start_x + laenge * math.cos(winkel)
        end_y = start_y + laenge * math.sin(winkel)

        # Linie zeichnen
        self.startlinie = self.canvas.create_line(start_x, start_y, end_x, end_y, fill="white", width=3, dash=(5, 5))

    def taste_druecken(self, event):
        if event.keysym in self.keys:
            self.keys[event.keysym] = True

    def taste_loslassen(self, event):
        if event.keysym in self.keys:
            self.keys[event.keysym] = False

    def aktualisiere_fenstergroesse(self, event):
        # Aktualisiere die Canvas-Größe basierend auf der Fenstergröße
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()

    def update(self):
        # Spielerfahrzeug-Logik
        self.update_spielerfahrzeug()

        # Computerfahrzeug-Logik
        if self.ai_active:
            self.update_computerfahrzeug()

        # FPS aktualisieren
        self.update_fps()

        # Runden-Counter aktualisieren
        self.update_runden_counter()

        # Nächste Aktualisierung
        self.master.after(15, self.update)

    def update_spielerfahrzeug(self):
        # Beschleunigung oder Verzögerung anwenden
        if self.keys["w"] or self.keys["Up"] or self.keys["KP_8"]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif self.keys["s"] or self.keys["Down"] or self.keys["KP_2"]:
            self.speed = max(self.speed - self.acceleration, -self.max_speed / 2)
        elif self.keys["space"]:
            if self.speed > 0:
                self.speed = max(self.speed - self.brake_force, 0)
            elif self.speed < 0:
                self.speed = min(self.speed + self.brake_force, 0)
        else:
            if self.speed > 0:
                self.speed = max(self.speed - self.friction, 0)
            elif self.speed < 0:
                self.speed = min(self.speed + self.friction, 0)

        # KI aktivieren, wenn der Spieler losfährt
        if not self.ai_active and self.speed != 0:
            self.ai_active = True

        # Bewegung basierend auf Geschwindigkeit
        new_x = self.x + self.speed * math.sin(math.radians(self.angle))
        new_y = self.y - self.speed * math.cos(math.radians(self.angle))

        if self.innerhalb_grenzen(new_x, new_y):
            self.x, self.y = new_x, new_y

        # Drehung nur bei Bewegung
        if self.speed > 0.1 or self.speed < -0.1:
            if self.keys["a"] or self.keys["Left"] or self.keys["KP_4"]:
                self.angle = (self.angle - self.turn_speed) % 360
            if self.keys["d"] or self.keys["Right"] or self.keys["KP_6"]:
                self.angle = (self.angle + self.turn_speed) % 360

        # Fahrzeugbild rotieren und Position aktualisieren
        self.drehe_auto()
        self.canvas.coords(self.auto, self.x, self.y)

    def update_computerfahrzeug(self):
        # Computerfahrzeug bewegt sich entlang eines festen Kreises
        center_x, center_y = 400, 300
        radius = 200
        # Winkel aktualisieren (Konstante Geschwindigkeit)
        self.ai_angle = (self.ai_angle + self.ai_speed) % 360

        # Neue Position berechnen
        self.ai_x = center_x + radius * math.cos(math.radians(self.ai_angle))
        self.ai_y = center_y + radius * math.sin(math.radians(self.ai_angle))

        # Fahrzeugbild rotieren und Position aktualisieren
        self.drehe_ai_auto()
        self.canvas.coords(self.ai_auto, self.ai_x, self.ai_y)

    def innerhalb_grenzen(self, new_x, new_y):
        # Berechne die Fahrzeuggrenzen
        center_x, center_y = new_x, new_y

        # Ovalgrenzen (außen)
        oval_left, oval_top, oval_right, oval_bottom = 50, 50, 750, 550
        outer_center_x = (oval_left + oval_right) / 2
        outer_center_y = (oval_top + oval_bottom) / 2
        outer_radius_x = (oval_right - oval_left) / 2
        outer_radius_y = (oval_bottom - oval_top) / 2

        # Punkt im äußeren Oval prüfen
        if ((center_x - outer_center_x) ** 2) / (outer_radius_x ** 2) + ((center_y - outer_center_y) ** 2) / (outer_radius_y ** 2) > 1:
            return False

        # Ovalgrenzen (innen)
        oval_left, oval_top, oval_right, oval_bottom = 200, 150, 600, 450
        inner_center_x = (oval_left + oval_right) / 2
        inner_center_y = (oval_top + oval_bottom) / 2
        inner_radius_x = (oval_right - oval_left) / 2
        inner_radius_y = (oval_bottom - oval_top) / 2

        # Punkt im inneren Oval prüfen
        if ((center_x - inner_center_x) ** 2) / (inner_radius_x ** 2) + ((center_y - inner_center_y) ** 2) / (inner_radius_y ** 2) < 1:
            return False

        # Fahrzeug befindet sich zwischen den Ovalsgrenzen
        return True

    def drehe_auto(self):
        # Spielerfahrzeugbild drehen basierend auf dem Winkel
        self.auto_image = self.original_image.rotate(-self.angle)
        self.auto_tk_image = ImageTk.PhotoImage(self.auto_image)
        self.canvas.itemconfig(self.auto, image=self.auto_tk_image)

    def drehe_ai_auto(self):
        # Computerfahrzeugbild drehen basierend auf dem Winkel
        self.ai_image = self.original_ai_image.rotate(-self.ai_angle)
        self.ai_tk_image = ImageTk.PhotoImage(self.ai_image)
        self.canvas.itemconfig(self.ai_auto, image=self.ai_tk_image)

    def update_runden_counter(self):
        # Spieler überquert die Ziellinie
        if self.x <= 50 and not self.startlinie_gekreuzt_spieler:
            self.spieler_runden += 1
            self.startlinie_gekreuzt_spieler = True
        elif self.x > 50:
            self.startlinie_gekreuzt_spieler = False

        # KI überquert die Ziellinie
        if self.ai_x <= 50 and not self.startlinie_gekreuzt_ai:
            self.ai_runden += 1
            self.startlinie_gekreuzt_ai = True
        elif self.ai_x > 50:
            self.startlinie_gekreuzt_ai = False

        #// // // Noch nicht fertig implementiert
        # Runden-Counter aktualisieren
        self.runden_label.config(text=f"Spieler Runden: {self.spieler_runden} | KI Runden: {self.ai_runden}")
        # print(f"Spieler Runden: {self.spieler_runden} | KI Runden: {self.ai_runden}")

    def update_fps(self):
        # Berechnung der FPS
        self.frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - self.last_time
        if elapsed_time >= 1.0:
            fps = self.frame_count / elapsed_time
            print(f"FPS: {fps:.2f}")
            self.last_time = current_time
            self.frame_count = 0

# Hauptanwendung starten
if __name__ == "__main__":
    root = tk.Tk()
    app = FahrzeugSteuerung(root)
    root.mainloop()
