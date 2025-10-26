from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Definimos la URL de nuestra base de datos
# Por ahora, es un archivo local llamado "test.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# (Cuando usemos PostgreSQL en AWS, esta línea será algo como:)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host/dbname"

# 2. Creamos el "motor" (engine) de SQLAlchemy
# connect_args es solo para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Creamos una "Fábrica de Sesiones"
# Esta es la que nos dará las conexiones individuales a la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Creamos una "Base"
# Nuestros modelos (las tablas de la BD) heredarán de esta clase
Base = declarative_base()