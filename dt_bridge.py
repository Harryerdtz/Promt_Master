#!/usr/bin/env python3
"""
Prompt Studio + Draw Things Bridge
----------------------------------
Startet die Seite (index.html neben dieser Datei) unter http://localhost:8080
und leitet alle /sdapi/*-Anfragen an Draw Things (http://127.0.0.1:7860) weiter.
So gibt es keine Browser-Sperre (CORS).

Start:  python3 dt_bridge.py
Stop:   Strg+C
Optional:  PORT=9000 DT_URL=http://127.0.0.1:7860 python3 dt_bridge.py
"""
import base64
import glob
import http.server
import json
import os
import shutil
import socketserver
import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser

DT_URL = os.environ.get("DT_URL", "http://127.0.0.1:7860").rstrip("/")
PORT = int(os.environ.get("PORT", "8080"))

# PyInstaller entpackt gebündelte Dateien in ein temporäres Verzeichnis.
# Die UI wird dort gelesen, der veränderliche Zustand aber dauerhaft im
# Benutzerordner gespeichert, damit er einen App-Neustart überlebt.
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    ROOT = sys._MEIPASS
    DATA_ROOT = os.path.join(os.path.expanduser("~/Library/Application Support"), "PromptMaster")
else:
    ROOT = os.path.dirname(os.path.abspath(__file__))
    DATA_ROOT = ROOT
os.makedirs(DATA_ROOT, exist_ok=True)
DATA_FILE = os.path.join(DATA_ROOT, "prompt_studio_data.json")
if DATA_ROOT != ROOT and not os.path.exists(DATA_FILE):
    bundled_state = os.path.join(ROOT, "prompt_studio_data.json")
    if os.path.isfile(bundled_state):
        shutil.copy2(bundled_state, DATA_FILE)
