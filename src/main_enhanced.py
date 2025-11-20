"""
Enhanced main.py with classification support.

Two modes:
1. initVectorDataBase() - Initialize with classification (run once)
2. runLLM() - Interactive chat with classification-aware RAG
"""

from retrieval.enhanced_retriever import retriever
from pipeline.enhanced_rag_pipeline import EnhancedRAGPipeline
from llm.client import LLMClient
from config.settings import settings
from classification.classifier import CVClassifier


def initVectorDataBase():
    """
    Initialize the vector database with CV embeddings and classifications.
    
    This should be run only once when first setting up the system.
    It will:
    1. Parse all CVs from the data folders
    2. Generate embeddings for each CV
    3. Build the classifier with category centroids
    4. Store everything in Qdrant with metadata
    """
    print("\n" + "=" * 70)
    print(" INITIALIZING VECTOR DATABASE WITH CLASSIFICATION")
    print("=" * 70)

    pipeline = EnhancedRAGPipeline(
        base_path=settings.DATA_PATH,
        model_embedding="all-MiniLM-L6-v2",
        vector_db="qdrant",
        num_centroids_per_category=3,  # 3 different skill profiles per job category
    )

    stats = pipeline.run()

    print("\n Initialization Summary:")
    print(f"   - Total CVs processed: {stats['total_cvs']}")
    print(f"   - Job categories: {stats['num_categories']}")
    print(f"   - Embedding dimension: {stats['embeddings_dimension']}")
    print(f"   - Centroid profiles per category: {stats['centroids_per_category']}")
    print("\nDatabase ready! You can now run runLLM() for interactive chat.\n")


def runLLM():
    """
    Run the interactive LLM chatbot with classification-aware RAG.
    
    The assistant will:
    1. Understand job descriptions
    2. Classify them into skill categories
    3. Find relevant CVs using both semantic and classification filtering
    4. Present results with classification insights
    """

    print("\n" + "=" * 70)
    print("STARTING HR ASSISTANT WITH CLASSIFICATION AWARENESS")
    print("=" * 70)

    # Load classifier if it exists
    try:
        classifier = CVClassifier()
        classifier_path = settings.get("CLASSIFIER_PATH", "src/classification/models/classifier.pkl")
        classifier.load(classifier_path)
        print(f" Classifier loaded from {classifier_path}")
        print(f"  Loaded {len(classifier.centroids)} categories with centroids\n")
        
        # Attach classifier to retriever for enhanced search
        retriever.classifier = classifier
    except Exception as e:
        print(f" Classifier not found ({e})")
        print("  Run initVectorDataBase() first to create the classifier\n")
        classifier = None

    # Initialize LLM with enhanced retriever tool
    # TODO: Implement LLM agent integration
    # For now, just show a message
    # tools = [rag_with_classification]
    # llm = LLMClient(tools, "mistral-large-latest")
    # agent = llm.get_agent()

    print("=" * 70)
    print("HR Assistant is ready! (type 'quit' to exit)")
    print("=" * 70)
    print("\n Tips:")
    print("   - Describe a job opening to find matching CVs")
    print("   - The system will classify the job and find relevant profiles")
    print("   - CVs are classified into multiple skill categories")
    print("\n")

    # Initialize LLM client
    llm_client = LLMClient()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        try:
            # Step 1: Get conversational response from LLM
            llm_response = llm_client.chat(user_input)
            
            # Step 2: Try to search for CVs if the user is asking for candidates
            search_keywords = ["cherche", "search", "find", "looking", "recherche", "candidat", "candidate", "cv", "profil", "profile", "engineer", "developer", "ingénieur", "développeur", "manager", "designer"]
            should_search = any(keyword in user_input.lower() for keyword in search_keywords)
            
            if should_search:
                results, classifications = retriever.search(user_input, top_k=3)
                
                if results:
                    print(f"\nHR Assistant: {llm_response}")
                    print("\n Profils correspondants trouvés:\n")
                    for i, result in enumerate(results, 1):
                        print(f"   {i}. [{result['source_category']}] Similarité: {result['similarity_score']:.3f}")
                        print(f"      {result['text_preview'][:200]}...\n")
                else:
                    print(f"\nHR Assistant: {llm_response}\n")
            else:
                print(f"\nHR Assistant: {llm_response}\n")

        except Exception as e:
            print(f"\nError: {str(e)}\n")


def showClassificationStats():
    """Display statistics about the classifier."""
    try:
        classifier = CVClassifier()
        classifier_path = settings.get("CLASSIFIER_PATH", "src/classification/models/classifier.pkl")
        classifier.load(classifier_path)

        print("\n" + "=" * 70)
        print("CLASSIFICATION STATISTICS")
        print("=" * 70)

        print(f"\nTotal categories: {len(classifier.centroids)}")
        print("\nCategories and their centroids:")
        print("-" * 70)

        for category, centroids in classifier.centroids.items():
            num_centroids = len(centroids)
            print(f"  • {category:30s} → {num_centroids} centroid(s)")

        print("\n" + "=" * 70 + "\n")

    except Exception as e:
        print(f"\nCould not load classifier: {e}")
        print("Run initVectorDataBase() first.\n")


def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "init":
            initVectorDataBase()
        elif command == "chat":
            runLLM()
        elif command == "stats":
            showClassificationStats()
        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python main.py init   - Initialize database with classifications")
            print("  python main.py chat   - Run interactive chat")
            print("  python main.py stats  - Show classification statistics")
    else:
        # Default behavior: check if database is initialized
        print("\n" + "=" * 70)
        print("HR ASSISTANT - ENHANCED WITH CLASSIFICATION")
        print("=" * 70)
        print("\nUsage:")
        print("  python main.py init   - Initialize database with classifications")
        print("  python main.py chat   - Run interactive chat")
        print("  python main.py stats  - Show classification statistics")
        print("\nFirst run: python main.py init")
        print("Then:      python main.py chat\n")
        

if __name__ == "__main__":
    main()
