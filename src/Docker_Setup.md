# Docker Compose - Démarrage de l'Application

## Structure

```
Services Docker:
├── FastAPI API (port 8000)
├── MySQL Database (port 3306)
├── Qdrant Vector DB (port 6333/6334)
└── React Frontend (port 8001)
```

## Prérequis

- Docker installé (version 20.10+)
- Fichier `.env` configuré dans le répertoire `src/`

## Configuration (.env)

Avant de démarrer, configurez le fichier `.env`:

```bash
# Mistral API Key (requis pour LLM)
MISTRAL_API_KEY=your-api-key-here

# LangChain (optionnel)
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=
LANGCHAIN_TRACING_V2=false
```

## Démarrage

### Méthode 1: Utiliser le script (recommandé)

```bash
cd src/
./start.sh
```

### Méthode 2: Commandes docker-compose manuelles

```bash
cd src/

# Démarrer les services
docker compose up -d

# Voir les logs
docker compose logs -f

# Voir l'état des services
docker compose ps
```

## Accès aux Services

Après le démarrage (attendre ~30 secondes):

- **API FastAPI**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Frontend React**: http://localhost:8001
- **MySQL**: localhost:3306
- **Qdrant**: localhost:6333

## Arrêt

### Méthode 1: Script (recommandé)

```bash
cd src/
./stop.sh
```

### Méthode 2: Commande manuelle

```bash
cd src/
docker compose down
```

## Logs et Débogage

```bash
cd src/

# Logs en temps réel
docker compose logs -f

# Logs d'un service spécifique
docker compose logs -f api
docker compose logs -f db
docker compose logs -f qdrant

# Entrer dans un conteneur
docker compose exec api bash
docker compose exec db bash
```

## Reconstruction des Images

Si vous modifiez le code:

```bash
cd src/

# Rebuild sans cache
docker compose build --no-cache

# Rebuild et restart
docker compose up -d --build
```

## Dépannage

### Le service API ne démarre pas

1. Vérifier le fichier `.env`
2. Vérifier les logs: `docker compose logs api`
3. S'assurer que le port 8000 est libre: `lsof -i :8000`

### La base de données ne se connecte pas

1. Vérifier que MySQL est en cours d'exécution: `docker compose logs db`
2. Vérifier les credentials dans `.env`

### Problèmes Qdrant

1. Vérifier le port 6333: `lsof -i :6333`
2. Vérifier le volume: `docker volume ls`

## Réinitialiser Complètement

```bash
cd src/

# Arrêter et supprimer tout
docker compose down -v

# Rebuild et restart
docker compose up -d --build
```

## Notes

- Les données MySQL sont persistées dans le volume `db_data`
- Les données Qdrant sont persistées dans le volume `qdrant_storage`
- Les CV uploadés sont stockés dans `server/backend/data`
