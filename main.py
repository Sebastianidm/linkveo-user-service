from fastapi import FastAPI, status, Depends, HTTPException # <--- 1. Importar Depends y HTTPException
from sqlalchemy.orm import Session # <--- 2. Importar Session

import schemas 
import security 
import models
import crud # <--- 3. Importar nuestro nuevo archivo crud
from database import engine, get_db # <--- 4. Importar get_db de database

# Esta línea crea la tabla si no existe (ya la teníamos)
models.Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI(title="Servicio de Usuarios", version="1.0.0")

# Endpoint raíz (sin cambios)
@app.get("/")
def read_root():
    return {"message": "Bienvenido al Servicio de Usuarios"}

# --- 5. ENDPOINT DE REGISTRO 100% FUNCIONAL ---
@app.post(
    "/auth/register",
    response_model=schemas.UserRead, # (Sin cambios)
    status_code=status.HTTP_201_CREATED, # (Sin cambios)
)
# --- 6. Inyectar la dependencia de la BD ---
async def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # --- 7. Validar que el email no exista ---
    db_user = crud.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    # --- 8. Validar que el username no exista ---
    db_user_username = crud.get_user_by_username(db, username=user_in.username)
    if db_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already registered"
        )
    
    # --- 9. Hashear la contraseña (esto ya lo teníamos) ---
    hashed_password = security.get_password_hash(user_in.password)
    
    # --- 10. Llamar a CRUD para crear el usuario ---
    # ¡Ya no hay simulación! Esta es la escritura real en la BD.
    new_user = crud.create_user(db=db, user=user_in, hashed_password=hashed_password)
    
    # Devolvemos el nuevo usuario creado
    return new_user