import psycopg2
import time

# Ici on utilise les noms d'hotes internes du reseau Docker
# C'est plus securise car ces noms ne sont pas accessibles depuis l'exterieur
nodes = [
    "postgresql://root@roach1:26257/defaultdb?sslmode=disable",
    "postgresql://root@roach2:26257/defaultdb?sslmode=disable",
    "postgresql://root@roach3:26257/defaultdb?sslmode=disable"
]

def simulate_traffic():
    print("--- Demarrage du test de haute disponibilite Reseau Interne ---")
    node_index = 0
    
    while True:
        try:
            # Tentative de connexion sur l'un des noeuds du reseau privé
            conn = psycopg2.connect(nodes[node_index], connect_timeout=3)
            conn.set_session(autocommit=True)
            cur = conn.cursor()
            print(f"--- Connexion etablie avec {nodes[node_index].split('@')[1].split(':')[0]} ---")
            
            while True:
                try:
                    cur.execute("INSERT INTO users (nom, email) VALUES ('Test_Interne', 'ha@private.com')")
                    print("Insertion reussie sur le cluster")
                    time.sleep(0.8)
                except Exception as e:
                    print(f"ERREUR : Perte de connexion avec le leader actuel")
                    break 
        except Exception:
            print("Tentative de basculement vers le noeud suivant dans le reseau...")
            node_index = (node_index + 1) % len(nodes)
            time.sleep(2)

if __name__ == "__main__":
    simulate_traffic()