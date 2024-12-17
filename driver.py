import tkinter as tk
from PIL import Image, ImageTk
import math

class FahrzeugSteuerung:
    def __init__(self, master):
        self.master = master
        self.master.title("Fahrzeugsteuerung")
        self.master.geometry("800x600")  # Fenstergröße

        # Canvas für das Fahrzeug
        self.canvas = tk.Canvas(self.master, bg="white", width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

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
        self.ai_auto = self.canvas.create_image(400, 300, image=self.ai_tk_image)

        # Initiale Positionen und Winkel
        self.x, self.y = 100, 300  # Spielerfahrzeug
        self.ai_x, self.ai_y = 400, 300  # Computerfahrzeug
        self.angle = 0
        self.ai_angle = 0

        # Geschwindigkeit
        self.speed = 0
        self.max_speed = 10
        self.acceleration = 0.5
        self.friction = 0.2
        self.brake_force = 1.0
        self.turn_speed = 3.5

        self.ai_speed = 3  # Konstante Geschwindigkeit für den Computer

        # Steuerungszustand
        self.keys = {"w": False, "s": False, "a": False, "d": False, "space": False,
                     "Up": False, "Down": False, "Left": False, "Right": False,
                     "KP_8": False, "KP_2": False, "KP_4": False, "KP_6": False}

        # Fahrzeuggrenzen
        self.auto_width = 50
        self.auto_height = 50
        self.canvas_width = 800
        self.canvas_height = 600

        # Ereignisse für Fenstergrößenänderung
        self.master.bind("<Configure>", self.aktualisiere_fenstergroesse)

        # Tasteneingaben binden
        self.master.bind("<KeyPress>", self.taste_druecken)
        self.master.bind("<KeyRelease>", self.taste_loslassen)

        # Update-Schleife
        self.update()

    def zeichne_rennstrecke(self):
        # Rennstrecke als Rechteck mit einem inneren "Grasbereich"
        self.strecke_aussen = self.canvas.create_oval(50, 50, 750, 550, outline="black", width=3)
        self.strecke_innen = self.canvas.create_oval(200, 150, 600, 450, outline="black", width=3)

        # Rennstrecke einfärben
        self.canvas.create_oval(51, 51, 749, 549, fill="gray", outline="")
        self.canvas.create_oval(201, 151, 599, 449, fill="green", outline="")

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
        self.update_computerfahrzeug()

        # Nächste Aktualisierung
        self.master.after(16, self.update)  # Ca. 60 FPS

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
        center_x, center_y = 400, 300  # Mittelpunkt des inneren Kreises
        radius = 200 # Radius des inneren Kreises
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
        half_width = self.auto_width / 2
        half_height = self.auto_height / 2

        # Grenzen prüfen
        if (new_x - half_width < 0 or
            new_x + half_width > self.canvas_width or
            new_y - half_height < 0 or
            new_y + half_height > self.canvas_height):
            return False
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

# Hauptanwendung starten
if __name__ == "__main__":
    root = tk.Tk()
    app = FahrzeugSteuerung(root)
    root.mainloop()
