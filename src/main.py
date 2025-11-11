from langchain_core.tools import tool
from llm.client import LLM
from retrieval.retriever import rag
from pipeline.rag_pipeline  import RAGPipeline  




def initVectorDataBase():
    pipeline = RAGPipeline(base_path="/home/moussaoui/langchain-chatbot/data/data",model_name="all-MiniLM-L6-v2",vector_db="qdrant")
    pipeline.run()


def runLLM():

    tools = [rag]
    llm = LLM("mistral-small", tools)

    chat_with_memory = llm.getChat_with_memory()
    session_id = llm.getSession_id()

    print("Assistant RH prêt à discuter! (tape 'quit' pour quitter)\n")

    while True:
        user_input = input("Vous : ")
        if user_input.lower() in ["quit", "exit"]:
            print("Fin.")
            break

        response = chat_with_memory.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}},
        )

        print("Assistant RH :", response["output"])





def main():
    # initVectorDataBase() #ceci doit etre lancé juste une seule fois pour intialiser la base vectoreil 

    runLLM()


main()
