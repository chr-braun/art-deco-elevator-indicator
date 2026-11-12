# Elevator Indicator

Eine Art-déco-Stockwerksanzeige, die statt der Etagen **FREI** oder **BESETZT** zeigt. Ein Servo schwenkt den Zeiger, Home Assistant steuert ihn per Präsenzmelder, und ein optionales Fahrstuhl-„Ding“ meldet den Wechsel.

Animierte Projektseite: [`index.html`](index.html). Bebilderte Bauanleitung: [`docs/anleitung.html`](docs/anleitung.html). Teileliste: [`PARTS.md`](PARTS.md). English version: [`README.md`](README.md).

## Kurzbau

1. `laser/01_base-plate.svg` und `laser/02_bezel-pointer.svg` auf 4 mm Sperrholz lasern (erst gravieren, dann schneiden, Platte nicht bewegen).
2. Drehpunktloch der Grundplatte von vorn auf 12 mm aufbohren, Blende aufleimen.
3. Zuerst `3d-print/fit-test-nodemcu.stl` drucken und das Board prüfen, dann Kästchen, Deckel und Haken-Hülsen drucken.
4. `home-assistant/secrets.yaml.example` nach `secrets.yaml` kopieren, ausfüllen, `elevator-indicator-nodemcu.yaml` mit ESPHome flashen (erstes Flashen per USB **ohne** Servo).
5. Servo verdrahten: braun an `G`, rot an `VIN` (5 V), orange an `D5`, Elko parallel an 5 V und Masse.
6. Zeiger auf das Servo-Horn kleben und in Home Assistant mit den Reglern „Zeiger FREI“ und „Zeiger BESETZT“ einstellen.
7. Mit `laser/wall-hook-drill-template.svg` an die Wand hängen und die Automation aus `home-assistant/automation.yaml` anlegen.

## Hinweise

* Zeigerwerte: Die Startwerte im YAML (-63 / +63) sind grob. Beim Original passen **FREI = 100** und **BESETZT = -50**. Läuft der Zeiger falsch herum, Vorzeichen tauschen.
* Rücklauf auf FREI nach **5 Sekunden** ohne Präsenz, der Ping kommt 2 Sekunden nach dem Umschalten. Bei `media_player.play_media` **nicht** `announce: true` verwenden (HomePod über Music Assistant blieb damit stumm).
* Eine eigene `elevator-ding.mp3` in Home Assistant unter *Medien → Lokale Medien* ablegen. Eine Sounddatei liegt dem Repository nicht bei.
* Servo vor dem Drucken nachmessen (Welle 6,0 mm vom Gehäuseende, Lochabstand der Laschen 27,8 mm), Werte in `source/druck_nodemcu.py` ändern und die STL neu erzeugen.
* Lizenz CC BY-NC-SA 4.0. Schriften: Limelight und Cinzel Decorative (SIL OFL 1.1).
