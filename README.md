# 🎨 Prompt Master — Universal AI Prompt Studio Ultra

> **Ein mächtiges, browserbasiertes Tool zum Erstellen, Verwalten und Exportieren von Prompts für KI-Bildgenerierung (Stable Diffusion, Midjourney, NovelAI, etc.)** — mit Fokus auf Anime, Hentai & Realistic Styles.

[![Live Demo](https://img.shields.io/badge/Live-Demo-purple?style=for-the-badge&logo=github)](https://harryerdtz.github.io/Promt_Master/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)](index.html)
[![Vanilla JS](https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=flat&logo=javascript&logoColor=black)](index.html)
[![No Build Step](https://img.shields.io/badge/No_Build-Required-brightgreen)](index.html)

---

## ✨ Features

### 🎯 **Prompt-Building**
- **Tag-basierte Auswahl** — Klickbare Chips für Characters, Outfits, Poses, Settings, Lighting, Quality, etc.
- **Multi-Style Support** — Anime • Realistic • Hentai (NSFW-Toggle)
- **Negative Prompts** — Ein-Klick Negative-Embeddings & Quality-Booster
- **Custom Tags** — Eigene Tags speichern, bearbeiten, löschen (persistiert in `localStorage`)
- **Presets** — Fertige Prompt-Vorlagen laden/speichern/teilen

### 🔧 **LoRA & Model Management**
- **LoRA-Slots** (bis zu 5) mit Weight-Slider (0–2.0)
- **Trigger-Word Auto-Injection** — LoRA-Triggers werden automatisch in den Prompt eingefügt
- **Model Presets** — SDXL, SD 1.5, Pony, NovelAI, Illustrious, NoobAI, Flux, HiDream, u.v.m.
- **Style-Switcher** — Anime / Realistic mit dedizierten Tag-Sets

### 📤 **Export & Integration**
- **Kopieren** — Prompt + Negative Prompt in die Zwischenablage
- **JSON Export/Import** — Vollständiger State (Tags, LoRAs, Settings, Custom Tags, Presets)
- **PNG Info Chunk** — Prompt-Metadaten direkt in generierte Bilder einbetten (A1111/ComfyUI-kompatibel)
- **Civitai / HuggingFace Links** — Direkt zu Model/LoRA-Seiten springen

### 🎨 **UI/UX**
- **Dark Theme** mit neon-accented Gradients (SFW/NSFW/LoRA/Custom)
- **Responsive Grid** — Sidebar (Tags) + Sticky Output-Panel rechts
- **Akkordeon-Sections** — Platzsparend, aufklappbar, Tag-Counter
- **Filter-Modes** — All / SFW / NSFW Tag-Filter
- **Toast-Notifications** — Feedback für Copy, Save, Import, Errors
- **Keyboard Shortcuts** — `Ctrl+Enter` (Copy), `Ctrl+Shift+E` (Export), `Ctrl+Shift+I` (Import)

---

## 🚀 Quick Start

```bash
# Klonen & lokal öffnen
git clone https://github.com/Harryerdtz/Promt_Master.git
cd Promt_Master
open index.html        # macOS
# oder: xdg-open index.html  # Linux
# oder: start index.html     # Windows
```

**Oder direkt im Browser:** https://harryerdtz.github.io/Promt_Master/

> **Kein Build, keine Dependencies, kein Server** — reine `index.html` öffnen und loslegen.

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
- Aktive LoRAs zeigen Trigger im Promout-Output (`<lora:name:weight>`).

### 4. **Negative Prompts**
- Unten im Output-Panel: Negative Tags genauso hinzufügen.
- Presets: `Quality Booster`, `Anatomy Fix`, `Bad Hands`, etc.

### 5. **Exportieren**
| Action | Shortcut | Ergebnis |
|--------|----------|----------|
| **Copy Prompt** | `Ctrl+Enter` | Prompt + Negative in Clipboard |
| **Export JSON** | `Ctrl+Shift+E` | `prompt-master-backup.json` (voller State) |
| **Import JSON** | `Ctrl+Shift+I` | State aus Datei wiederherstellen |
| **Save as PNG Info** | — | Bild mit eingebetteten Prompt-Metadaten |

### 6. **Presets nutzen**
- `Presets` Section → fertige Prompt-Kombis laden
- Eigene Presets: `Save as Preset` → Name geben → wiederverwendbar

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Aktion |
|----------|--------|
| `Ctrl / Cmd + Enter` | Prompt + Negative Prompt kopieren |
| `Ctrl / Cmd + Shift + E` | JSON-Export herunterladen |
| `Ctrl / Cmd + Shift + I` | JSON-Import (Datei-Dialog) |
| `Escape` | Offene Dropdowns/Toasts schließen |

---

## 🗂 Project Structure

```
Promt_Master/
├── index.html      # 🎯 Einzige Datei — alles drin (HTML + CSS + JS)
└── README.md       # Diese Datei
```

**Architektur:** Single-file Vanilla ES6 Module Pattern (IIFE), State in `localStorage`, zero dependencies.

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

---

## 💾 Data Persistence

Alles wird im **localStorage** gespeichert (Key: `promptMasterState`):
- Aktive Tags (SFW/NSFW/Custom/Extras/Negative)
- LoRA-Slots (Name, Trigger, Weight, Enabled)
- Custom Tags & Presets
- Model-Auswahl, Style, Filter-Mode
- Letzte Prompt-Ausgabe

> **Privatsphäre:** Keine Daten verlassen deinen Browser. Kein Tracking, keine Analytics.

---

## 🌐 Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chrome / Edge | 90+ | ✅ Full |
| Firefox | 88+ | ✅ Full |
| Safari | 15+ | ✅ Full |
| Mobile Safari/Chrome | iOS 15+ / Android 10+ | ✅ Touch-optimiert |

Benötigt: `localStorage`, `Blob`, `FileReader`, `Clipboard API` (HTTPS/localhost).

---

## 🤝 Contributing

1. Fork repo
2. Branch: `git checkout -b feature/amazing-thing`
3. Changes in `index.html` machen
4. Commit: `git commit -m "feat: amazing thing"`
5. Push & PR öffnen

**Ideen:** Neue Tag-Kategorien, Model-Presets, Export-Formate, Accessibility, i18n, Themes.

---

## 📄 License

**MIT License** — frei für privat & kommerziell. Siehe [LICENSE](LICENSE).

---

## 🙏 Credits & Inspiration

- **Tag-Datenbank** — Community-Listen (Danbooru, Civitai, NovelAI, Pony Diffusion)
- **UI Patterns** — Automatic1111 WebUI, ComfyUI, NovelAI Prompt Editor
- **Icons** — Inline SVGs, Unicode-Symbole
- **Fonts** — Inter (Google Fonts), Fira Code (Monospace)

---

## 📞 Support & Links

| Link | Beschreibung |
|------|--------------|
| [🐛 Issues](https://github.com/Harryerdtz/Promt_Master/issues) | Bugs, Feature-Requests |
| [💬 Discussions](https://github.com/Harryerdtz/Promt_Master/discussions) | Fragen, Showcase, Tipps |
| [🌐 Live Demo](https://harryerdtz.github.io/Promt_Master/) | Sofort ausprobieren |

---

<div align="center">

**Made with 💜 for the AI Art Community**

*Prompt Master — Because prompting shouldn't be painful.*

</div>