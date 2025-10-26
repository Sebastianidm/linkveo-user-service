from sqlalchemy.orm import Session
import models
import schemas

# FUNCIONES DE LECTURA (Read)

def get_user_by_email(db: Session, email: str):
    """
    Busca un usuario por su email.
    Devuelve el usuario si lo encuentra, o None si no.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    """
    Busca un usuario por su username.
    Devuelve el usuario si lo encuentra, o None si no.
    """
    return db.query(models.User).filter(models.User.username == username).first()

# FUNCIÓN DE ESCRITURA (Create)

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    # 1. Creamos un objeto "User" de SQLAlchemy (un modelo)
    #    con los datos del schema Pydantic.
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password # ¡Guardamos el hash!
    )

    # 2. Añadimos ese objeto a la sesión de la BD
    db.add(db_user)

    # 3. Confirmamos los cambios (ejecuta el INSERT en la BD)
    db.commit()

    # 4. Refrescamos el objeto (para obtener datos nuevos, como el ID)
    db.refresh(db_user)

    # 5. Devolvemos el nuevo usuario creado
    return db_user