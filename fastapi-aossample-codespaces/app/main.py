from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

# Carpeta de estáticos (donde estará index.html)
static_dir = Path(__file__).parent / "static"

# Montar /static (por si en el futuro tienes CSS/JS/imágenes)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def root():
    """
    Devuelve la página principal (frontend simple).
    """
    index_path = static_dir / "index.html"
    return FileResponse(index_path)


@app.get("/healthz")
async def healthz():
    """
    Endpoint de salud para comprobar que la API está viva.
    """
    return {"status": "ok", "env": settings.env}


# Rutas de la API (/api/v1/...)
app.include_router(api_router)
