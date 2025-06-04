from sqlalchemy import create_engine

DATABASE_URL = "postgresql://log430:UzKlwfV6aLJ9utNb@10.194.32.174:5432/posdb"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("Connexion réussie !")
        print("Version de PostgreSQL :", conn.execute("SELECT version();").fetchone())
except Exception as e:
    print("Erreur de connexion :", e)
