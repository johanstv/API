from typing import Optional
from pydantic import BaseModel

class UserBd(BaseModel):
     nombre: str
     email: str
     direccion: str
     edad: int
    


class UserAuth(BaseModel):
    id:str
    contraseña: str