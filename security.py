from passlib.context import CryptContext

# Configurar el contexto de cifrado de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear una contraseña
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Función para verificar una contraseña
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)