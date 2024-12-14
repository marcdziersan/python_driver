# Fahrzeugsteuerung in Python

Dieses Projekt implementiert eine einfache Fahrzeugsteuerung für ein Auto, das sich auf einer Rennstrecke bewegt. Die Steuerung erfolgt über die Tastatur und ermöglicht es dem Fahrzeug, zu beschleunigen, zu bremsen, zu lenken und sich zu drehen. Die Anwendung ist mit `tkinter` für die Benutzeroberfläche und `Pillow` für die Bildbearbeitung erstellt.

## Features

- **Fahrzeugbewegung**: Das Fahrzeug kann durch Tastenanschläge beschleunigt und abgebremst werden.
- **Lenkung**: Das Fahrzeug kann durch Tastensteuerung nach links und rechts gedreht werden.
- **Kollisionserkennung**: Das Fahrzeug bleibt innerhalb der vorgegebenen Grenzen des Fensters.
- **Fahrzeugbild**: Das Fahrzeug wird als Bild auf dem Canvas angezeigt und rotiert, um der Bewegungsrichtung zu entsprechen.

## Anforderungen

Um das Projekt auszuführen, müssen die folgenden Python-Bibliotheken installiert sein:

- `tkinter` (für die GUI)
- `Pillow` (für die Bildverarbeitung)

Installiere die erforderlichen Bibliotheken mit pip:

```bash
pip install pillow
```

**Hinweis**: `tkinter` ist normalerweise bereits in der Standardinstallation von Python enthalten.

## Installation und Verwendung

1. Klone das Repository oder lade die Dateien herunter.
2. Stelle sicher, dass du ein Fahrzeugbild (`auto.png`) im selben Verzeichnis wie das Skript hast. Du kannst jedes beliebige 50x50 px Bild verwenden.
3. Starte die Anwendung, indem du das Skript ausführst:

```bash
python fahrzeugsteuerung.py
```

4. Steuere das Fahrzeug mit den folgenden Tasten:
   - **W** / **Pfeil nach oben** / **KP 8**: Beschleunigen
   - **S** / **Pfeil nach unten** / **KP 2**: Bremsen
   - **A** / **Pfeil nach links** / **KP 4**: Nach links drehen
   - **D** / **Pfeil nach rechts** / **KP 6**: Nach rechts drehen
   - **Space**: Sanftes Bremsen

## Anwendung

1. Die Fahrzeugsteuerung funktioniert auf einer virtuellen Rennstrecke, die durch zwei Ovale dargestellt wird: eines für die äußeren Begrenzungen der Strecke und eines für den inneren Bereich (Grasbereich).
2. Das Fahrzeug kann sich frei auf der Strecke bewegen, aber es bleibt innerhalb der Begrenzungen, die durch die Fenstergröße vorgegeben sind.
3. Du kannst das Fahrzeug nach Belieben steuern und mit den Tasten die Richtung und Geschwindigkeit ändern.

## Codeerklärung

### Hauptkomponenten

- **FahrzeugSteuerung**: Die Hauptklasse, die die Steuerung des Fahrzeugs und die Logik der Bewegung implementiert.
- **zeichne_rennstrecke**: Diese Methode zeichnet die Rennstrecke als zwei Ovale – eines für die äußeren Ränder der Strecke und eines für die innere "Gras"-Region.
- **taste_druecken und taste_loslassen**: Diese Methoden registrieren Tasteneingaben, um die Steuerungsbefehle des Fahrzeugs zu steuern.
- **update**: Die Hauptaktualisierungsschleife, die das Fahrzeug basierend auf den aktuellen Steuerbefehlen bewegt, die Geschwindigkeit anpasst und die Fahrzeugposition aktualisiert.
- **innerhalb_grenzen**: Eine Methode, die überprüft, ob das Fahrzeug innerhalb der Grenzen des Canvas bleibt.
- **drehe_auto**: Diese Methode dreht das Fahrzeugbild basierend auf dem aktuellen Drehwinkel des Fahrzeugs.

### Steuerungslogik

- **Beschleunigung**: Wenn die W-Taste (oder die Pfeiltaste nach oben oder KP 8) gedrückt wird, wird die Geschwindigkeit des Fahrzeugs erhöht, bis die maximale Geschwindigkeit erreicht ist.
- **Bremsen**: Wenn die S-Taste (oder die Pfeiltaste nach unten oder KP 2) gedrückt wird, wird das Fahrzeug verlangsamt. Die Bremskraft wird ebenfalls durch die Space-Taste kontrolliert.
- **Drehung**: Das Fahrzeug kann sich um 3 Grad pro Schritt drehen, wenn die Tasten A (oder Pfeil nach links oder KP 4) bzw. D (oder Pfeil nach rechts oder KP 6) gedrückt werden.

### Fahrzeuggrenzen

Das Fahrzeug bleibt innerhalb der Grenzen des Canvas und bewegt sich nicht über den Rand hinaus. Dies wird durch die Methode `innerhalb_grenzen` sichergestellt, die prüft, ob das Fahrzeug innerhalb des sichtbaren Bereichs des Fensters bleibt.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert – siehe die [LICENSE](LICENSE)-Datei für Details.
```

### Erläuterungen:
- **Features**: Diese Sektion hebt die wichtigsten Funktionen des Programms hervor, wie Fahrzeugsteuerung, Lenkung und Kollisionserkennung.
- **Anforderungen**: Diese Sektion listet die notwendigen Python-Bibliotheken auf.
- **Installation und Verwendung**: Erklärt, wie man das Projekt installiert und startet.
- **Codeerklärung**: Gibt eine kurze Erklärung zu den wichtigsten Komponenten des Codes, um das Verständnis zu erleichtern.
- **Beispiel**: Du kannst einen Screenshot oder eine Animation deines Programms hinzufügen, um das Aussehen der Anwendung zu zeigen.
- **Lizenz**: Standardlizenzhinweis, der angepasst werden kann, je nachdem, welche Lizenz du verwenden möchtest.

Diese Dokumentation bietet eine vollständige Übersicht und eine benutzerfreundliche Anleitung zur Nutzung deines Projekts.
