FROM python:3.11-slim

WORKDIR /app

# On copie juste le requirements, on installe, puis on copie tout le reste
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY ./src .

EXPOSE 5000


CMD ["python", "app.py"]