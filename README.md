# Bootprozess-Website

## Aufbau
Diese Website ist in Flask unter Python geschrieben worden. Sie enthält:
- Eine Startseite
- Impresum
- Quellen
- Bootprozess
    - Generell
    - Windows
    - Linux
- Quiz mit Leaderboard und Registrierung

## Architektur
Die App befindet sich als Python Packet unter 'app/'. Alle HTML Templates befinden sich dann unter 'app/templates/' und alle verwendeten js, css und andere assets befinden sich unter 'app/static/'.
Die Dateien 'app/main.py' und 'app/quiz.py' enthalten die jeweiligen Endpunkte sowie weiter funktionalitäten.

## Instance
Die Datenbank für das Leaderboard wird unter dem Verzeichnis 'instance/' erstellt. Sie umfasst Nutzerdaten(Nutzername und E-Mail) sowie der Quiz score unverschlüsselt.

## Hinweis zur Verwendung
Diese Seite wurde für ein benotetes Schulprojekt erstellt und ist keinesfalls in der reelen Produktion zu verwenden. Alle Daten im Impresum und Copyright sind reine Show. Dieses Projekt steht unter der MIT License.
