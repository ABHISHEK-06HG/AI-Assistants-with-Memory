# AI-Assistants-with-Memory

## 🤖 Project Overview
A beautiful Streamlit-based AI assistant with voice + text input and long-term memory using Google Gemini 2.5 Pro.

## 🚀 Quick Start
1. **Install dependencies**: `pip install -r requirements.txt`
2. **Get Google API key**: https://makersuite.google.com/app/apikey
3. **Configure environment**: Copy `.env.sample` to `.env` and add your API key
4. **Run the app**: `streamlit run app.py`

## 📁 Project Structure
```
my_ai_assistant/
├── app.py                # Beautiful Streamlit frontend
├── assistant.py          # Core AI logic (Gemini + memory)
├── memory.py             # ChromaDB + LangChain memory
├── requirements.txt      # All dependencies
├── .env.sample          # Environment template
├── README.md            # This file
└── start_beautiful_app.bat  # Easy Windows startup
```

## ✨ Features
- 🎨 **Beautiful Modern UI** with gradients and animations
- 🎤 **Voice Input** via Whisper transcription
- 💬 **Text Chat** with Gemini 2.5 Pro
- 🧠 **Long-term Memory** with ChromaDB
- 🔍 **Memory Search** through past conversations
- 📱 **Mobile Responsive** design

## 🔧 Setup Instructions

### For Beginners:
1. **Install Python** from https://python.org
2. **Open terminal** in this folder
3. **Install packages**: `pip install -r requirements.txt`
4. **Get API key** from Google AI Studio
5. **Create .env file** with your API key
6. **Run**: `streamlit run app.py`

### API Keys Needed:
- **Google Gemini**: https://makersuite.google.com/app/apikey
- **Hugging Face** (optional): https://huggingface.co/settings/tokens

## 🌐 Access Options
- **Local**: http://localhost:8501
- **Network**: http://YOUR_IP:8501
- **Public**: Use ngrok for permanent public access

## 🎯 Usage
1. **Text Chat**: Type messages in the input field
2. **Voice Input**: Upload audio files (MP3, WAV, M4A)
3. **Memory Search**: Use sidebar to search past conversations
4. **Clear Memory**: Reset all stored conversations

## 🛠️ Customization
- **Change AI personality**: Edit `assistant.py`
- **Modify UI**: Update CSS in `app.py`
- **Adjust memory**: Configure settings in `memory.py`

## 📞 Support
- Check the README.md for detailed instructions
- All code is well-commented for easy understanding
- Beginner-friendly setup with clear error messages

---
**Created with using Streamlit, LangChain, and Google Gemini**
