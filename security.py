from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt 
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import crud
import models
from database import get_db

# Constantes 
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Esta es la "magia" de FastAPI. Le dice al endpoint:
# "Para funcionar, necesitas un token, y debes buscarlo
# en la URL '/auth/token'".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# Hashing (sin cambios)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    """
    Dependencia para obtener el usuario actual a partir de un token JWT.
    """
    
    # 1. Definimos la excepción de credenciales inválidas
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub") # El token tiene el ID
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # 4. Buscamos al usuario en la base de datos
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    
    if user is None:
        # Si el usuario del token ya no existe en la BD
        raise credentials_exception
        
    # 5. Devolvemos el objeto 'user' de la base de datos
    return user