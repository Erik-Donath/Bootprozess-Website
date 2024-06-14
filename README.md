# Bootprozess-Website

## Aufbau
Diese Website ist in Flask unter Python geschrieben worden. Sie enthält:
- Eine Startseite
- Impressum und Quellen
- Bootprozess
    - Windows
    - Linux
    - MacOS
- Quiz mit Leaderboard (Account benötigt)
- Account System - Registrierung, Login, Logout, View, Delete

## Architektur
Die App befindet sich als Python Packet unter 'app/'. Alle HTML Templates befinden sich unter 'app/templates/' und alle verwendeten js, css und andere Ressourcen befinden sich unter 'app/static/'.
Die 'app/__ init __.py' ist für die Initialisierung von Flask und seinen Komponenten zuständig. Unter 'app/database.py' werden alle Datenbank relevanten Systeme deklariert und ggf. initalisiert. 'app/user.py' ist zuständig für alle Nutzer funktionen. Die Dateien 'app/quiz.py', 'app/main.py' und 'app/account.py' definieren die jeweiligen Endpunkte der Website und fügen ggf. eigene Funktionalität hinzu.
Unter 'instance/App.db' befindet sich die Datenbank. Diese enthält die Table 'Users' und 'Contacts'.

## Ausführen
Unter dem Verzeichnis 'Scripts/' befinden sich Windows skripts zum Ausführen und installieren des Servers. ('Scripts/Install.bat', 'Scripts/Run.bat')
Achtung: Install.bat installiert Python und die relevanten Softwarepakete als virtuelle Umgebung unter 'venv/'. Folgende wege exsistieren um die Anwendung auszuführen:
<br>**Der einfachste Weg ist es, die 'Scripts/Run.bat' Datei auszuführen.**

## Datenbank Einträge

+ Users → Table für alle Nutzer
  + id → Id des Nutzers. (Primitiv Key, unique)
  + name → Name des Nutzers. (unique)
  + pwhash → Der Password Hash des Nutzer (Salted, Papered, 128byte)
  + icon → Nutzer Profile (int)
  + score → Der Quiz Score (int)
+ Contacts → Table für die Kontaktanfragen
  + id → Id der Anfrage. (Primitiv Key, unique)
  + firstname → Vorname des Absenders. (string 15)
  + lastname → Nachname des Absenders. (string 15)
  + subject → Nachricht des Absenders. (string 500)

## Hinweis zur Verwendung
Diese Seite wurde für ein benotetes Schulprojekt erstellt und ist keinesfalls in der reellen Produktion zu verwenden. 
Alle Daten im Impressum und Copyright sind reine Show. Dieses Projekt steht unter der MIT License.
