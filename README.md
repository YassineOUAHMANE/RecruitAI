# Assistant RH 



### 1. Créer l’environnement virtuel et installer les dépendances
```bash
python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```

### 2. Lancer Qdrant avec Docker
```bash
docker run -d \
  -p 6333:6333 \
  -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

### 3. Créer un fichier `.env` avec votre clé Mistral
```env
MISTRAL_API_KEY=ta_clef_mistral
```

---

## Utilisation

Lancez le script principal :
```bash
python3 src/main.py
```
