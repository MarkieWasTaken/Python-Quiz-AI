# 🧠 DWare Quiz Tool

**DWare Quiz Tool** is a lightweight screen-based quiz solver assistant powered by Python and Google Gemini AI.
With a single hotkey, it captures a selected region of your screen, analyzes it using AI vision, and shows the answer as a Windows notification.

---

## 📦 Features

- 🖼️ Region-based screenshot (click-and-drag)
- 🤖 AI-powered question answering using Google Gemini Vision
- 🔔 Instant Windows toast notification with the answer
- 🎯 Fully hotkey-driven (no GUI popup)
- 📁 Screenshots saved in `screenshot-history` folder
- 🔤 OCR text extraction using Tesseract

---

## 🚀 Hotkeys

| Action                  | Hotkey             |
|-------------------------|--------------------|
| Define screenshot area  | `Ctrl + Alt + D`   |
| Take screenshot + solve | `Ctrl + Alt + S`   |
| Exit tool               | `ESC`              |

---

## 📥 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/MarkieWasTaken/Python-Quiz-AI.git
cd Python-Quiz-AI
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install Pillow pytesseract google-generativeai keyboard plyer python-dotenv
```

### Step 3: Install Tesseract OCR

Tesseract is required for text extraction from images.

#### For Windows:

1. Download the installer from UB Mannheim:
   - 🔗 [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the `.exe` installer (e.g., `tesseract-5.x.x-setup.exe`)
3. Install to the default path: `C:\Program Files\Tesseract-OCR\`

#### For macOS:

```bash
brew install tesseract
```

#### For Linux:

```bash
sudo apt-get install tesseract-ocr
```

### Step 4: Get Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### Step 5: Configure Environment Variables

1. Create a `.env` file in the project root directory:

```bash
# On Windows
echo. > .env

# On macOS/Linux
touch .env
```

2. Open `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with the actual API key from Step 4.

---

## 🎮 Usage

### Starting the Tool

Run the script:

```bash
python index.py
```

You should see:

```
📸 Listening for Ctrl + Alt + S to take a screenshot and solve quiz...
💝  Press Ctrl + Alt + D to define screenshot region.
🔴 Press ESC to quit.
```

### How to Use

1. **Define the quiz area** (optional, first time only):
   - Press `Ctrl + Alt + D`
   - Click and drag to select the area where quiz questions appear
   - Release to confirm

2. **Solve a quiz question**:
   - Press `Ctrl + Alt + S`
   - The tool will capture the screen, analyze it with AI, and show the answer in a notification

3. **Exit**:
   - Press `ESC` to stop the tool

---

## 📝 Notes

- Screenshots are automatically saved in the `screenshot-history` folder
- The AI provides direct, concise answers (letters for multiple choice, numbers for calculations)
- Notifications display for 15 seconds
- Works best with clear, readable quiz questions

---

## 🛠️ Troubleshooting

**Issue: "Tesseract not found"**
- Verify Tesseract is installed at `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Update the path in `index.py` line 15 if installed elsewhere

**Issue: "GEMINI_API_KEY not found"**
- Ensure `.env` file exists in the project root
- Check that the API key is correctly formatted in `.env`

**Issue: Hotkeys not working**
- Make sure you run the script with administrator privileges on Windows
- Check if another application is using the same hotkey combination

---

## 📄 License

This project is open source and available for educational purposes.



