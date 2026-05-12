FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
# ne garde pas le cahce de télécharchement dans l'image docker
RUN pip install --no-cache-dir -r requirements.txt

# On ne copie que le code important pas tout 
COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# 0.0.0.0 = accessible depuis l’extérieur du conteneur via Docker
# 127.0.0.1 = seulement dans le conteneur