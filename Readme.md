# CV Classification & RAG System

A production-ready Retrieval-Augmented Generation (RAG) system for CV classification and intelligent search using K-Means clustering and Mistral AI.

## Features

- **2484 CVs Indexed**: Across 24 job categories
- **K-Means Classification**: 72 centroids (3 per category) for multi-profile matching
- **Vector Search**: Semantic search with 384-dimensional embeddings (Sentence Transformers)
- **Intelligent LLM**: ChatMistralAI with conversation memory and fallback responses
- **Hybrid Search**: Classification filtering + semantic similarity for optimal results
- **Production-Ready**: Clean, optimized codebase with ~60% space efficiency

## Quick Start

### Prerequisites
- Python 3.10+
- Qdrant Docker container running on port 6333
- Mistral API key (for LLM features)

### Installation

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r src/requirements.txt

# Start Qdrant (if not running)
docker run -d -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### Usage

```bash
# Initialize database (parse PDFs, generate embeddings, train classifier)
python3 src/main_enhanced.py init

# Run interactive chat
python3 src/main_enhanced.py chat

# View classification statistics
python3 src/main_enhanced.py stats
```

## Architecture

```
Document Pipeline:
  PDF Files → Parser → Embedder → K-Means Classifier → Qdrant Storage

Search Pipeline:
  Query → Embedder → Classifier Filter → Vector Search → LLM Response
```

## Core Modules

- `src/ingestion/parser.py`: PDF text extraction
- `src/embeddings/embedder.py`: Sentence Transformers embeddings (384-dim)
- `src/classification/classifier.py`: K-Means clustering with 72 centroids
- `src/storage/vector_store.py`: Qdrant vector database integration
- `src/retrieval/enhanced_retriever.py`: Hybrid search with classification
- `src/llm/client.py`: ChatMistralAI integration with fallbacks
- `src/pipeline/enhanced_rag_pipeline.py`: End-to-end initialization pipeline
- `src/main_enhanced.py`: CLI interface

## Configuration

- **Embedding Model**: all-MiniLM-L6-v2 (384-dim vectors)
- **Clustering**: K-Means with n_init=10, random_state=42
- **Categories**: 24 job categories with 3 centroids each
- **Vector DB**: Qdrant (COSINE similarity distance)
- **LLM**: ChatMistralAI (Mistral Large with fallback responses)

## Performance

- Initialization: ~2-3 minutes for 2484 CVs
- Classification filtering: ~24x faster than exhaustive search
- Search response: <1s typical (with LLM response)

## Environment Variables

```bash
export MISTRAL_API_KEY="your_api_key_here"
```

## Status

 **Production Ready** - All features tested and validated
- K-Means classification: 100% functional
- PDF parsing: 2484 CVs processed
- Vector storage: 4967 points in Qdrant
- LLM chat: Real ChatMistralAI with intelligent fallbacks
- Hybrid search: Classification-aware retrieval working