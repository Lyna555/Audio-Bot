# 🤖 **Fahla Audio Bot**

Fahla Audio Bot is an islamic Telegram userbot that allows users to play any audio in Telegram group voice chats using the **PyTgCalls** library.

## ⚙️ **Features**

  - 🔊 Playing audio in Telegram group voice chat
  - 📱 Built with Pyrogram, PyTgCalls, and Telethon
  - 🔐 Uses environment variables for secure API credentials

## 📦 **Requirements**

  - Telegram API ID & Hash (from my.telegram.org)
  - Phone number linked to a Telegram account
  - The script should be run on a Linux environment
  - Python 3.10+

## 🚀 **Deployment**

You can deploy this bot by setting the following environment variables:

    API_ID=your_api_id
    API_HASH=your_api_hash
    SESSION_STRING=your_session_string

## 🛠️ **Setup (Locally)**
### **For Linux Users**

      git clone https://github.com/Lyna555/Fahla_Bot.git
      cd Fahla_Bot
      pip install -r requirements.txt
      python fahla_aud_bot.py

### **For Windows Users (via WSL)**

  1. **Install WSL**
     Open PowerShell as administrator and run:
     
          wsl --install

  2. **Navigate to Your Project Directory**
     Replace the path with your actual username and project location:

          cd /mnt/c/Users/<YourUsername>/path/to/your/project
     
  3. **Create a Virtual Environment**

         python3 -m venv your_environment
  
  4. **Activate the Environment**

          source your_environment/bin/activate

  5. **Clone & Run the Project**
      
          git clone https://github.com/Lyna555/Fahla_Bot.git
          cd Fahla_Bot
          pip install -r requirements.txt
          python fahla_aud_bot.py
