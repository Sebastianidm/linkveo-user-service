from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import  jwt  

#CONSTANTES DE SEGURIDAD
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Duración del token en minutos


# Configurar el contexto de cifrado de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear una contraseña
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Función para verificar una contraseña
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Función para crear un token de acceso
def create_access_token(data: dict):
    #copiar los datos para no modificar el original
    to_encode = data.copy()
    # Calcular la fecha de expiración del token
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Añadimos la expiracion a los datos a codificar
    to_encode.update({"exp": expire})
    # crear el token JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt