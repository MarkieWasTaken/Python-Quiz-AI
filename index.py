import os
import time
from datetime import datetime
from PIL import ImageGrab, Image
import google.generativeai as genai
import keyboard
import tkinter as tk
from plyer import notification
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

screenshot_dir = "screenshot-history"
os.makedirs(screenshot_dir, exist_ok=True)

screenshot_region = None

def ask_gemini_vision(image: Image.Image) -> str:
    """Send image directly to Gemini vision model for better accuracy"""
    prompt = """Answer this quiz question. Give ONLY the direct answer - no explanations, no reasoning, just the answer.

If it's multiple choice, give only the letter(s) or number(s).
If it's a calculation, give only the result.
If it's a short answer, give only the answer in 1-2 words maximum.

Be concise and direct."""

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content([prompt, image])
        return response.text.strip()
    except Exception as e:
        return f"[ERROR] {e}"

def handle_screenshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(screenshot_dir, filename)

    if screenshot_region:
        screenshot = ImageGrab.grab(bbox=screenshot_region)
    else:
        screenshot = ImageGrab.grab()

    screenshot.save(filepath)
    print(f"[+] Screenshot saved: {filepath}")

    # Use vision API - send image directly instead of OCR
    print("[🔍] Analyzing image with Gemini Vision...")
    answer = ask_gemini_vision(screenshot)

    print(f"\n💡 Answer: {answer}\n")

    # Truncate answer if too long for notification (256 char limit)
    if len(answer) > 250:
        notification_text = answer[:247] + "..."
    else:
        notification_text = answer

    notification.notify(
        title="Quiz Answer",
        message=notification_text,
        timeout=15
    )

def define_screenshot_region():
    def on_drag(event):
        nonlocal start_x, start_y
        canvas.delete("selection")
        canvas.create_rectangle(start_x, start_y, event.x, event.y, outline='red', width=2, tag="selection")

    def on_click(event):
        nonlocal start_x, start_y
        start_x, start_y = event.x, event.y

    def on_release(event):
        global screenshot_region
        end_x, end_y = event.x, event.y
        root.destroy()
        screenshot_region = (min(start_x, end_x), min(start_y, end_y),
                             max(start_x, end_x), max(start_y, end_y))
        print(f"[📐] Region set: {screenshot_region}")

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-alpha', 0.3)
    root.configure(background='gray')
    canvas = tk.Canvas(root, cursor="cross")
    canvas.pack(fill="both", expand=True)

    start_x = start_y = 0
    canvas.bind("<Button-1>", on_click)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)

    root.mainloop()

keyboard.add_hotkey('ctrl+alt+s', handle_screenshot)
keyboard.add_hotkey('ctrl+alt+d', define_screenshot_region)

print("📸 Listening for Ctrl + Alt + S to take a screenshot and solve quiz...")
print("💝  Press Ctrl + Alt + D to define screenshot region.")
print("🔴 Press ESC to quit.")
print("🔴 V2")
keyboard.wait('esc')
