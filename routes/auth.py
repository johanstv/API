from fastapi import APIRouter, Header, Body
from pydantic import BaseModel
from schemas.user import UserAuth, UserBd
from functions_jwt import write_token, validate_token
from fastapi.responses import JSONResponse

auth_routes = APIRouter()


@auth_routes.post("/login")
def login(user: UserAuth = Body(..., example={
        "id": "Cédula/Pasaporte",
        "contraseña": "123/ABC"
    })):
    print(user.dict())
    if user.id == "1726564295" and user.contraseña == "742000":
        return write_token(user.dict())
    else:
        return JSONResponse(content={"Error": "Credenciales no encontradas o incorrectas"}, status_code=404)

