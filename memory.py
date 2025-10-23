"""
Memory Management Module for AI Assistant
Handles ChromaDB vector storage and LangChain memory integration
"""

import os
from typing import List, Dict, Any
from langchain.memory import ConversationBufferWindowMemory
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings

class MemoryManager:
    """
    Manages long-term memory using ChromaDB and LangChain memory
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize memory manager with ChromaDB
        
        Args:
            persist_directory: Directory to store ChromaDB data
        """
        self.persist_directory = persist_directory
        
        # Initialize embeddings (using Hugging Face embeddings)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize ChromaDB
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )
        
        # Initialize conversation memory (keeps last 10 exchanges)
        self.conversation_memory = ConversationBufferWindowMemory(
            k=10,
            return_messages=True,
            memory_key="chat_history"
        )
        
        # Text splitter for processing long documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def add_conversation(self, user_input: str, assistant_response: str) -> None:
        """
        Add a conversation exchange to memory
        
        Args:
            user_input: User's message
            assistant_response: Assistant's response
        """
        # Add to conversation memory
        self.conversation_memory.save_context(
            {"input": user_input},
            {"output": assistant_response}
        )
        
        # Create document for vector storage
        conversation_text = f"User: {user_input}\nAssistant: {assistant_response}"
        document = Document(page_content=conversation_text)
        
        # Split and add to vector store
        texts = self.text_splitter.split_documents([document])
        self.vectorstore.add_documents(texts)
    
    def search_memory(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant past conversations
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant conversation chunks
        """
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            return [{"content": doc.page_content, "metadata": doc.metadata} for doc in docs]
        except Exception as e:
            print(f"Error searching memory: {e}")
            return []
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get recent conversation history
        
        Returns:
            List of recent conversation exchanges
        """
        memory_variables = self.conversation_memory.load_memory_variables({})
        chat_history = memory_variables.get("chat_history", [])
        
        history = []
        for i in range(0, len(chat_history), 2):
            if i + 1 < len(chat_history):
                history.append({
                    "user": chat_history[i].content,
                    "assistant": chat_history[i + 1].content
                })
        
        return history
    
    def clear_memory(self) -> None:
        """
        Clear all stored memory
        """
        # Clear conversation memory
        self.conversation_memory.clear()
        
        # Clear vector store
        try:
            # Delete the persist directory to clear ChromaDB
            import shutil
            if os.path.exists(self.persist_directory):
                shutil.rmtree(self.persist_directory)
            
            # Reinitialize vectorstore
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        except Exception as e:
            print(f"Error clearing memory: {e}")
