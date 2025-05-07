# 🤖 QRX3 AI Chatbot (Mac Silicon Complatible)

A secure, multi-functional chatbot with image generation capabilities, built with PyQt5 and Stable Diffusion.

---

## ✨ Key Features

### 🔒 Security System
- SHA-512 password hashing with double encryption
- 3-attempt limit before self-destruction
- Automatic script deletion on failed attempts

### 💬 Chat Capabilities
- Context-aware conversations
- Chat history persistence
- Custom Ollama model integration ("Vedu/QRX3_chatbot")

### 🎨 Image Generation
- Stable Diffusion v1.4 integration
- MPS-accelerated (Apple Silicon optimized)
- Automatic image clearing after display
- Prompt-based generation ("image: [description]")

### 🖥️ Dual Interfaces
- **GUI Version**:
  - PyQt5-based interface
  - Image preview panel
  - Chat history sidebar
- **CLI Version**:
  - Lightweight console alternative
  - Same core functionality

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (Tested on 3.13.1)
- <a href="https://ollama.ai">Ollama</a>
- Apple Silicon Mac (for MPS acceleration) or CUDA GPU (Tested on Apple Silicon M2)

### Note for Developers: 
To contribute or collaborate in this project reach out to us via <a href="mailto:vedant.storm@gmail.com">E-Mail</a>

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/QRX3-Chatbot.git
cd QRX3-Chatbot

# Install dependencies
pip install -r requirements.txt
ollama pull Vedu/QRX3_chatbot:latest

# Set up password (first run only)
python register.py
> Password: [your_password]

# Launch application
python main_gui.py  # GUI version
# or
python main_cli.py  # CLI version
