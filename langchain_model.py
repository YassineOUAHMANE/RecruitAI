from dotenv import load_dotenv
import os
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


load_dotenv()


@tool
def multiply(a: int, b: int) -> int:
    """Multiplie deux entiers."""
    return a * b

@tool
def rag(description_poste: str, top_k: int = 5):
    """
    Recherche les CV les plus pertinents pour une description de poste donnée.
    Retourne une liste des meilleurs candidats trouvés.
    """
    res = (
        "Voilà, Houssam est le meilleur ingénieur : "
        "expert en Python, Java et architecture logicielle."
    )
    return {
        "description_poste": description_poste,
        "top_profils": res
    }

tools = [rag, multiply]


llm = ChatMistralAI(
    api_key=os.getenv("MISTRAL_API_KEY"),
    model="mistral-large-latest",
    temperature=0.4,
)

def create_chat_with_memory():
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

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    store = {}

    def get_session_history(session_id: str):
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

    chat_with_memory = RunnableWithMessageHistory(
        agent_executor,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return chat_with_memory
