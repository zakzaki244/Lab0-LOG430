from service import Service

def print_menu():
    print("\n=== SYSTÈME DE CAISSE ===")
    print("1. Rechercher un produit")
    print("2. Enregistrer une vente")
    print("3. Gérer un retour")
    print("4. Consulter le stock")
    print("5. Quitter")

def main():
    svc = Service()

    while True:
        print_menu()
        choice = input("Prompt — choix: ").strip()

        if choice == "1":
            term = input("Terme de recherche (ID, nom ou catégorie) : ")
            results = svc.search(term)
            if not results:
                print("Aucun produit trouvé.")
            for p in results:
                print(f"{p.id}: {p.name} ({p.category}) — {p.price:.2f} $ — stock={p.stock}")

        elif choice == "2":
            print("Entrez les articles (ID puis quantité), 'f' pour finir.")
            cart = []
            while True:
                pid = input("> Produit ID (ou 'f') : ").strip()
                if pid.lower() == "f":
                    break
                qty = input("  Quantité : ").strip()
                cart.append((int(pid), int(qty)))
            try:
                sale_id = svc.sale(cart)
                print(f"Vente #{sale_id} enregistrée.")
            except Exception as e:
                print(f"Erreur : {e}")

        elif choice == "3":
            sid = input("ID de la vente à annuler : ").strip()
            try:
                svc.refund(int(sid))
                print(f"Vente #{sid} annulée.")
            except Exception as e:
                print(f"Erreur : {e}")

        elif choice == "4":
            print("=== ÉTAT DU STOCK ===")
            for p in svc.stock():
                print(f"{p.id}: {p.name} — stock={p.stock}")

        elif choice == "5":
            print("À bientôt !")
            break

        else:
            print("Choix invalide, recommencez.")

if __name__ == "__main__":
    main()
