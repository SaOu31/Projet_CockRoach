# Projet CockroachDB - Haute Disponibilité & Performance

##  Résultats Clés
- **Performance** : Optimisation via Index/STORING -> Latence de **4ms**.
- **Résilience** : Cluster de 3 nœuds avec tolérance aux pannes.
- **Backup** : Sauvegardes automatisées vers stockage S3 (MinIO).

## Installation
1. `docker-compose up -d`
2. `python3 seed.py` (Peuplement de 10 000 lignes)
3. `python3 test_panne.py` (Test de résilience)
