# OneClickAI

> Moderne KI-Modelle lokal auf dem eigenen Laptop ausführen – privat, offline und ohne Cloud.

---

## 🚀 Beschreibung

OneClickAI ermöglicht das einfache Herunterladen, Installieren und lokale Ausführen moderner KI-Modelle direkt auf dem eigenen Laptop – komplett offline, privat und ohne Cloud-Abhängigkeit.

Die Anwendung richtet sich an Nutzer:innen, welche lokale KI möglichst einfach nutzen möchten, ohne manuelle Installation, Kommandozeilen oder komplexe Setups.

---

# 🧩 Elemente / Module / Funktionen

## 🖥️ Grafisches Desktop-Interface

Die Anwendung basiert auf einem modernen GUI mit `PySide6` und führt Nutzer Schritt für Schritt durch die Auswahl und Installation passender KI-Modelle.

---

## 🎯 Use-Case Auswahl

Nutzer wählen aus typischen KI-Anwendungsfällen wie:

- 💬 Chat
- ✍️ Schreiben
- 💻 Coding
- 📄 Dokumentanalyse (RAG)
- 🖼️ Vision / Bildverständnis

Basierend darauf empfiehlt die App automatisch geeignete lokale KI-Modelle.

---

## 🤖 Modell-Empfehlungssystem

Die Anwendung bewertet verfügbare Modelle anhand ihrer Fähigkeiten (z. B. Chat, Coding oder Vision) und sortiert sie automatisch nach Eignung.

Dadurch erhalten Nutzer:innen passende Modelle für ihren konkreten Einsatzzweck.

---

## ⬇️ Automatischer Download

Ausgewählte Modelle werden direkt von Hugging Face heruntergeladen.

Features:

- Fortschrittsanzeige
- Geschwindigkeitsanzeige
- Download-Abbruch
- automatische Installation
- automatische Umbenennung zu ausführbaren `.exe`-Dateien

---

## 🚀 Automatisches Starten der KI

Nach dem Download startet OneClickAI das Modell automatisch lokal auf dem Gerät und öffnet die Weboberfläche im Browser.

---

## 🌐 Lokale Weboberfläche

Die Modelle laufen lokal auf:

```txt
http://127.0.0.1:8080
```

Die Nutzung funktioniert ähnlich wie ChatGPT – jedoch vollständig lokal auf dem eigenen Gerät.

---

# 🧠 Wie funktioniert lokale KI auf der CPU?

OneClickAI verwendet sogenannte **Llamafiles**.

Dabei handelt es sich um portable ausführbare Dateien, welche:

- das KI-Modell,
- die Laufzeitumgebung,
- sowie die Inferenz-Engine

in einer einzigen Datei bündeln.

---

## ⚙️ Verwendete Technologien

### llama.cpp

🔗 https://github.com/ggml-org/llama.cpp

`llama.cpp` ist eine hochoptimierte C/C++-Inference-Engine für lokale Large Language Models auf CPUs und GPUs.

Sie ermöglicht effiziente KI-Inferenz direkt auf Consumer-Hardware.

---

### Mozilla Llamafile

🔗 https://github.com/Mozilla-Ocho/llamafile

`llamafile` kombiniert:

- Modellgewichte
- llama.cpp
- Laufzeitumgebung

zu einer einzigen portablen Datei.

Dadurch lassen sich KI-Modelle wie normale Programme starten.

---

## 💡 Warum funktioniert das ohne GPU?

Moderne Open-Source-Modelle können stark quantisiert werden (z. B. Q4, Q5 oder Q8).

Dadurch:

- sinkt der Speicherverbrauch massiv
- CPU-Inferenz wird praktikabel
- selbst Laptops ohne dedizierte GPU können KI lokal ausführen

`llama.cpp` nutzt dafür:

- SIMD-Optimierungen
- Multi-Threading
- AVX / AVX2 / AVX512 CPU-Instruktionen
- optimierte Matrixoperationen
- effiziente Speicherverwaltung

Dadurch lassen sich erstaunlich leistungsfähige Modelle lokal und energieeffizient betreiben.

---

# 📦 Das Distributable (`OneClickAI.exe`)

Die Anwendung wird als einzelnes Windows-Executable bereitgestellt.

## Vorteile

- keine Installation notwendig
- keine Python-Umgebung erforderlich
- portable Nutzung möglich
- vollständig offline nutzbar

---

## Enthaltene Komponenten

Das finale `.exe` bündelt:

- die gesamte PySide6-Oberfläche
- die Downloadlogik
- das Modellmanagement
- alle Python-Abhängigkeiten
- die Launcher-Logik

in einer einzigen ausführbaren Datei.

---

## 🔨 Build / Packaging

Das Distributable wurde gebaut mit:

- Python
- PySide6
- PyInstaller

---

# 🌱 Hintergrund

Dieses Projekt entstand im Rahmen des:

- Climate Week Zürich
- Green Tech Hackathon

Die Idee hinter OneClickAI:

> KI zugänglicher, privater und ressourcenschonender machen.

Anstatt jede Anfrage über entfernte Cloud-Rechenzentren laufen zu lassen, bringt OneClickAI moderne KI direkt auf den eigenen Laptop.

