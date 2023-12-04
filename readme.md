# KontenKlärer
Der KontenKlärer ist ein Hobby-Projekt zur Analyse von Bank-Transaktionsdaten mit einem Kategorisierungssystem. Es handelt sich hierbei um eine Webseite, auf Basis von Django. Es ist derzeit nicht geplant diese Webseite öffentlich zu hosten. 

![screenshot](screenshots/screenshot.png)

## Installation
Um den KontenKlärer lokal zu hosten, wird grundsätzlich `Python` und `Django` benötigt. `Django` kann dabei auch in einer virtuellen Umgebung betrieben werden. Zur Minimierung des Speicherplatzes wurde die für dieses Projekt verwendete virtuelle Umgebung nicht auf Github mit veröffentlicht. Über die Liste der Dependencies kann eine virtuelle Umgebung passend aufgebaut werden.

## Dependencies
* Python==3.12.0
* Django==4.2.7

# Funktionen
Grunsätzlich handelt es sich bei dem KontenKläerer in der aktuellen Version um eine sehr einfache Umsetzung. Die Funktionen sind bewusst simpel gehalten und werden nach persönlichen Bedarf in der Zukunft gegebenfalls ausgebaut. Eine feste Roadmap gibt es nicht. Die aktuelle Version besitzt den gewünschten minimalen Funktionsumfang.

# Hochladen von CSV-Dateien
Der KontenKlärer erlaubt das Hochladen von CSV-Dateien aus dem Internet-Banking. Aktuell wird nur das Dateiformat der DKB-Bank unterstützt. 