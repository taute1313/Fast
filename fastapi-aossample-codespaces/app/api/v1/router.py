from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Optional
import hashlib
import secrets

api_router = APIRouter(prefix="/api/v1")

# Esquema para obtener el token desde el frontend
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- MODELOS DE DATOS ---

class User(BaseModel):
    username: str
    password: str

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = ""
    priority: str = "medium"
    completed: bool = False
    owner: str = None  # <--- NUEVO: La tarea pertenece a alguien

# --- BASE DE DATOS EN MEMORIA ---
users_db = []      # Lista de usuarios registrados
sessions_db = {}   # Diccionario de tokens activos { "token_abc": "usuario_juan" }
tasks_db = []      # Lista de todas las tareas
current_task_id = 1

# --- FUNCIONES DE SEGURIDAD (Sin librerías externas para evitar errores) ---

def hash_password(password: str) -> str:
    """Encripta la contraseña usando SHA256 (nativo de Python)"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Verifica el token y devuelve el usuario dueño de la sesión"""
    user_owner = sessions_db.get(token)
    if not user_owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_owner

# --- ENDPOINTS DE AUTENTICACIÓN ---

@api_router.post("/auth/register")
async def register(user: User):
    # 1. Comprobar si el usuario ya existe
    for u in users_db:
        if u.username == user.username:
            raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    # 2. Guardar usuario con contraseña encriptada
    new_user = User(username=user.username, password=hash_password(user.password))
    users_db.append(new_user)
    return {"message": "Usuario creado exitosamente"}

@api_router.post("/auth/login")
async def login(user: User):
    hashed_input = hash_password(user.password)
    
    # 1. Buscar usuario y verificar contraseña
    user_found = None
    for u in users_db:
        if u.username == user.username and u.password == hashed_input:
            user_found = u
            break
    
    if not user_found:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    
    # 2. Generar un token único y guardarlo en la "sesión"
    token = secrets.token_hex(16)
    sessions_db[token] = user_found.username # Asociamos el token al usuario
    
    return {"access_token": token, "token_type": "bearer"}

# --- ENDPOINTS DE TAREAS (PROTEGIDOS) ---

@api_router.get("/tasks/", response_model=List[Task])
async def get_tasks(current_user: str = Depends(get_current_user)):
    # FILTRO: Solo devolvemos las tareas que pertenecen al usuario actual
    user_tasks = [t for t in tasks_db if t.owner == current_user]
    return user_tasks

@api_router.post("/tasks/", response_model=Task)
async def create_task(task: Task, current_user: str = Depends(get_current_user)):
    global current_task_id
    
    # ASIGNACIÓN: Marcamos la tarea como propiedad del usuario actual
    task.id = current_task_id
    task.owner = current_user 
    current_task_id += 1
    
    tasks_db.append(task)
    return task

@api_router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, current_user: str = Depends(get_current_user)):
    global tasks_db
    # BORRADO SEGURO: Solo borramos si el ID coincide Y el dueño es el usuario actual
    tasks_db = [t for t in tasks_db if not (t.id == task_id and t.owner == current_user)]
    return {"message": "Tarea eliminada (si existía y era tuya)"}

@api_router.patch("/tasks/{task_id}")
async def update_task(task_id: int, task_update: dict, current_user: str = Depends(get_current_user)):
    for task in tasks_db:
        # EDICIÓN SEGURA: Solo si es tu tarea
        if task.id == task_id and task.owner == current_user:
            if "completed" in task_update:
                task.completed = task_update["completed"]
            return task
    raise HTTPException(status_code=404, detail="Tarea no encontrada o no tienes permiso")
