

from langchain_model import create_chat_with_memory

if __name__ == "__main__":
    print("Assistant RH prêt à discuter! (tape 'quit' pour quitter)\n")

    chat_with_memory = create_chat_with_memory()
    session_id = "rh_session"

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