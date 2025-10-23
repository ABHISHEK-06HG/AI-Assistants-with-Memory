"""
Core AI Assistant Module
Handles Gemini 2.5 Pro integration and conversation logic
"""

import os
import google.generativeai as genai
from typing import List, Dict, Any
from memory import MemoryManager

class AIAssistant:
    """
    Core AI Assistant using Gemini 2.5 Pro with memory integration
    """
    
    def __init__(self):
        """
        Initialize the AI Assistant
        """
        # Configure Gemini API
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # Initialize Gemini model
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Initialize memory manager
        self.memory_manager = MemoryManager()
        
        # System prompt for the assistant
        self.system_prompt = """You are a helpful AI assistant with long-term memory. 
        You can remember previous conversations and provide contextually relevant responses.
        Be friendly, helpful, and informative in your responses."""
    
    def process_message(self, user_input: str) -> str:
        """
        Process user message and generate response
        
        Args:
            user_input: User's message
            
        Returns:
            Assistant's response
        """
        try:
            # Search for relevant past conversations
            relevant_memories = self.memory_manager.search_memory(user_input, k=3)
            
            # Get recent conversation history
            recent_history = self.memory_manager.get_conversation_history()
            
            # Build context from memories
            context = ""
            if relevant_memories:
                context += "\n\nRelevant past conversations:\n"
                for memory in relevant_memories:
                    context += f"- {memory['content']}\n"
            
            # Build recent conversation context
            if recent_history:
                context += "\n\nRecent conversation:\n"
                for exchange in recent_history[-3:]:  # Last 3 exchanges
                    context += f"User: {exchange['user']}\nAssistant: {exchange['assistant']}\n"
            
            # Create the full prompt
            full_prompt = f"{self.system_prompt}\n\n{context}\n\nCurrent user message: {user_input}"
            
            # Generate response using Gemini
            response = self.model.generate_content(full_prompt)
            assistant_response = response.text
            
            # Store the conversation in memory
            self.memory_manager.add_conversation(user_input, assistant_response)
            
            return assistant_response
            
        except Exception as e:
            error_message = f"Sorry, I encountered an error: {str(e)}"
            print(f"Error in process_message: {e}")
            return error_message
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get conversation history
        
        Returns:
            List of conversation exchanges
        """
        return self.memory_manager.get_conversation_history()
    
    def clear_memory(self) -> None:
        """
        Clear all stored memory
        """
        self.memory_manager.clear_memory()
    
    def search_memory(self, query: str) -> List[Dict[str, Any]]:
        """
        Search stored memories
        
        Args:
            query: Search query
            
        Returns:
            List of relevant memories
        """
        return self.memory_manager.search_memory(query)
