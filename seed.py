import psycopg2
from faker import Faker
import time
import random

conn_string = "postgresql://root@localhost:26257/defaultdb?sslmode=disable"

try:
    conn = psycopg2.connect(conn_string)
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    fake = Faker('fr_FR')
    nombre_lignes = 10000

  
    print(" Création de la table user ")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            nom TEXT, prenom TEXT, email TEXT, ville TEXT, 
            date_inscription TIMESTAMP DEFAULT now()
        );
    """)
  
    cur.execute("TRUNCATE TABLE users CASCADE;") 
    
    user_ids = []
    for i in range(nombre_lignes):
        cur.execute(
            "INSERT INTO users (nom, prenom, email, ville) VALUES (%s, %s, %s, %s) RETURNING id",
            (fake.last_name(), fake.first_name(), fake.email(), fake.city())
        )
        user_ids.append(cur.fetchone()[0])
        if (i+1) % 2000 == 0: print(f"  {i+1} users insérés")

  
    print("Création de la table Produit")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS produits (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            nom_produit TEXT, categorie TEXT, prix DECIMAL
        );
    """)
    categories = ['Électronique', 'Mode', 'Maison', 'Sport', 'Loisirs']
    for i in range(1000):
        cur.execute(
            "INSERT INTO produits (nom_produit, categorie, prix) VALUES (%s, %s, %s)",
            (fake.word().capitalize(), random.choice(categories), round(random.uniform(10, 1000), 2))
        )

  
    print(" Création de la table Commandes ")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS commandes (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID, montant DECIMAL, statut TEXT,
            date_commande TIMESTAMP DEFAULT now()
        );
    """)
    statuts = ['Livré', 'En cours', 'Annulé', 'Expédié']
    for i in range(nombre_lignes):
        cur.execute(
            "INSERT INTO commandes (user_id, montant, statut) VALUES (%s, %s, %s)",
            (random.choice(user_ids), round(random.uniform(20, 500), 2), random.choice(statuts))
        )
        if (i+1) % 2000 == 0: print(f"  {i+1} commandes insérées")

    print("\n Le seeding des 3 tables est terminé.")
    cur.close()
    conn.close()

except Exception as e:
    print(f" Erreur lors du seeding : {e}")