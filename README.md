# Lab1-LOG430 – Client/Serveur 2-tiers (lab1)

[![CI](https://github.com/zakzaki244/Lab0-LOG430/actions/workflows/ci.yml/badge.svg)](https://github.com/zakzaki244/Lab0-LOG430/actions)

## Description
Ce dépôt contient l’application console POS (Point Of Sale) à deux niveaux, réalisée en Python et conteneurisée avec Docker :

- **Client** : interface CLI (`main.py`)  
- **Serveur** : base de données PostgreSQL  

---

## 📋 Instructions

## Prérequis
- Python 3.11  
- Docker & Docker Compose  
- (Optionnel) `venv` ou `virtualenv` pour isoler l’environnement Python  

## Installation locale et exécution

1. **Cloner le projet**  
   ```bash
   git clone https://github.com/zakzaki244/Laboratoires-LOG430.git
   cd Laboratoires-LOG430
   git checkout lab1

2. **Environnement Python**
   Optionnel : créer et activer un environnement virtuel
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   
4. **Lancer l'application**  
   ```bash
   python app.py

5. **Tests unitaires**  
   ```bash
   pytest -q

## Installation Conteneurisation & orchestration 
Lancer l’application et la base PostgreSQL :

1. **Docker Compose**  
   ```bash
   docker compose up --build
   et pour arrêter et supprimer les conteneurs :
   docker-compose down

## Pipeline CI/CD
À chaque push ou pull request sur main :
- Lint (flake8)
- Tests (pytest)
- Build & Push (Docker)

## 🛠️ Choix technologiques

| Composant        | Outil / Bibliothèque | Justification                                                               |
|------------------|----------------------|------------------------------------------------------------------------------|
| Langage          | Python 3.11          | Syntaxe claire, riche écosystème, portable                                   |
| ORM              | SQLAlchemy           | Abstraction SQL/objet, gestion des transactions, compatible PostgreSQL/SQLite |
| Base de données  | PostgreSQL           | ACID, fiable, conteneurisable, scalable                                      |
| Conteneurisation | Docker               | Isolation, reproductibilité, déploiement uniforme                            |
| Orchestration    | Docker Compose       | Lancement multi-conteneurs en une seule commande                             |
| Tests            | pytest               | Fixtures, plugins, large communauté                                          |
| CI/CD            | GitHub Actions       | Intégré au dépôt, workflows “lint → test → build → push” faciles à configurer|

## Explications techniques du code
- **main.py** : interface console, lit commandes, affiche résultats.
- **service.py** : logique métier, règles, orchestration.
- **dao.py** : accès brut à la BD, CRUD sur tes modèles.
- **models.py** : définition des tables/entités métier.
- **db.py** : config et connexion à la BD.
- **SQLAlchemy** : l’ORM qui unit le tout et simplifie tes interactions SQL.

## Structure
<pre>
Laboratoire-LOG430/
├── app.py
├── service.py 
├── dao.py 
├── models.py 
├── db.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── docs/
│   ├── ADR/
│   │   ├── ADR 0001.md
│   │   └── ADR 0002.md
│   ├── UML/
│   │   ├── Cas Utilisation.png
│   │   ├── Diagramme de classe.png
│   │   └── Diagramme de sequence-Enregsitrer une vente.png
│   │   └── Diagramme de sequence-Rechercher un produit.png
│   │   └── Vue Deploiement.png
│   │   └── Vue Implementation.png
│   └── Analyse des besoins.md
├── tests/
│   └── test_app.py
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
</pre>
