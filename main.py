import os
import google.generativeai as genai
import datetime
import speech_recognition as sr
import webbrowser
from config import apikey
import pyautogui
chatStr = ""


genai.configure(api_key=apikey)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,

)



def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"Nikhil said: {query}")
            return query
        except Exception as e:
            print(f"Error: {e}")
            return "Some Error Occurred. Sorry from Jarvis"



def chat(query):
    global chatStr
    print(chatStr)
    chatStr += f"Nikhil: {query}\n Jarvis: "

    # Start a chat session with the model
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"{query}\n",
                ],
            },
        ]
    )

    try:
        # Send user input to the model and get response
        response = chat_session.send_message(query)
        chatStr += f"{response.text}\n"
        print(response.text)
        say(response.text)
    except Exception as e:
        print(f"Error in chat function: {e}")
        chatStr += f"Error: {e}\n"
        return "Sorry, I encountered an error while processing your request."


def ai(prompt):

    text = f"Google AI response for Prompt: {prompt} \n *************************\n\n"
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"{prompt}\n",
                ],
            },
        ]
    )

    try:

        response = chat_session.send_message(prompt)
        text += response.text


        if not os.path.exists("GoogleAI"):
            os.mkdir("GoogleAI")
        with open(f"GoogleAI/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
            f.write(response.text)

        say(response.text)
    except Exception as e:
        print(f"Error in ai function: {e}")
        text += f"Error: {e}"

    return text

def say(text):
    os.system(f'say "{text}"')

def screenshot():
    try:
        # Take screenshot
        img = pyautogui.screenshot()
        # Define the path within the project directory
        img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pictureSS")
        img_path = os.path.join(img_dir, "ss.png")
        # Ensure the directory exists
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        # Save the screenshot
        img.save(img_path)
        print(f"Screenshot saved at {img_path}")
    except pyautogui.PyAutoGUIException as e:
        print(f"An error occurred: {e}")

def wishme():

    hour = datetime.datetime.now().hour
    if hour >= 4 and hour < 12:
        say("Good Morning Sir!!")
        print("Good Morning Sir!!")
    elif hour >= 12 and hour < 16:
        say("Good Afternoon Sir!!")
        print("Good Afternoon Sir!!")
    elif hour >= 16 and hour < 24:
        say("Good Evening Sir!!")
        print("Good Evening Sir!!")
    else:
        say("Good Night Sir, See You Tommorrow")

    say("Jarvis at your service , please tell me how may I help you.")
    print("Jarvis at your service, please tell me how may I help you.")
if __name__ == '__main__':
    wishme()

    while True:
        query = takeCommand()


        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"],
        ]


        site_opened = False
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                site_opened = True
                break

        if site_opened:
            continue


        if "open music" in query.lower():
            musicPath = "/Users/nikhilchoudhary/Downloads/kahani.mp3"  # Replace with your music path
            os.system(f"open {musicPath}")


        # Check if query is to get the current time
        elif "the time" in query.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir time is {strfTime}")

        elif "search on google".lower() in query.lower():
            try:
                say("What should I search?")
                search = takeCommand()
                search_url = f"https://www.google.com/search?q={search}"
                webbrowser.get('macosx').open_new_tab(search_url)
                print(f"Searching for: {search}")
            except Exception as e:
                say("An error occurred while trying to search on google.")
                print(f"Error: {e}")

        elif "who are you".lower() in query.lower():
            say("I'm JARVIS created by Mr. Nikhil Choudhary and I'm a desktop voice assistant.")

        elif "how are you".lower() in query.lower():
            say("I'm fine sir, What about you?")

        elif "fine".lower()   in query.lower():
            say("Nice to hear that sir!!")

        elif "good".lower() in query.lower():
            spay("Glad to hear that sir!!")

        # Check if query is to open FaceTime
        elif "open facetime".lower() in query.lower():
            say(f"Opening facetime sir...")
            os.system(f"open /System/Applications/FaceTime.app")

        # Check if query is related to using artificial intelligence
        elif "using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
        elif "screenshot" in query:
            screenshot()
            say("I've taken screenshot, please check it")
        # Check if query is to quit Jarvis
        elif "jarvis quit".lower() in query.lower():
            exit()

        # Check if query is to reset chat history
        elif "reset chat".lower() in query.lower():
            chatStr = ""

        # If none of the specific commands match, start a general chat
        else:
            print("Chatting...")
            chat(query)
