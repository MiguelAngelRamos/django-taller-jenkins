# Utilizamos una imagen oficial de Python ligera (slim) para reducir el tamaño
FROM python:3.11-slim

# Configuramos variables de entorno cruciales para Python en contenedores
# 1. Evita que Python genere archivos .pyc en el disco
ENV PYTHONDONTWRITEBYTECODE=1
# 2. Asegura que los logs de stdout y stderr se emitan en tiempo real (útil para ver logs de Docker)
ENV PYTHONUNBUFFERED=1

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero solo el archivo de requerimientos (Optimización de caché de Docker)
COPY requirements.txt /app/

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código fuente al contenedor
COPY . /app/

# Exponemos el puerto en el que correrá Django
EXPOSE 8000

# Ejecutamos las migraciones (opcional aquí, pero útil para desarrollo) 
# y levantamos el servidor exponiéndolo a cualquier IP (0.0.0.0) para que sea accesible desde fuera del contenedor
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]