# 🤖 QRX3 AI Chatbot 
## **Optimized and tested on Mac Silicon M2**

A secure, multi-functional chatbot with image generation capabilities, built with PyQt5 and Stable Diffusion.

---

## ✨ Key Features

### 🔒 Security System
- SHA-512 password hashing with double encryption
- Locally hosted AI chatbot
- No internet dependency — **100% offline**
- Multiple user authentication system
- 3-attempt limit before self-destruction
- Automatic script deletion on failed attempts

### 💬 Chat Capabilities
- Context-aware conversations
- Message persistence across sessions
- Session management with chat logs
- Chat history persistence
- Custom Ollama model integration ("Vedu/QRX3_chatbot")

### 🎨 Image Generation
- Stable Diffusion v1.4 integration
- MPS-accelerated (Apple Silicon optimized)
- Automatic image clearing after display
- Prompt-based generation ("image: [description]")

### 🖥️ Dual Interfaces
- **GUI Version**:
  - Clean, responsive chat UI built with PyQt5
  - Image preview panel
- **CLI Version**:
  - Lightweight console alternative
  - Same core functionality

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (Tested on 3.13.1)
- <a href="https://ollama.ai">Ollama</a> installed
- Apple Silicon Mac (for MPS acceleration) or CUDA GPU (Tested on Apple Silicon M2)

### Note for Developers: 
To contribute or collaborate in this project reach out to us via <a href="mailto:vedant.storm@gmail.com">E-Mail</a>

### Installation
When cloning please ensure secrets file is downloaded and is in the root folder
```bash
# Clone repository
git clone https://github.com/VeduStorm/qrx3_ai-chatbot.git
cd QRX3-Chatbot

# Install dependencies
pip install -r requirements.txt
ollama pull Vedu/QRX3_chatbot:latest

# Set up a new user
python register.py
> Password: [your_password]

# Launch application
python main_gui.py  # GUI version
# or
python main_cli.py  # CLI version

# Launch source code (without extra code encryption and code decryption
python3 source_gui.py # GUI version
# or
python3 source_cli.py # CLI version
```
# Acknowledgements

This project wouldn’t be possible without:

- [Ollama](https://ollama.com/) for enabling easy local LLM deployment
- Open-source LLMs like Llama3
- PyQt5 for the fast and clean UI
- The open-source community for constant inspiration

Made with ❤️ by [Vedant Gandhi](https://github.com/VeduStorm)
