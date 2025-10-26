from fastapi import FastAPI, status
import schemas 
import security 
from datetime import datetime

#inicializar la aplicación FastAPI
app = FastAPI(title="Servicio de Usuarios", version="1.0.0")

# Endpoint raíz
@app.get("/")
def read_root():
    return {"message": "Bienvenido al Servicio de Usuarios"}

# Endpoint para registrar un nuevo usuario
@app.post(
    "/auth/register",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(user_in: schemas.UserCreate):
    
    # Encriptar - Hashear la contraseña usando nuestra función de security.py
    
    hashed_password = security.get_password_hash(user_in.password)
    
    # Imprimimos los datos en la terminal (para demostración)
    print("--- Usuario Registrado (Datos Seguros) ---")
    print(f"Username: {user_in.username}")
    print(f"Email: {user_in.email}")
    print(f"Hashed Password: {hashed_password}") # Imprimimos el HASH de la contraseña
    
    # SIMULACIÓN (Aún hay base de datos)
    # En el siguiente paso, guardaríamos 'hashed_password' en la BD,
    # no 'user_in.password'.
    
    fake_user_db = {
        "id":1,
        "username": user_in.username,
        "email": user_in.email,
        "created_at":datetime.now()
    }
    
    # La respuesta sigue siendo la misma.
    # El 'response_model=schemas.UserRead' se asegura de que
    # NUNCA devolvamos el hash (ni la contraseña) al cliente.
    return fake_user_db