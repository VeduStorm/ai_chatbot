# 🤖 QRX3 AI Chatbot

A secure, multi-functional chatbot with image generation capabilities, built with PyQt5 and Stable Diffusion.

---

## 📂 Project Structure
QRX3-Chatbot/
├── main.py # Primary chatbot application
├── gui.py # Enhanced GUI version
├── main_dupe.py # CLI version backup
├── check.py # Password hashing utility
├── register.py # User registration system
├── requirements.txt # Dependency specifications
├── database.txt # Password storage (hashed)
├── important_info.txt # System configuration
├── chathistory_chatbot.txt # Conversation log
└── assets/
├── QRX3 AI Logo.png # Application icon
└── generated_image.png # Sample output

---

## ✨ Key Features

### 🔒 Security System
- SHA-512 password hashing with double encryption
- 3-attempt limit before self-destruction
- Automatic script deletion on failed attempts

### 💬 Chat Capabilities
- Context-aware conversations
- Chat history persistence
- Custom Ollama model integration ("Vedu/QRX3")
- Markdown-style message formatting

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
- Python 3.8+
- Apple Silicon Mac (for MPS acceleration) or CUDA GPU

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/QRX3-Chatbot.git
cd QRX3-Chatbot

# Install dependencies
pip install -r requirements.txt

# Set up password (first run only)
python check.py
> Password: [your_password]
# Copy output to database.txt

# Launch application
python main.py  # GUI version
# or
python main_dupe.py  # CLI version
