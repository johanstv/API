from fastapi import APIRouter, Response, status, Header, HTTPException, Depends, Body
from pydantic import BaseModel
from config.db import conn
from models.user import users
from functions_jwt import write_token, validate_token, verify_token
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError, InterfaceError
from schemas.user import UserAuth, UserBd
from starlette.status import HTTP_204_NO_CONTENT
from datetime import datetime, timedelta


user = APIRouter()
    

@user.post("/users")
def create_user(user: UserBd = Body(..., example={
        "nombre": "Juan",
        "email": "juan@example.com",
        "direccion": "Calle 123",
        "edad": 30
    }), token: str = Depends(verify_token)):
    if not user.nombre or not user.email or not user.direccion or not user.edad:
        raise HTTPException(status_code=400, detail="Los campos 'nombre', 'email', 'direccion' y 'edad' no deben estar vacíos")
    try:
        # Con bd
        new_user = {"Nombre": user.nombre, "Email": user.email, "Direccion": user.direccion, "Edad": user.edad}
        result = conn.execute(users.insert().values(new_user))
        return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()
    except:
        raise HTTPException(status_code=422, detail="Error de validación")



@user.get("/users", tags=["Users"])
def get_users(token: str = Depends(verify_token)):
    try:
        result = conn.execute(users.select()).fetchall()
    except (OperationalError, InterfaceError):
        raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
    return result


@user.get("/users/{id}", tags=["Users"])
def get_user(id: str, token: str = Depends(verify_token)):
    user = conn.execute(users.select().where(users.c.id == id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="El usuario no fue encontrado")
    return user



@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(id: str, token: str = Depends(verify_token)):
 user = conn.execute(users.select().where(users.c.id == id)).first()
 if user is None:
     raise HTTPException(status_code=404, detail="El usuario no existe")
 conn.execute(users.delete().where(users.c.id == id))
 return Response(status_code=HTTP_204_NO_CONTENT)




@user.put("/users/{id}", tags=["Users"])
def update_user(id: str, user:UserBd, token: str = Depends(verify_token)):
    result = conn.execute(users.select().where(users.c.id == id)).first()
    if result is None:
        raise HTTPException(status_code=404, detail="No se ha encontrado un usuario con ese 'id'")
    if not user.nombre or not user.email or not user.direccion or not user.edad:
        raise HTTPException(status_code=400, detail="Los campos 'nombre', 'email', 'direccion' y 'edad' no deben estar vacíos")
    conn.execute(users.update().values(Nombre = user.nombre, Email = user.email, Direccion = user.direccion,
    Edad = user.edad).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()


