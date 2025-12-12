from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from uuid import UUID

from app.schemas.task import Task, TaskCreate, TaskUpdate, Priority
from app.repositories.tasks_repo import repo

from app.api.v1.endpoints.auth import get_current_user
from app.repositories.users_repo import User

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[Task])
async def list_tasks(skip: int = 0,limit: int = 50,completed: Optional[bool] = None,q: Optional[str] = None,priority: Optional[Priority] = None,current_user: User = Depends(get_current_user)):
    """
    Lista tareas con filtros opcionales:
    - completed: true/false
    - q: texto a buscar en título o descripción
    - priority: low | medium | high
    """
    return repo.list(
        owner_id=current_user.id,
        skip=skip,
        limit=limit,
        completed=completed,
        q=q,
        priority=priority,
    )


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate,current_user: User = Depends(get_current_user)):
    """
    Crea una nueva tarea.
    """
    return repo.create(payload, owner_id=current_user.id)


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: UUID):
    """
    Devuelve una tarea por su ID.
    """
    task = repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=Task)
async def replace_task(task_id: UUID, payload: Task):
    """
    Reemplaza completamente una tarea (hay que enviar todo el objeto Task).
    El id de la ruta y el del body deben coincidir.
    """
    if task_id != payload.id:
        raise HTTPException(
            status_code=400,
            detail="Path id and body id mismatch",
        )
    return repo.replace(task_id, payload)


@router.patch("/{task_id}", response_model=Task)
async def update_task(task_id: UUID, payload: TaskUpdate):
    """
    Actualiza parcialmente una tarea (solo los campos que envíes).
    """
    updated = repo.update(task_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID):
    """
    Elimina una tarea por ID.
    """
    deleted = repo.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


@router.post("/complete_all", status_code=status.HTTP_200_OK)
async def complete_all_tasks():
    """
    Marca como completadas todas las tareas que aún no lo estén.
    Devuelve cuántas se han actualizado.
    """
    count = repo.complete_all()
    return {"updated": count}
