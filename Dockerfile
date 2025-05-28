FROM python:3.11-slim

WORKDIR /app

# On copie juste le requirements, on installe, puis on copie tout le reste
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# **Important** : on copie TOUT le dossier (dont main.py, service.py, dao.py…)
COPY . .

# On démarre main.py (et non plus app.py)
CMD ["python", "main.py"]