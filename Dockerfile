FROM python:3.11-slim

WORKDIR /app

# Copie les dépendances et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code source, y compris wait-for-it.sh
COPY ./src .

# Rends le script exécutable
COPY ./src/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

EXPOSE 5000

# Lancement : attend que la base de données "db" (service docker) soit prête avant de lancer l’app Flask
CMD ["/wait-for-it.sh", "db:5432", "--", "python", "app.py"]
