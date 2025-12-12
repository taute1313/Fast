import json
from pathlib import Path
from uuid import uuid4
from pydantic import BaseModel

DATA_FILE = Path("data") / "users.json"

class User(BaseModel):
    id: str
    username: str
    hashed_password: str

class UsersRepository:
    def __init__(self):
        self._users = {}
        self._load()

    def _load(self):
        if DATA_FILE.exists():
            try:
                raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
                for u in raw:
                    self._users[u["username"]] = User(**u)
            except: pass

    def _save(self):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = [u.model_dump() for u in self._users.values()]
        DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def get_by_username(self, username: str):
        return self._users.get(username)

    def create(self, username, hashed_password):
        if username in self._users:
            return None
        user = User(id=str(uuid4()), username=username, hashed_password=hashed_password)
        self._users[username] = user
        self._save()
        return user

repo = UsersRepository()