MAX_STATE_BYTES = 30 * 1024 * 1024
IMG_DIR = os.path.join(DATA_ROOT, "ps_images")
MAX_IMAGE_BYTES = 80 * 1024 * 1024


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def _proxy(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else None
        req = urllib.request.Request(
            DT_URL + self.path, data=body, method=self.command,
            headers={"Content-Type": self.headers.get("Content-Type", "application/json")},
        )
        try:
            with urllib.request.urlopen(req, timeout=3600) as r:
                data, status = r.read(), r.status
                ctype = r.headers.get("Content-Type", "application/json")
        except urllib.error.HTTPError as e:
            data, status, ctype = e.read(), e.code, "application/json"
        except Exception as e:
            msg = str(e).replace('"', "'")
            data, status, ctype = ('{"error": "%s"}' % msg).encode(), 502, "application/json"
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, status, obj):
        data = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _state_get(self):
        if not os.path.exists(DATA_FILE):
            return self._json(404, {"error": "noch keine Daten"})
        try:
            with open(DATA_FILE, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self._json(500, {"error": str(e)})

    def _state_post(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_STATE_BYTES:
            return self._json(413, {"error": "Daten zu gross oder leer"})
        try:
            raw = self.rfile.read(length)
            json.loads(raw)
            tmp = DATA_FILE + ".tmp"
            with open(tmp, "wb") as f:
                f.write(raw)
            if os.path.exists(DATA_FILE):
                try:
                    os.replace(DATA_FILE, DATA_FILE + ".bak")
                except OSError:
                    pass
            os.replace(tmp, DATA_FILE)
            self._json(200, {"ok": True})
        except Exception as e:
            self._json(400, {"error": str(e)})

    def _image_post(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_IMAGE_BYTES:
            return self._json(413, {"error": "Bild zu gross oder leer"})
        try:
            data = json.loads(self.rfile.read(length))
            b64 = str(data.get("image", ""))
            if b64.startswith("data:"):
                b64 = b64.split(",", 1)[1]
            img = base64.b64decode(b64)
            if img[:8] == b"\x89PNG\r\n\x1a\n":
                ext = "png"
            elif img[:3] == b"\xff\xd8\xff":
                ext = "jpg"
            elif img[8:12] == b"WEBP":
                ext = "webp"
            else:
                return self._json(400, {"error": "Kein gueltiges Bild"})
            os.makedirs(IMG_DIR, exist_ok=True)
            stamp, n = time.strftime("%Y%m%d_%H%M%S"), 1
            while os.path.exists(os.path.join(IMG_DIR, f"{stamp}_{n:02d}.{ext}")):
                n += 1
            name = f"{stamp}_{n:02d}"
            with open(os.path.join(IMG_DIR, name + "." + ext), "wb") as f:
                f.write(img)
            metadata = {key: data.get(key) for key in ("prompt", "negativePrompt", "model", "seed", "settings", "loras", "createdAt", "rating", "favorite", "collection", "notes")}
            with open(os.path.join(IMG_DIR, name + ".json"), "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False)
            self._json(200, {"ok": True, "file": f"ps_images/{name}.{ext}"})
        except Exception as e:
            self._json(400, {"error": str(e)})

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/state":
            self._state_get()
        elif path == "/api/gallery":
            items = []
            for file in sorted(glob.glob(os.path.join(IMG_DIR, "*.json")), reverse=True):
                try:
                    with open(file, encoding="utf-8") as f:
                        meta = json.load(f)
                    stem = os.path.splitext(os.path.basename(file))[0]
                    image = next((stem + ext for ext in (".png", ".jpg", ".webp") if os.path.isfile(os.path.join(IMG_DIR, stem + ext))), None)
                    if image:
                        items.append({"id": stem, "image": "/api/gallery/image/" + image, **meta})
                except (OSError, ValueError):
                    continue
            self._json(200, {"items": items[:500]})
        elif path.startswith("/api/gallery/image/"):
            name = path.removeprefix("/api/gallery/image/")
            if name != os.path.basename(name) or not name.lower().endswith((".png", ".jpg", ".webp")):
                return self.send_error(404)
            file = os.path.join(IMG_DIR, name)
            if not os.path.isfile(file):
                return self.send_error(404)
            self.send_response(200)
            self.send_header("Content-Type", "image/jpeg" if name.lower().endswith(".jpg") else "image/webp" if name.lower().endswith(".webp") else "image/png")
            self.send_header("Content-Length", str(os.path.getsize(file)))
            self.end_headers()
            with open(file, "rb") as f:
                shutil.copyfileobj(f, self.wfile)
        elif self.path.startswith("/sdapi/"):
            self._proxy()
        elif path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
        elif path in ("/", "/index.html", "/app-design.css"):
            self.path = "/index.html" if path == "/" else path
            super().do_GET()
        else:
            self.send_error(404)

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/state":
            self._state_post()
        elif path == "/api/save-image":
            self._image_post()
        elif path.startswith("/api/gallery/metadata/"):
            name = path.removeprefix("/api/gallery/metadata/")
            if not name or name != os.path.basename(name) or not all(c.isascii() and (c.isalnum() or c in "_-") for c in name):
                return self.send_error(404)
            file = os.path.join(IMG_DIR, name + ".json")
            if not os.path.isfile(file):
                return self.send_error(404)
            length = int(self.headers.get("Content-Length") or 0)
            if length <= 0 or length > 4096:
                return self._json(413, {"error": "Metadaten zu gross oder leer"})
            try:
                changes = json.loads(self.rfile.read(length))
                if not isinstance(changes, dict) or any(k not in ("rating", "favorite", "collection", "notes") for k in changes):
                    return self._json(400, {"error": "Ungueltige Felder"})
                with open(file, encoding="utf-8") as f:
                    meta = json.load(f)
                if "rating" in changes:
                    rating = int(changes["rating"])
                    if not 0 <= rating <= 5: return self._json(400, {"error": "Ungueltige Bewertung"})
                    meta["rating"] = rating
                if "favorite" in changes:
                    meta["favorite"] = bool(changes["favorite"])
                for key in ("collection", "notes"):
                    if key in changes: meta[key] = str(changes[key])[:500]
                tmp = file + ".tmp"
                with open(tmp, "w", encoding="utf-8") as f: json.dump(meta, f, ensure_ascii=False)
                os.replace(tmp, file)
                self._json(200, {"ok": True})
            except (ValueError, OSError, TypeError) as error:
                self._json(400, {"error": str(error)})
        elif self.path.startswith("/sdapi/"):
            self._proxy()
        else:
            self.send_error(404)

    def log_message(self, fmt, *args):
        first_arg = str(args[0]) if args else ""
        if "/sdapi/" in first_arg:
            super().log_message(fmt, *args)


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    url = f"http://localhost:{PORT}"
    print(f"Prompt Studio laeuft: {url}\nDraw Things erwartet unter: {DT_URL}\nDaten werden gesichert in: {DATA_FILE}\nBeenden mit Strg+C")
    if os.environ.get("PROMPT_MASTER_NO_BROWSER") != "1":
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        Server(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nBeendet.")
