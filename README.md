# Lab0-LOG430 – Hello World

[![CI](https://github.com/zakzaki244/Lab0-LOG430/actions/workflows/ci.yml/badge.svg)](https://github.com/zakzaki244/Lab0-LOG430/actions)

## Description
Ce dépôt contient une mini-application Python qui affiche « Hello, World ! ».

## Prérequis
- Git  
- Python 3.11+  
- Docker & Docker Compose  

## Installation et exécution

1. **Cloner le projet**  
   ```bash
   git clone https://github.com/zakzaki244/Lab0-LOG430.git
   cd Lab0-LOG430

2. **Environnement Python**  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   
3. **Lancer l'application**  
   ```bash
   python app.py

4. **Tests unitaires**  
   ```bash
   pytest -q

5. **Docker Compose**  
   ```bash
   docker compose up --build

## Pipeline CI/CD
À chaque push ou pull request sur main :
- Lint (flake8)
- Tests (pytest)
- Build & Push (Docker)


## Structure
<pre>
Lab0-LOG430/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── tests/
│   └── test_app.py
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
</pre>

