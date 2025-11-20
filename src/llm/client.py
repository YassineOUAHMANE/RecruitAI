"""
LLM Client module - Handles interactions with Language Models.
Currently supports Mistral AI via LangChain.
"""

from typing import Optional, List
import os
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage


class ConversationMemory:
    """Simple conversation memory to track chat history."""
    
    def __init__(self):
        self.buffer = []
    
    def load_memory_variables(self) -> dict:
        return {"history": "\n".join(self.buffer[-10:])}  # Last 10 messages
    
    def save_context(self, inputs: dict, outputs: dict) -> None:
        self.buffer.append(f"User: {inputs.get('input', '')}")
        self.buffer.append(f"Assistant: {outputs.get('output', '')}")
        # Keep only last 10 exchanges (20 messages)
        if len(self.buffer) > 20:
            self.buffer = self.buffer[-20:]
    
    def clear(self) -> None:
        self.buffer = []


class LLMClient:
    """
    Client for interacting with Mistral language models.
    Supports conversational AI with context and memory.
    """

    def __init__(self, model_name: str = "mistral-large-latest", api_key: Optional[str] = None):
        """
        Initialize the LLM client with Mistral.
        
        Args:
            model_name: Name of the Mistral model (default: mistral-large-latest)
            api_key: Mistral API key (reads from MISTRAL_API_KEY env var if not provided)
        """
        self.model_name = model_name
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        self.llm = None
        self.memory = ConversationMemory()
        self._initialize()

    def _initialize(self):
        """Initialize the LLM."""
        if not self.api_key:
            print("  Warning: MISTRAL_API_KEY not set. Using fallback responses.")
            self.llm = None
            return

        try:
            self.llm = ChatMistralAI(
                model=self.model_name,
                api_key=self.api_key,
                temperature=0.7,
                max_tokens=1024,
            )
            print(f" Mistral LLM initialized ({self.model_name})")
        except Exception as e:
            print(f"  Warning: Could not initialize Mistral LLM: {e}")
            self.llm = None

    def chat(self, message: str, context: Optional[str] = None) -> str:
        """
        Send a message to the LLM and get a response.
        
        Args:
            message: The user message
            context: Optional context (CV search results, etc.)
            
        Returns:
            The LLM response
        """
        if not self.llm:
            return self._fallback_response(message)

        try:
            system_prompt = """You are a professional HR Assistant specializing in CV matching and recruitment.
Your responsibilities include:
- Helping find suitable CV candidates for job positions
- Providing information about candidates
- Answering HR-related questions
- Using CV search results to make personalized recommendations
- Maintaining a professional and helpful tone

Always explain your reasoning when searching for candidates."""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=message)
            ]
            
            if context:
                messages.append(HumanMessage(content=f"\nContext about available CVs:\n{context}"))

            response = self.llm.invoke(messages)
            response_text = response.content.strip()
            
            # Save to memory
            self.memory.save_context(
                {"input": message},
                {"output": response_text}
            )
            
            return response_text

        except Exception as e:
            print(f"  LLM Error: {e}")
            return self._fallback_response(message)

    def generate(self, prompt: str) -> str:
        """
        Generate text from a prompt (one-shot, no memory).
        
        Args:
            prompt: The prompt to generate from
            
        Returns:
            Generated text
        """
        if not self.llm:
            return "I cannot generate text without API key."

        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f" Generation Error: {e}")
            return "Error generating response."

    def _fallback_response(self, message: str) -> str:
        """Provide a fallback response when LLM is not available."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["bonjour", "hello", "hi", "salut", "coucou"]):
            return "Bonjour! Je suis votre assistant HR. Comment puis-je vous aider à trouver des candidats ou obtenir des informations sur les CVs? "
        
        elif any(word in message_lower for word in ["cherche", "search", "find", "looking", "recherche"]):
            return "D'accord! Je vais vous aider à trouver les meilleurs candidats. Décrivez le poste ou le profil que vous recherchez, et je vous montrerai les CVs les plus pertinents."
        
        elif any(word in message_lower for word in ["merci", "thanks", "thank you", "thx"]):
            return "De rien! Avez-vous d'autres questions concernant les candidats? Je suis là pour vous aider! "
        
        elif any(word in message_lower for word in ["quitter", "quit", "exit", "bye", "adieu", "au revoir"]):
            return "Au revoir! Bonne journée et bonne chance avec vos recrutements! "
        
        else:
            return f"Je comprends: \"{message}\". Pour vous aider au mieux, décrivez le type de candidat ou le poste que vous recherchez. Par exemple: 'Je cherche un développeur Python avec 3 ans d'expérience' ou 'Qui peut travailler en finance?'"
