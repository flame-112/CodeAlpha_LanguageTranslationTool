# 🌍 CodeAlpha - Language Translation Tool

📌 **Project Overview**
The Language Translation Tool is a simple, modern, and interactive web application built using **Streamlit** and **Python**. This project was developed as a task for the CodeAlpha Internship. It allows users to input text, automatically detect or select languages, translate paragraphs in real-time, and listen to the translated audio output using text-to-speech technology.

---

## ✨ Features
- 🌐 **Real-Time Translation:** Seamlessly translate text between dozens of global languages.
- 🔄 **Language Swap:** Swap source and target languages instantly with a click.
- 🔊 **Text-to-Speech (TTS):** Integrated audio player to listen to the exact pronunciation of your translated text.
- 📋 **Copy to Clipboard:** Easily copy the translated results.
- 🎨 **Modern UI:** Clean, responsive, and lightweight web layout styled with Streamlit.
- 🛠️ **Error Handling:** Gracefully manages empty fields or API timeouts.

---

## 🛠️ Tech Stack
- **Language:** Python 🐍
- **Frontend Framework:** Streamlit (For the web interface)
- **Translation API Wrapper:** `deep-translator` (Leveraging Google Translate behind the scenes)
- **Audio Engine:** `gTTS` (Google Text-to-Speech)

---

## 📂 Project Structure
```text
CodeAlpha_LanguageTranslationTool/
│
├── app.py               # Main application script containing UI logic
├── requirements.txt     # List of external library dependencies
└── README.md            # Project documentation (this file)
