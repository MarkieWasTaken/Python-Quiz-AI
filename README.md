# 🧠 DWare Quiz Tool

**DWare Quiz Tool** is a lightweight screen-based quiz solver assistant powered by Python.  
With a single hotkey, it captures a selected region of your screen, extracts the text using OCR, sends it to ChatGPT, and shows the answer as a Windows notification.

---

## 📦 Features

- 🖼️ Region-based screenshot (click-and-drag)
- 🔤 OCR text extraction using Tesseract
- 🧠 AI question answering using ChatGPT (GPT-3.5)
- 🔔 Instant Windows toast notification with the answer
- 🎯 Fully hotkey-driven (no GUI popup)
- 📁 Screenshots saved in `screenshot-history` folder

---

## 🚀 Hotkeys

| Action                  | Hotkey             |
|-------------------------|--------------------|
| Define screenshot area  | `Ctrl + Alt + D`   |
| Take screenshot + solve | `Ctrl + Alt + S`   |
| Exit tool               | `ESC`              |

---

## 📥 Installation

### 1. Download all the PIPS

pip install pillow pytesseract openai keyboard plyer

### 2. Install Tesseract OCR

Tesseract is required to perform OCR (Optical Character Recognition) on screenshots.  
You need to install the actual **Tesseract engine**, not just the Python wrapper.

#### 2.1 For Windows:

Download and install the recommended Windows build from UB Mannheim:

🔗 [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

Choose the latest `.exe` installer (e.g., `tesseract-5.x.x-setup.exe`).

#### 📂 Installation Path

Install it to the default path:

C:\Program Files\Tesseract-OCR\



