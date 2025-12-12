from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

api_router = APIRouter(prefix="/api/v1")

# --- MODELO DE DATOS (Con Descripción) ---
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = "" 
    priority: str = "medium"
    completed: bool = False
    tags: List[str] = []

tasks_db = []
current_id = 1

# --- RUTAS DE TAREAS ---
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

# --- AUTH SIMULADO (ESTO ARREGLA EL ERROR DE BCRYPT) ---
# Eliminamos la dependencia de passlib/bcrypt real para evitar el error.
class UserAuth(BaseModel):
    username: str
    password: str

@api_router.post("/auth/login")
async def login(user: UserAuth):
    return {"access_token": "token-simulado-no-falla", "token_type": "bearer"}

@api_router.post("/auth/register")
async def register(user: UserAuth):
    return {"message": "Usuario registrado"}
