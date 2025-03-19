altgraph==0.17.4
anyio==4.4.0
APScheduler==3.6.3
attrs==24.2.0
cachetools==4.2.2
certifi==2024.7.4
cffi==1.17.0
charset-normalizer==3.3.2
exceptiongroup==1.2.2
h11==0.14.0
httpcore==1.0.5
httpx==0.27.0
idna==3.7
importlib_metadata==8.2.0
keyboard==0.13.5
MouseInfo==0.1.3
outcome==1.3.0.post0
packaging==24.1
pefile==2023.2.7
Pillow==8.4.0
psutil==6.1.0
PyAutoGUI==0.9.53
pycparser==2.22
PyGetWindow==0.0.9
PyMsgBox==1.0.9
pynput==1.7.6
pyperclip==1.9.0
PyRect==0.2.0
PyScreeze==0.1.28
PySocks==1.7.1
pystray==0.19.5
pyTelegramBotAPI==4.22.1
python-dotenv==1.0.1
python-telegram-bot==13.7
pytweening==1.2.0
pytz==2024.1
pywin32==308
pywin32-ctypes==0.2.2
requests==2.32.3
six==1.16.0
sniffio==1.3.1
sortedcontainers==2.4.0
tk==0.1.0
tornado==6.4.1
trio==0.26.2
trio-websocket==0.11.1
typing_extensions==4.12.2
tzdata==2024.1
tzlocal==5.2
urllib3==2.2.2
websocket-client==1.8.0
wsproto==1.2.0
zipp==3.19.2
 
 
Command: pip install -r requirements.txt
 
 
 
import pyautogui
import time
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import io
from pynput import keyboard
 
TELEGRAM_BOT_TOKEN ='7134433149:AAHmH4T3wVVMQ0V29mbTQKAlR8aXrVAsHng'
 
bot_chat_id = None
screenshot_enabled = True
 
def take_screenshot_and_send(region_type):
    global bot_chat_id
    if bot_chat_id is None:
        print("DEBUG: No chat ID set. Please start a conversation with the bot first.")
        return
 
    if not screenshot_enabled:
        print("DEBUG: Screenshot functionality is paused.")
        return
 
    time.sleep(1)
 
    screen_width, screen_height = pyautogui.size()
    print(f"DEBUG: Screen size - Width: {screen_width}, Height: {screen_height}")
 
    regions = {
        'full': (0, 0, screen_width, screen_height),
        'left_half': (0, 0, screen_width // 2, screen_height),
        'right_half': (screen_width // 2, 0, screen_width // 2, screen_height),
        'first_quadrant': (0, 0, screen_width // 2, screen_height // 2),
        'second_quadrant': (screen_width // 2, 0, screen_width // 2, screen_height // 2),
        'third_quadrant': (0, screen_height // 2, screen_width // 2, screen_height // 2),
        'fourth_quadrant': (screen_width // 2, screen_height // 2, screen_width // 2, screen_height // 2)
    }
 
    if region_type in regions:
        region = regions[region_type]
        print(f"DEBUG: Capturing screenshot for region: {region_type}, Region coordinates: {region}")
        screenshot = pyautogui.screenshot(region=region)
    else:
        print(f"ERROR: Unknown region type: {region_type}")
        return
 
    buffer = io.BytesIO()
    screenshot.save(buffer, format='PNG')
    buffer.seek(0)
    print("DEBUG: Screenshot captured and saved to buffer.")
 
    updater.bot.send_photo(chat_id=bot_chat_id, photo=InputFile(buffer, filename='screenshot.png'))
    print(f"DEBUG: {region_type.replace('_', ' ').title()} screenshot sent to Telegram.")
 
# Start command handler
def start(update: Update, context: CallbackContext):
    global bot_chat_id
    bot_chat_id = update.message.chat_id
    update.message.reply_text('Hi! Send me a screenshot, and I will extract the text and solve the problem.')
    print(f"DEBUG: Bot started. Chat ID set to {bot_chat_id}.")
 
def type_code(code):
    time.sleep(2)
    print(f"DEBUG: Typing the following code:\n{code}")
    pyautogui.typewrite(code, interval=0.05)
 
def handle_code(update: Update, context: CallbackContext):
 
    message_text = update.message.text
    code_snippet = message_text[len("Code:"):].strip()
    print(f"DEBUG: Received code snippet: {code_snippet}")
 
    type_code(code_snippet)
    update.message.reply_text('Code typing initiated.')
 
def on_press(key):
    global screenshot_enabled
 
    try:
        if key.char == '`':
            screenshot_enabled = not screenshot_enabled
            status = "enabled" if screenshot_enabled else "paused"
            print(f"DEBUG: Screenshot functionality {status}.")
        elif screenshot_enabled:
 
            if key.char == '1':
                take_screenshot_and_send('full')
            elif key.char == '2':
                take_screenshot_and_send('left_half')
            elif key.char == '3':
                take_screenshot_and_send('right_half')
            elif key.char == '4':
                take_screenshot_and_send('first_quadrant')
            elif key.char == '5':
                take_screenshot_and_send('second_quadrant')
            elif key.char == '6':
                take_screenshot_and_send('third_quadrant')
            elif key.char == '7':
                take_screenshot_and_send('fourth_quadrant')
            print(f"DEBUG: Key pressed: {key.char}")
    except AttributeError:
        print(f"DEBUG: Special key pressed: {key}")
 
def main():
    while True:
        try:
            global updater
            updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
            dp = updater.dispatcher
 
            dp.add_handler(CommandHandler('start', start))
            dp.add_handler(MessageHandler(Filters.text & Filters.regex(r'^Code:.*'), handle_code))
            print("DEBUG: Telegram bot initialized and handlers set.")
 
            updater.start_polling()
            print("DEBUG: Bot polling started.")
 
            with keyboard.Listener(on_press=on_press) as listener:
                print("DEBUG: Keyboard listener started.")
                updater.idle()
                listener.join()
                print("DEBUG: Keyboard listener stopped.")
 
        except Exception as e:
            print(f"DEBUG: Exception occurred: {e}")
            print("DEBUG: Waiting 30 seconds before attempting to reconnect...")
            time.sleep(30)
            print("DEBUG: Attempting to restart the bot...")
            continue
 
if __name__ == '__main__':
    main()
