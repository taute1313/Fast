from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

# Definimos el router (esto es lo que importa tu main.py)
api_router = APIRouter()

# --- 1. MODELO DE DATOS ACTUALIZADO ---
# Aquí es donde le decimos a Python: "Oye, ahora las tareas tienen descripción"
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = ""  # <--- ¡ESTO ES LO NUEVO!
    priority: str = "medium"
    completed: bool = False
    tags: List[str] = []

# Base de datos temporal en memoria
tasks_db = []
current_id = 1

# --- 2. RUTAS DE TAREAS (Endpoints) ---

@api_router.get("/tasks/", response_model=List[Task])
async def get_tasks():
    return tasks_db

@api_router.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    global current_id
    task.id = current_id
    current_id += 1
    tasks_db.append(task)
    return task

@api_router.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    global tasks_db
    tasks_db = [t for t in tasks_db if t.id != task_id]
    return {"message": "Tarea eliminada"}

@api_router.patch("/tasks/{task_id}")
async def update_task(task_id: int, task_update: dict):
    for task in tasks_db:
        if task.id == task_id:
            if "completed" in task_update:
                task.completed = task_update["completed"]
            return task
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


# --- 3. AUTH SIMULADO (Solución al error de bcrypt) ---
# Esto permite que el frontend funcione sin configurar bases de datos complejas ahora mismo.

class UserAuth(BaseModel):
    username: str
    password: str

@api_router.post("/auth/login")
async def login(user: UserAuth):
    # Aceptamos cualquier usuario para que puedas probar la app
    return {"access_token": "token-simulado-123", "token_type": "bearer"}

@api_router.post("/auth/register")
async def register(user: UserAuth):
    return {"message": "Usuario registrado exitosamente"}
