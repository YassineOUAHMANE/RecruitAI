from ml_pipeline.retrieval.retriever import rag
from ml_pipeline.pipeline.rag_pipeline  import RAGPipeline
from ml_pipeline.llm.client import LLM  
from ml_pipeline.config.settings import settings

def initVectorDataBase():
    pipeline = RAGPipeline(base_path = settings.DATA_PATH, model_embedding="all-MiniLM-L6-v2",vector_db="qdrant")
    pipeline.run()

def runLLM():

    tools = [rag]
    llm = LLM(tools, "mistral-large-latest")

    agent = llm.get_agent()

    print("Assistant RH prêt à discuter! (tape 'quit' pour quitter)\n")

    while True:
        user_input = input("Vous : ")
        #llm.add_input_to_messages(user_input)
        #messages = llm.get_messages()
        
        if user_input.lower() in ["quit", "exit"]:
            print("Fin.")
            break

        response = agent.invoke({
            "messages": [
                {"role": "user", "content": user_input},
            ]
        },
        {
            "configurable": {"thread_id": "1"}
        })
        #llm.add_response_to_messages(response)

        print("Assistant RH :", response["messages"][-1].content, "\n")





def main():
    #initVectorDataBase() #ceci doit etre lancé juste une seule fois pour intialiser la base vectoreil 

    runLLM()


main()
