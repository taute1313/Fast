from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os

# Importamos tu router
from app.api.v1.router import api_router

app = FastAPI(title="Task Manager Pro")

# --- SOLUCIÓN DEL ERROR DE CARPETA 'static' ---
# 1. Buscamos dónde está ESTE archivo (main.py)
BASE_DIR = Path(__file__).resolve().parent

# 2. Definimos la ruta a la carpeta static
static_dir = BASE_DIR / "static"

# 3. (Opcional) Si la carpeta no existe, la creamos para que no falle
if not static_dir.exists():
    os.makedirs(static_dir)

# 4. Montamos la carpeta usando la ruta absoluta
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def root():
    # Servimos el index.html usando la ruta absoluta
    index_path = static_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Archivo index.html no encontrado en app/static"}

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

# Incluimos las rutas
app.include_router(api_router)
