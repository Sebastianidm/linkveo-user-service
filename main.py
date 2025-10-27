from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm 


from sqlalchemy.orm import Session
import schemas 
import security 
import models
import crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicio de Usuarios", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Servicio de Usuarios"}


@app.get("/users/me", response_model=schemas.UserRead)
async def read_users_me(
    current_user: models.User = Depends(security.get_current_user)
):
    """
    Obtiene los detalles del usuario actualmente autenticado.
    
    Este endpoint está PROTEGIDO. Requiere un token JWT válido.
    """
    # Gracias a 'Depends(security.get_current_user)', esta función
    # SÓLO se ejecutará si el token es válido.
    # La variable 'current_user' ya contendrá los datos del usuario
    # que viene de la base de datos.
    
    return current_user

@app.post(
    "/auth/register",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    
    db_user = crud.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    db_user_username = crud.get_user_by_username(db, username=user_in.username)
    if db_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already registered"
        )
    
    hashed_password = security.get_password_hash(user_in.password)
    
    new_user = crud.create_user(db=db, user=user_in, hashed_password=hashed_password)
    
    return new_user


@app.post("/auth/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # 1. Buscamos al usuario en la BD por su USERNAME
    #    (form_data.username es el campo 'username' del formulario)
    db_user = crud.get_user_by_username(db, username=form_data.username)

    # 2. Si el usuario NO existe O la contraseña es incorrecta
    if not db_user or not security.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}, # Estándar de OAuth2
        )
    
    # 3. Si todo es correcto, creamos el token
    access_token = security.create_access_token(
        data={"sub": db_user.username} # "sub" (subject) es el estándar para el ID del token
    )
    
    # 4. Devolvemos el token
    return {"access_token": access_token, "token_type": "bearer"}