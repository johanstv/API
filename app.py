from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from routes.user import user
from routes.auth import auth_routes
from dotenv import load_dotenv
import jwt


app = FastAPI(
       title="MyAPI",
       description="Johan Ordóñez",
       openapi_tags=[
          
      {"name":"Auth", "description": "Autenticación de usuarios"},
      {"name":"Users", "description": "Información de usuarios"}

       ]
)


app.include_router(auth_routes, prefix="/api", tags=["Auth"])
app.include_router(user, prefix="/api", tags=["Users"])


load_dotenv()


