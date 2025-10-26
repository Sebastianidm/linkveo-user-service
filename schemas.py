#Definir esquemas de datos utilizando Pydantic.
from pydantic import BaseModel, EmailStr
from datetime import datetime

#Esquema para crear un nuevo usuario
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str 

#Esquema para leer un nuevo usuario
class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    #Configuración para permitir la conversión desde objetos ORM si es necesario
    class Config:
        from_attributes = True

#Esquema para el Token de autenticación 
class Token(BaseModel):
    access_token: str
    token_type: str

    