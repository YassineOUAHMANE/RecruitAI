# src/llm/client.py
from dotenv import load_dotenv
import os

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()


class LLM:
    def __init__(self, model: str, tools: list):
        self.model_name = model
        self.tools = tools

        # 1) modèle Mistral
        llm = ChatMistralAI(
            api_key=os.getenv("MISTRAL_API_KEY"),
            model=self.model_name,
            temperature=0.4,
            
        )

        # 2) prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system",
            "Tu es un assistant RH expert en recrutement. "
            "Si l'utilisateur décrit un poste ou un profil recherché, "
            "appelle la fonction `rag` pour trouver les meilleurs CV correspondants. "
            "Sinon, aide-le de manière claire et concise."),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ])

        # 3) agent
        agent = create_tool_calling_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # 4) mémoire de session
        store = {}

        def get_session_history(session_id: str):
            if session_id not in store:
                store[session_id] = InMemoryChatMessageHistory()
            return store[session_id]

        self.chat_with_memory = RunnableWithMessageHistory(
            agent_executor,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

        self.session_id = "rh_session"

    def getSession_id(self):
        return self.session_id

    def getChat_with_memory(self):
        return self.chat_with_memory
