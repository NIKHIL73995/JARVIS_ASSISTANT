import pyautogui
from telegram import Bot
from telegram.error import TelegramError
from pynput import keyboard
from PIL import Image
import io
import asyncio
import threading

# Telegram bot token and chat ID
TOKEN = '7134433149:AAHmH4T3wVVMQ0V29mbTQKAlR8aXrVAsHng'

CHAT_ID = CHAT_ID = '1080709504'

# Initialize Telegram bot
bot = Bot(token=TOKEN)

# Global flag used to disable screenshot capturing when typing code.
writing_mode = False

# Screen dimensions
screen_width, screen_height = pyautogui.size()

# Region dimensions keyed by numbers as strings
regions = {
    '1': (0, 0, screen_width // 2, screen_height // 2),              # Top-left
    '2': (screen_width // 2, 0, screen_width, screen_height // 2),   # Top-right
    '3': (0, screen_height // 2, screen_width // 2, screen_height),  # Bottom-left
    '4': (screen_width // 2, screen_height // 2, screen_width, screen_height),  # Bottom-right
    '5': (0, 0, screen_width, screen_height // 2),                   # Upper half
    '6': (0, screen_height // 2, screen_width, screen_height),       # Lower half
    '7': (0, 0, screen_width, screen_height)                         # Full screen
}

def take_screenshot(region_key):
    if region_key in regions:
        print(f"Taking screenshot for region {region_key}...")
        x1, y1, x2, y2 = regions[region_key]
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
        print("Screenshot taken successfully.")
        return screenshot
    print(f"Region key '{region_key}' not recognized.")
    return None

async def send_screenshot(image, chat_id, bot):
    try:
        print("Sending screenshot to Telegram...")
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')  # using PNG for lossless quality
        img_byte_arr = img_byte_arr.getvalue()

        # Send the screenshot image
        await bot.send_photo(chat_id=chat_id, photo=img_byte_arr)
        print("Screenshot sent successfully.")
    except TelegramError as e:
        print(f"Failed to send screenshot: {e}")

def on_press(key):
    global writing_mode
    try:
        if not writing_mode and (hasattr(key, 'char') and key.char in ['1', '2', '3', '4', '5', '6', '7']):
            screenshot = take_screenshot(key.char)
            if screenshot:
                asyncio.run_coroutine_threadsafe(
                    send_screenshot(screenshot, CHAT_ID, bot), loop)
    except AttributeError:
        pass

def start_listener():
    print("Listening for key presses (1-7) to take screenshots...")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

async def poll_messages():
    global writing_mode
    last_update_id = None
    print("Starting to poll for Telegram messages for 'Code:' commands...")
    while True:
        try:
            updates = await bot.get_updates(offset=last_update_id, timeout=10)
            for update in updates:
                last_update_id = update.update_id + 1
                if update.message and update.message.text:
                    message_text = update.message.text.strip()
                    if message_text.startswith("Code:"):
                        writing_mode = True
                        code_text = message_text[len("Code:"):].strip()
                        print(f"Received Code command. Typing text: {code_text}")
                        await asyncio.get_running_loop().run_in_executor(None, pyautogui.write, code_text, 0.05)
                        await asyncio.sleep(2)
                        writing_mode = False
                        print("Typing complete. Screenshot feature re-enabled.")
        except Exception as ex:
            print("Error while polling messages:", ex)
        await asyncio.sleep(1)

def main():
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.create_task(poll_messages())

    listener_thread = threading.Thread(target=start_listener)
    listener_thread.daemon = True
    listener_thread.start()

    loop.run_forever()

if __name__ == '__main__':
    main()
