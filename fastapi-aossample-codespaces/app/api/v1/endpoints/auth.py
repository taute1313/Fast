from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM
from app.repositories.users_repo import repo as users_repo
from jose import JWTError, jwt

router = APIRouter(tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

class AuthData(BaseModel):
    username: str
    password: str

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None: raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    user = users_repo.get_by_username(username)
    if user is None: raise HTTPException(status_code=401)
    return user

@router.post("/auth/register")
def register(data: AuthData):
    hashed = get_password_hash(data.password)
    user = users_repo.create(data.username, hashed)
    if not user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return {"message": "Usuario creado"}

@router.post("/auth/login")
def login(data: AuthData):
    user = users_repo.get_by_username(data.username)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
