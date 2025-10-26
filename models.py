from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

# Importamos la 'Base' que creamos en database.py
from database import Base 

class User(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "users" 

    # --- Definición de las columnas ---

    # ID: Llave primaria, se auto-incrementa
    id = Column(Integer, primary_key=True, index=True)

    # Username: Texto, debe ser único, no puede estar vacío
    username = Column(String, unique=True, index=True, nullable=False)

    # Email: Texto, debe ser único, no puede estar vacío
    email = Column(String, unique=True, index=True, nullable=False)

    # Password: Texto, no puede estar vacío (guardaremos el HASH aquí)
    hashed_password = Column(String, nullable=False)

    # Fecha de creación: Se auto-genera con la fecha y hora del servidor
    created_at = Column(DateTime(timezone=True), server_default=func.now())