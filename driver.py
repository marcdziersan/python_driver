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

        # Fahrzeugbild laden
        self.original_image = Image.open("auto.png").resize((50, 50))  # Originalbild
        self.auto_image = self.original_image
        self.auto_tk_image = ImageTk.PhotoImage(self.auto_image)

        # Fahrzeug auf dem Canvas platzieren
        self.auto = self.canvas.create_image(400, 300, image=self.auto_tk_image)

        # Initiale Position und Winkel
        self.x, self.y = 400, 300
        self.angle = 0  # 0 Grad zeigt nach oben

        # Geschwindigkeit
        self.speed = 0
        self.max_speed = 10
        self.acceleration = 0.5
        self.friction = 0.2  # Verzögerung, wenn keine Taste gedrückt wird
        self.brake_force = 1.0  # Bremskraft
        self.turn_speed = 3  # Drehgeschwindigkeit in Grad

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
        strecke_aussen = self.canvas.create_oval(50, 50, 750, 550, outline="black", width=3)
        strecke_innen = self.canvas.create_oval(200, 150, 600, 450, outline="black", width=3)

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

        # Nächste Aktualisierung
        self.master.after(16, self.update)  # Ca. 60 FPS

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
        # Fahrzeugbild drehen basierend auf dem Winkel
        self.auto_image = self.original_image.rotate(-self.angle)
        self.auto_tk_image = ImageTk.PhotoImage(self.auto_image)
        self.canvas.itemconfig(self.auto, image=self.auto_tk_image)

# Hauptanwendung starten
if __name__ == "__main__":
    root = tk.Tk()
    app = FahrzeugSteuerung(root)
    root.mainloop()
