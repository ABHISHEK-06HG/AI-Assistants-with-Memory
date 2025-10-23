"""
Streamlit AI Assistant App
Voice + Text Input with Long-term Memory using Gemini 2.5 Pro
"""

import streamlit as st
import os
import tempfile
import whisper
from dotenv import load_dotenv
from assistant import AIAssistant
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Assistant with Memory",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header Styles */
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    /* Chat Message Styles */
    .chat-message {
        padding: 1.5rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
        border-radius: 20px 20px 5px 20px;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        margin-right: 20%;
        border-radius: 20px 20px 20px 5px;
    }
    
    /* Button Styles */
    .stButton > button {
        width: 100%;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Input Styles */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        font-family: 'Poppins', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* File Uploader Styles */
    .stFileUploader > div {
        border-radius: 15px;
        border: 2px dashed #667eea;
        background: rgba(102, 126, 234, 0.05);
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        background: rgba(102, 126, 234, 0.1);
        border-color: #764ba2;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Status Indicators */
    .status-online {
        color: #4CAF50;
        font-weight: bold;
    }
    
    .status-offline {
        color: #f44336;
        font-weight: bold;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        .user-message, .assistant-message {
            margin-left: 0;
            margin-right: 0;
        }
    }
    
    /* Loading Animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

def initialize_assistant():
    """Initialize the AI Assistant"""
    if 'assistant' not in st.session_state:
        try:
            st.session_state.assistant = AIAssistant()
            st.session_state.initialized = True
        except Exception as e:
            st.error(f"Failed to initialize AI Assistant: {str(e)}")
            st.error("Please check your GOOGLE_API_KEY in the .env file")
            st.session_state.initialized = False

def transcribe_audio(audio_file):
    """Transcribe audio file to text using Whisper"""
    try:
        # Load Whisper model (this will download on first run)
        model = whisper.load_model("base")
        
        # Transcribe the audio
        result = model.transcribe(audio_file)
        return result["text"]
    except Exception as e:
        st.error(f"Error transcribing audio: {str(e)}")
        return None

def convert_audio_format(audio_file):
    """Convert audio file to WAV format for Whisper"""
    try:
        # For now, we'll let Whisper handle the audio conversion directly
        # Save the uploaded file to a temporary location
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        
        # Write the uploaded file content to temp file
        with open(temp_file.name, "wb") as f:
            f.write(audio_file.getvalue())
        
        return temp_file.name
    except Exception as e:
        st.error(f"Error processing audio: {str(e)}")
        return None

def display_chat_message(role, content):
    """Display a chat message with proper styling"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>AI Assistant:</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main Streamlit app"""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Assistant with Memory</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Powered by Gemini 2.5 Pro • Voice & Text Input • Long-term Memory</p>', unsafe_allow_html=True)
    
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("⚠️ GOOGLE_API_KEY not found!")
        st.info("""
        **Setup Instructions:**
        1. Get your Google API key from: https://makersuite.google.com/app/apikey
        2. Copy the `.env` file and rename it to `.env`
        3. Replace `your_google_api_key_here` with your actual API key
        4. Restart the app
        """)
        return
    
    # Initialize assistant
    initialize_assistant()
    
    if not st.session_state.get('initialized', False):
        return
    
    # Sidebar for controls
    with st.sidebar:
        st.markdown("## 🎛️ Control Panel")
        st.markdown("---")
        
        # Clear memory button
        if st.button("🗑️ Clear Memory", help="Clear all stored conversations"):
            st.session_state.assistant.clear_memory()
            st.session_state.messages = []
            st.success("Memory cleared!")
            st.rerun()
        
        st.markdown("---")
        
        # Memory search
        st.markdown("### 🔍 Search Memory")
        search_query = st.text_input("Search past conversations:", placeholder="Type your search...")
        if search_query and st.button("🔎 Search"):
            with st.spinner("Searching..."):
                results = st.session_state.assistant.search_memory(search_query)
            if results:
                st.markdown("**Found memories:**")
                for i, result in enumerate(results[:3]):  # Show top 3
                    st.markdown(f"**{i+1}.** {result['content'][:100]}...")
            else:
                st.markdown("No relevant memories found.")
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Refresh App"):
            st.rerun()
        
        if st.button("📝 New Chat"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Setup instructions
        st.markdown("### 📋 Setup Guide")
        st.markdown("""
        **For Beginners:**
        1. Install dependencies: `pip install -r requirements.txt`
        2. Get Google API key from: https://makersuite.google.com/app/apikey
        3. Add API key to `.env` file
        4. Run: `streamlit run app.py`
        
        **Features:**
        - Type messages or upload audio files
        - AI remembers previous conversations
        - Search through past conversations
        - Voice input via Whisper transcription
        """)
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 💬 Chat Interface")
        
        # Initialize messages
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        if st.session_state.messages:
            for message in st.session_state.messages:
                display_chat_message(message["role"], message["content"])
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #666;">
                <h3>👋 Welcome to your AI Assistant!</h3>
                <p>Start a conversation by typing a message below or uploading an audio file.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Text input
        st.markdown("### ✍️ Type Your Message")
        user_input = st.text_input("", placeholder="Ask me anything...", key="text_input")
        
        # Voice input
        st.markdown("### 🎤 Voice Input")
        audio_file = st.file_uploader(
            "Upload audio file (MP3, WAV, M4A):",
            type=['mp3', 'wav', 'm4a', 'mp4'],
            help="Upload an audio file to transcribe and send as a message",
            key="audio_uploader"
        )
        
        # Process voice input
        if audio_file is not None:
            with st.spinner("Processing audio..."):
                # Convert audio to WAV format
                temp_audio_path = convert_audio_format(audio_file)
                
                if temp_audio_path:
                    # Transcribe audio
                    transcribed_text = transcribe_audio(temp_audio_path)
                    
                    if transcribed_text:
                        st.success(f"Transcribed: {transcribed_text}")
                        user_input = transcribed_text
                        
                        # Clean up temporary file
                        os.unlink(temp_audio_path)
        
        # Send button
        if st.button("Send Message", disabled=not user_input):
            if user_input:
                # Add user message to chat
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Get AI response
                with st.spinner("AI is thinking..."):
                    response = st.session_state.assistant.process_message(user_input)
                
                # Add AI response to chat
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Rerun to update the display
                st.rerun()
    
    with col2:
        st.markdown("### 📊 Status Dashboard")
        
        # Show conversation count
        conversation_count = len(st.session_state.messages) // 2
        st.markdown(f"""
        <div class="metric-card">
            <h3>💬 Conversations</h3>
            <h2>{conversation_count}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Show memory status
        try:
            history = st.session_state.assistant.get_conversation_history()
            memory_count = len(history)
            st.markdown(f"""
            <div class="metric-card">
                <h3>🧠 Stored Memories</h3>
                <h2>{memory_count}</h2>
            </div>
            """, unsafe_allow_html=True)
        except:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🧠 Stored Memories</h3>
                <h2>N/A</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # AI Status
        st.markdown(f"""
        <div class="metric-card">
            <h3>🤖 AI Status</h3>
            <h2 class="status-online">ONLINE</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Refresh"):
            st.rerun()
        
        if st.button("📝 New Chat"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("📱 Share Link"):
            st.info("Share this link: http://localhost:8502")

if __name__ == "__main__":
    main()
