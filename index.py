import os
import time
from datetime import datetime
from PIL import ImageGrab, Image
import pytesseract
import openai
import keyboard
import tkinter as tk
from plyer import notification

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

openai.api_key = "ENTER YOUR API KEY (CHAT GPT, OR CHANGE THE CODE SO IT WORKS FOR ANY AI)"

screenshot_dir = "screenshot-history"
os.makedirs(screenshot_dir, exist_ok=True)

screenshot_region = None

def extract_text_from_image(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)

def ask_chatgpt(question_text: str) -> str:
    prompt = f"Answer this quiz question briefly and directly:\n\n{question_text.strip()}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.2,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"[ERROR] Failed to get response: {e}"

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

    extracted_text = extract_text_from_image(screenshot)
    print(f"[?] Extracted Text:\n{extracted_text}")

    if extracted_text.strip():
        answer = ask_chatgpt(extracted_text)
        print(f"\n💡 Answer from ChatGPT:\n{answer}\n")
        notification.notify(
            title="Quiz Answer",
            message=answer,
            timeout=10 
        )
    else:
        print("[!] No text found in the screenshot.")

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
keyboard.wait('esc')
