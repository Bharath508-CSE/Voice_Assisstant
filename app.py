import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pyjokes
import os
import pywhatkit
import pyautogui
import requests

# =========================
# INIT ENGINE
# =========================
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)

# =========================
# SPEAK FUNCTION
# =========================
def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# =========================
# GREETING
# =========================
def wish_user():
    hour = int(datetime.datetime.now().hour)

    if hour < 12:
        speak("Good Morning")
    elif hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("I am your advanced voice assistant. How can I help you?")

# =========================
# VOICE INPUT
# =========================
def take_command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("You said:", query)

    except:
        speak("Please say that again")
        return "none"

    return query.lower()

# =========================
# WEATHER FUNCTION
# =========================
def get_weather():
    speak("Enter city name")
    city = input("City: ")
    
    api_key = "YOUR_API_KEY"   # Replace with OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    data = requests.get(url).json()

    if data["cod"] == 200:
        temp = data["main"]["temp"]
        speak(f"The temperature in {city} is {temp} degree Celsius")
    else:
        speak("City not found")

# =========================
# MAIN ASSISTANT
# =========================
def run_assistant():
    wish_user()

    while True:
        query = take_command()

        # Wikipedia
        if 'wikipedia' in query:
            speak("Searching Wikipedia")
            query = query.replace("wikipedia", "")

            try:
                result = wikipedia.summary(query, sentences=2)
                speak(result)
            except:
                speak("Sorry, no results found")

        # Open Websites
        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://google.com")

        elif 'open website' in query:
            speak("Which website?")
            site = take_command()
            webbrowser.open(f"https://{site}.com")

        # Search
        elif 'search' in query:
            speak("What should I search?")
            search = take_command()
            webbrowser.open(f"https://www.google.com/search?q={search}")

        # Time
        elif 'time' in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {time}")

        # Joke
        elif 'joke' in query:
            speak(pyjokes.get_joke())

        # Play Song
        elif 'play' in query:
            song = query.replace('play', '')
            speak("Playing " + song)
            pywhatkit.playonyt(song)

        # WhatsApp
        elif 'whatsapp' in query:
            speak("Enter number with country code")
            number = input("Number: ")

            speak("Enter message")
            message = input("Message: ")

            hour = int(datetime.datetime.now().hour)
            minute = int(datetime.datetime.now().minute) + 2

            pywhatkit.sendwhatmsg(number, message, hour, minute)
            speak("Message scheduled")

        # Screenshot
        elif 'screenshot' in query:
            img = pyautogui.screenshot()
            img.save("screenshot.png")
            speak("Screenshot saved")

        # Volume Control
        elif 'volume up' in query:
            pyautogui.press("volumeup")

        elif 'volume down' in query:
            pyautogui.press("volumedown")

        elif 'mute' in query:
            pyautogui.press("volumemute")

        # Weather
        elif 'weather' in query:
            get_weather()

        # Open Apps
        elif 'open chrome' in query:
            os.system("start chrome")

        elif 'open notepad' in query:
            os.system("notepad")

        # System Controls
        elif 'shutdown' in query:
            speak("Shutting down")
            os.system("shutdown /s /t 5")

        elif 'restart' in query:
            speak("Restarting")
            os.system("shutdown /r /t 5")

        # Exit
        elif 'exit' in query or 'bye' in query:
            speak("Goodbye")
            break

        else:
            speak("Sorry, I didn't understand")

# =========================
# RUN
# =========================
run_assistant()