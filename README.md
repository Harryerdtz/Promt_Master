# 🎨 Prompt Master — Universal AI Prompt Studio Ultra

> **Ein mächtiges, browserbasiertes Tool zum Erstellen, Verwalten und Exportieren von Prompts für KI-Bildgenerierung (Stable Diffusion, Midjourney, NovelAI, etc.)** — mit Fokus auf Anime, Hentai & Realistic Styles.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)](index.html)
[![Vanilla JS](https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=flat&logo=javascript&logoColor=black)](index.html)
[![Python Bridge](https://img.shields.io/badge/Python_Bridge-Required-3776AB?logo=python&logoColor=white)](dt_bridge.py)

---

## ⚠️ WICHTIG: Das ist eine **lokale App**, keine statische Website

**Das funktioniert NICHT:**
- ❌ Direkt auf GitHub Pages öffnen
- ❌ `index.html` per Doppelklick im Browser öffnen (CORS blockiert Draw Things API)
- ❌ Als "Live Demo" ohne lokalen Server nutzen

**Das MUSS laufen:**
```
Browser (http://localhost:8080) 
    → dt_bridge.py (Python HTTP Server + Proxy auf Port 8080) 
        → Draw Things API (http://127.0.0.1:7860)
```

Ohne laufenden `dt_bridge.py` **und** Draw Things funktioniert: keine Bildgenerierung, kein State-Save, keine LoRA-Ladung, kein PNG-Export.

---

## 🚀 Quick Start (Richtig)

### Voraussetzungen
- **Draw Things** (macOS/iOS App) installiert
- In Draw Things: **Settings → API → Enable** (Port 7860)
- Python 3.8+

### Installation & Start
```bash
# 1. Repo klonen
git clone https://github.com/Harryerdtz/Promt_Master.git
cd Promt_Master

# 2. Draw Things starten & API aktivieren (Port 7860)

# 3. Bridge starten (öffnet Browser automatisch auf localhost:8080)
python3 dt_bridge.py

# Optional: Anderer Port / Draw Things URL
PORT=9000 DT_URL=http://127.0.0.1:7860 python3 dt_bridge.py
```

**Stoppen:** `Strg+C` im Terminal

---

## 📖 Usage Guide

### 1. **Model & Style wählen**
Oben links: Model-Dropdown (SDXL, Pony, Illustrious, …) + Style-Toggle (Anime 🌸 / Realistic 📸).

### 2. **Tags zusammenklicken**
- Sections aufklappen (▾) → Tags anklicken → sie wandern in den **Output-Bereich** (rechts, sticky).
- **Filter** (All / SFW / NSFW) blendet unerwünschte Kategorien aus.
- **Custom Tags** (`+ Custom` Button) → Name + Wert eingeben → dauerhaft gespeichert.

### 3. **LoRAs hinzufügen**
- `+ LoRA` → Name, Trigger-Word, Weight (Slider) → **Add**.
- Aktive LoRAs zeigen Trigger im Prompt-Output (`<lora:name:weight>`).

### 4. **Negative Prompts**
- Unten im Output-Panel: Negative Tags genauso hinzufügen.
- Presets: `Quality Booster`, `Anatomy Fix`, `Bad Hands`, etc.

### 5. **Generieren & Exportieren**
| Action | Shortcut | Ergebnis |
|--------|----------|----------|
| **Generate** | — | Sendet Prompt an Draw Things via Bridge |
| **Copy Prompt** | `Ctrl+Enter` | Prompt + Negative in Clipboard |
| **Export JSON** | `Ctrl+Shift+E` | `prompt-master-backup.json` (voller State) |
| **Import JSON** | `Ctrl+Shift+I` | State aus Datei wiederherstellen |
| **Save as PNG Info** | — | Bild mit eingebetteten Prompt-Metadaten |

### 6. **Presets nutzen**
- `Presets` Section → fertige Prompt-Kombis laden
- Eigene Presets: `Save as Preset` → Name geben → wiederverwendbar

### 7. **Automation / Randomizer**
- `🎲 Assistent` Button → Schritt-für-Schritt Wizard für Batches
- `⚡ Automation` Button → Massen-Generierung mit Randomizer (Pin/Exclude Tags, LoRA Weight Randomization, Partner Modes)

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Aktion |
|----------|--------|
| `Ctrl / Cmd + Enter` | Prompt + Negative Prompt kopieren |
| `Ctrl / Cmd + Shift + E` | JSON-Export herunterladen |
| `Ctrl / Cmd + Shift + I` | JSON-Import (Datei-Dialog) |
| `Escape` | Offene Dropdowns/Toasts schließen |
| `/` | Suchfokus (Tag-Suche) |
| `Enter` (im Wizard) | Weiter / Generieren |

---

## 🗂 Project Structure

```
Promt_Master/
├── index.html                 # 🎯 UI (HTML + CSS + JS, ~200 KB)
├── dt_bridge.py               # 🌉 Python HTTP Server + Draw Things Proxy
├── prompt_studio_data.json    # 💾 Gespeicherter State (Tags, LoRAs, Presets, History)
├── prompt_studio_data.json.bak# 💾 Backup des vorherigen States
├── ps_images/                 # 🖼️ Auto-generierte Bilder + Prompt-.txt (wird erstellt)
└── README.md                  # Diese Datei
```

**Architektur:**
- **Frontend:** Single-file Vanilla ES6 (IIFE), State in `localStorage` + Server-Sync via `/api/state`
- **Backend:** `dt_bridge.py` — `http.server` + Threading, Proxy zu Draw Things `/sdapi/*`, State/Image Persistenz
- **Draw Things:** Lokale macOS App mit aktivierter API (Port 7860)

---

## 🔧 Customization

### Eigene Tag-Kategorien hinzufügen
In `index.html` → `TAG_DATABASE` Object erweitern:

```javascript
const TAG_DATABASE = {
  anime: {
    character: [ "1girl", "solo", "long_hair", ... ],
    outfit:    [ "school_uniform", "dress", ... ],
    // neue Kategorie:
    weather:   [ "rain", "snow", "sunny", "storm" ],
  },
  realistic: { ... },
  nsfw:      { ... },
};
```

### Neue Models registrieren
In `MODEL_PRESETS` Array:

```javascript
{
  id: "my-model",
  name: "My Custom Model",
  type: "sdxl",           // sdxl | sd15 | pony | nai | flux | hidream
  triggerPrefix: "",      // z.B. "score_9, score_8_up, "
  recommendedSteps: 30,
  recommendedCfg: 7,
  tags: ["anime", "sfw"],
}
```

### Theme-Farben anpassen
CSS Custom Properties in `:root` (ganz oben im `<style>` Block):

```css
:root {
  --sfw-color: #3b82f6;
  --nsfw-color: #ff2e93;
  --lora-color: #06b6d4;
  --custom-color: #f59e0b;
  --bg: #05070c;
  --panel: rgba(15, 18, 30, 0.75);
  /* ... */
}
```

Verfügbare Themes: `neon` (Default), `calm`, `night`, `soft` — via `body[data-theme="..."]`.

---

## 💾 Data Persistence

**Drei Speicher-Ebenen:**

| Ebene | Ort | Inhalt |
|-------|-----|--------|
| **Browser** | `localStorage` (`promptMasterState`) | UI-State für schnelles Laden (Tags, Model, Style, Filter) |
| **Server (Bridge)** | `prompt_studio_data.json` | Voller State + LoRAs + Presets + Randomizer-History (persistent, überlebt Browser-Neustart) |
| **Backup** | `prompt_studio_data.json.bak` | Vorheriger Stand vor jedem Save |
| **Bilder** | `ps_images/YYYYMMDD_HHMMSS_XX.png/.txt` | Generierte Bilder + zugehörige Prompts |

> **Privatsphäre:** Alles läuft **lokal**. Keine Daten verlassen deinen Rechner. Kein Tracking, keine Analytics, keine Cloud.

---

## 🌐 Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chrome / Edge | 90+ | ✅ Full |
| Firefox | 88+ | ✅ Full |
| Safari | 15+ | ✅ Full |
| Mobile Safari/Chrome | iOS 15+ / Android 10+ | ✅ Touch-optimiert |

Benötigt: `localStorage`, `Blob`, `FileReader`, `Clipboard API` (nur auf `http://localhost` oder HTTPS).

---

## 🛠️ dt_bridge.py Details

**Endpoints:**
| Method | Path | Beschreibung |
|--------|------|--------------|
| `GET` | `/` | Serviert `index.html` |
| `GET/POST` | `/api/state` | State laden/speichern (JSON) |
| `POST` | `/api/save-image` | Base64-Bild + Prompt → `ps_images/` |
| `*` | `/sdapi/*` | **Proxy** zu Draw Things (löst CORS) |

**Umgebungsvariablen:**
| Variable | Default | Beschreibung |
|----------|---------|--------------|
| `PORT` | `8080` | HTTP Port für Bridge |
| `DT_URL` | `http://127.0.0.1:7860` | Draw Things API Basis-URL |

---

## 🤝 Contributing

1. Fork repo
2. Branch: `git checkout -b feature/amazing-thing`
3. Changes in `index.html` und/oder `dt_bridge.py` machen
4. Commit: `git commit -m "feat: amazing thing"`
5. Push & PR öffnen

**Ideen:** Neue Tag-Kategorien, Model-Presets, Export-Formate, Accessibility, i18n, Themes, Bridge-Features (z.B. Multi-GPU, Queue-Management).

---

## 📄 License

**MIT License** — frei für privat & kommerziell. Siehe [LICENSE](LICENSE).

---

## 🙏 Credits & Inspiration

- **Tag-Datenbank** — Community-Listen (Danbooru, Civitai, NovelAI, Pony Diffusion)
- **UI Patterns** — Automatic1111 WebUI, ComfyUI, NovelAI Prompt Editor
- **Draw Things** — Lokale Stable Diffusion für Apple Silicon (von Liu Liu)
- **Icons** — Inline SVGs, Unicode-Symbole
- **Fonts** — Inter (Google Fonts), Fira Code (Monospace)

---

## 📞 Support & Links

| Link | Beschreibung |
|------|--------------|
| [🐛 Issues](https://github.com/Harryerdtz/Promt_Master/issues) | Bugs, Feature-Requests |
| [💬 Discussions](https://github.com/Harryerdtz/Promt_Master/discussions) | Fragen, Showcase, Tipps |
| [📖 Draw Things](https://drawthings.ai/) | Die erforderliche macOS/iOS App |

---

<div align="center">

**Made with 💜 for the AI Art Community**

*Prompt Master — Because prompting shouldn't be painful. (And it runs locally.)*

</div>