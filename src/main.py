# src/main.py
from langchain_core.tools import tool
from llm.client import LLM


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

# crée notre LLM avec outils
llm = LLM("mistral-small", tools)

chat_with_memory = llm.get2()
session_id = llm.get1()

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
