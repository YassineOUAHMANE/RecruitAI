# src/llm/client.py
from json import loads
import uuid
from ml_pipeline.retrieval.retriever import rag
from langchain_mistralai import ChatMistralAI
from langchain.messages import HumanMessage, AIMessage
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import os
from dotenv import load_dotenv

from ml_pipeline.pipeline.rag_pipeline  import RAGPipeline
from ml_pipeline.config.settings import settings

from qdrant_client import QdrantClient

load_dotenv()

class LLM:

    def __init__(self, tools : list, model_name = "mistral-large-latest", temperature = 0.3):
        self.model_name = model_name
        self.tools = tools
        self.temperature = temperature
        
        # llm Mistral
        llm = ChatMistralAI(
            api_key=os.getenv("MISTRAL_API_KEY"),
            model=self.model_name,
            temperature=self.temperature
        )

        prompt = "Tu es un assistant RH expert en recrutement. Si l'utilisateur décrit un poste ou un profil recherché, résume les informations qu'il te donne et appelle la fonction `rag` pour trouver les meilleurs CV correspondants. Sinon, aide-le de manière claire et concise. Voici la liste des catégories que tu peux utiliser pour la fonction rag : accountant, advocate, agriculture, apparel, arts, automobile, aviation, banking, bpo, buisiness-development, chef, construction, consultant, designer, digital-media, engineering, finance, fitness, healthcare, hr, information-technology, public-relations, sales, teacher"

        # agent
        self.agent = create_agent(
            model = llm,
            tools = self.tools,
            system_prompt= prompt,
            checkpointer = InMemorySaver()
            )
        
        # historique des messages
        self.messages = []
        
    def get_agent(self):
        return self.agent
    

    def get_messages(self):
        return self.messages
    
    def add_input_to_messages(self, input):
        self.messages.append(HumanMessage(input))

    def add_response_to_messages(self, response):
        self.messages.append(AIMessage(response))
        
        


class llm_client:
    def __init__(self):
        

        

        tools=[rag]
        llm = LLM(tools, "mistral-large-latest")

        self.agent = llm.get_agent()




    def call_llm(self, user_input):

        message_id = str(uuid.uuid4())

        response = self.agent.invoke(
            {
                "messages": [
                    {"role": "system", "content": f"message_id={message_id}"},
                    {"role": "user", "content": user_input}
                ]
            },
            {"configurable": {"thread_id": "1"}}
        )


        tool_messages = [
            msg for msg in response["messages"] 
            if msg.type == "tool"
        ]

        cv_ids = []

        for msg in response["messages"]:
            if msg.type == "tool":
                tool_data = loads(msg.content)
                if tool_data.get("message_id") == message_id:
                    cv_ids = tool_data.get("cv_ids", [])
                    break


        if cv_ids is None:
            cv_ids = []

        return {
            "text": response["messages"][-1].content,
            "files": cv_ids
        }

