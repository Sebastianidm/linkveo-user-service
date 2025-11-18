# 1. Usamos una imagen base de Python (ligera)
FROM python:3.10-slim

# 2. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos la "lista de ingredientes"
COPY requirements.txt .

# 4. Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto del código de tu carpeta al contenedor
COPY . .

# 6. Le decimos al contenedor qué puerto vamos a usar
EXPOSE 8000

# 7. El comando para encender el motor cuando arranque el contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]