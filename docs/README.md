# Analyse des besoins fonctionnels et non-fonctionnels du système

### 1.1 Fonctionnels

1. **Recherche de produit**
   - Par identifiant  
   - Par nom  
   - Par catégorie  

2. **Enregistrement d’une vente**
   - Sélection de plusieurs produits avec quantités  
   - Calcul du total à payer  
   - Décrémentation automatique du stock  

3. **Gestion des retours**
   - Annuler une vente récente  
   - Réinjection des quantités en stock  

4. **Consultation du stock**
   - Affichage de l’état courant (quantité restante)  

5. **Multi-clients simultanés**
   - 3 postes de caisse (clients CLI) accèdent à la même base  

### 1.2 Non-fonctionnels

On respecte le modèle ACID : 

- **Transactions atomiques**  
  Chaque vente ou annulation est un bloc transactionnel ACID.

- **Cohérence**  
  Pas de sur‐vente grâce à des verrous ou isolation de transactions.

- **Performance**  
  Réponse en < 100 ms pour requêtes de stock ou création de vente.

- **Disponibilité**  
  La base Docker-hostée reste accessible même si un client plante.

- **Portabilité & simplicité**  
  Tout démarre via `docker-compose up`.

- **Sécurité minimale**  
  Aucune injection SQL possible : toute interaction passe par SQLAlchemy (ORM spécifique pour le langage python).
