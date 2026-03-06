# Assistant RH – Lancement rapide

## 1. Créer le fichier `.env`

Créer un fichier `.env` dans   `src/.env`

```env
MISTRAL_API_KEY=your_mistral_api_key_here

LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=Assistant_RH
LANGCHAIN_API_KEY=your_langchain_api_key_here

DB_HOST=db
DB_USER=root
DB_PASSWORD=rootpassword
DB_NAME=recruit_AI

DATA_PATH=/app/data
```


---

## 2. Lancer tous les services

```bash
docker compose up --build
```

---

## 3. Accéder aux services

### Backend API (FastAPI)
- http://localhost:8000

### Frontend
- http://localhost:8001

Accès direct aux interfaces :
- **HR Panel (recruteur)** : http://localhost:8001/hrpanel
- **Candidate (dépôt de CV)** : http://localhost:8001/candidate


### Qdrant (base vectorielle)
- Collection : http://localhost:6333/dashboard#/collections

---

## 4. Arrêter les services

```bash
docker compose down -v
```

---
## 5. Workflow
### Architecture Globale
Vue d'ensemble du système, incluant le Frontend (React), le Backend (FastAPI), le pipeline ML (RAG, Mistral LLM), et la persistance des données (Qdrant, MySQL).
![Workflow](Images/workflow.png)
### Workflow Recruteur (HR Panel)
Séquence des requêtes lorsqu'un recruteur interagit avec le chatbot pour interroger la base de CV via le pipeline RAG.
![Workflow Recruiter](Images/workflow_recruteur.png)
### Workflow Candidat (Dépôt de CV)
Séquence d'ingestion d'un CV : de l'upload par le candidat à l'extraction de texte, la génération d'embeddings, et le stockage en base vectorielle.
![Workflow User](Images/workflow_user.png)
## 6. Application demo

### Interface Chatbot
![Interface Chatbot](Images/Interface-chatbot.png)

### Base de Données Qdrant
![Qdrant Database](Images/Qdrant-Database.png)

### Visualisation CV Chatbot
![Visualisation CV Chatbot](Images/visualisation-cv-chatbot.png)

### Upload CV
![Upload CV](Images/Upload-CV.png)


