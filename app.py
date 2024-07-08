import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import subprocess
import os
import openai
import pyautogui 
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

# Initialize the TTS engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get current time
def get_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M")

# Function to get current date
def get_date():
    now = datetime.datetime.now()
    return now.strftime("%B %d, %Y")

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        
        try:
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            return None

# Function to get weather information
def get_weather():
    api_key = "YOUR_WEATHER_API_KEY"  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "Your_City"  # Replace with your city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        temp = main["temp"] - 273.15  # Convert Kelvin to Celsius
        humidity = main["humidity"]
        description = weather["description"]
        return f"Current temperature is {temp:.2f} degree Celsius with {description} and humidity of {humidity}%."
    else:
        return "City not found."

# Function to get news updates
def get_news():
    api_key = "YOUR_NEWS_API_KEY"  # Replace with your actual API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    articles = response.json()["articles"]
    
    news = []
    for article in articles[:5]:
        news.append(article["title"])
    
    return "Here are the top 5 news headlines: " + ", ".join(news)

# Function to set a reminder
def set_reminder(reminder):
    speak(f"Reminder set for {reminder}")
    # Save reminder to a file or a database

# Function to open system applications
def open_application(app_name):
    system_apps = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "settings": "start ms-settings:",
        "command prompt": "cmd",
        "calculator": "calc",
        "vscode": "code",
        "notepad": "notepad",
        "file explorer": "explorer",
        "task manager": "taskmgr",
        "control panel": "control",
        "calendar": "outlookcal:",
        "photos": "ms-photos:",
        "music": "ms-music:",
        "video": "ms-video:",
        "whatsapp": "https://web.whatsapp.com",
        "spotify": "spotify"
    }
    app_command = system_apps.get(app_name)
    if app_command:
        if app_name == "settings":
            os.system(app_command)
        elif app_name in ["command prompt", "calculator", "vscode", "notepad", "file explorer", "task manager", "control panel", "calendar", "photos", "music", "video"]:
            subprocess.Popen([app_command], shell=True)
        else:
            webbrowser.open(app_command)
    else:
        speak(f"Sorry, I don't know how to open {app_name}.")

# Function to close Chrome tabs or applications
def close_applications():
    os.system("taskkill /im chrome.exe /f")
    apps_to_close = ["notepad.exe", "calc.exe", "cmd.exe", "explorer.exe", "taskmgr.exe", "control.exe", "code.exe"]
    for app in apps_to_close:
        os.system(f"taskkill /im {app} /f")

# Function to get an answer from OpenAI
def ask_openai(question):
    openai.api_key = 'YOUR_API_KEY'  # Replace with your actual API key
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            max_tokens=150
        )
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        print(f"Error: {e}")
        return None

def type_in_calculator(expression):
    key_mapping = {
        'plus': '+',
        'minus': '-',
        'multiply': '*',
        'times': '*',
        'divided': '/',
        'by': '/',
        'equal': '=',
        'equals': '=',
        'percent': '%',
        'x': '*',
    }
    for word, symbol in key_mapping.items():
        expression = expression.replace(word, symbol)
    expression = re.sub(r'[^0-9+\-*/=%]', '', expression)
    for char in expression:
        pyautogui.press(char)
        time.sleep(0.1)
    pyautogui.press('enter')

# Function to search a contact on WhatsApp Web
def search_whatsapp_contact(contact_name):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://web.whatsapp.com")
    if "Click to reload QR code" not in driver.page_source:
        speak("Already logged in to WhatsApp Web.")
    else:
        speak("Please scan the QR code to log in to WhatsApp Web.")
        while "Click to reload QR code" in driver.page_source:
            time.sleep(5)
        speak("Logged in to WhatsApp Web.")
    search_box = None
    while search_box is None:
        try:
            search_box = driver.find_element("xpath", "//div[@contenteditable='true'][@data-tab='3']")
        except:
            pass
    search_box.click()
    search_box.send_keys(contact_name)
    time.sleep(2)
    search_box.send_keys(Keys.ENTER)
    speak(f"Opening chat with {contact_name}")
    while True:
        time.sleep(10)

# Function to read emails
def read_emails():
    # Placeholder for email reading functionality
    speak("Reading your emails...")

# Function to play music
def play_music(song):
    speak(f"Playing {song}")
    webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
    
# Main function for voice assistant
def voice_assistant():
    speak("Hello, how can I help you today?")
    X_train, y_train = build_dataset()
    pipeline = make_pipeline(
        TfidfVectorizer(preprocessor=lambda x: x.lower()),
        RandomForestClassifier(n_estimators=100, random_state=42)
    )
    pipeline.fit(X_train, y_train)
    system_apps = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "settings": "start ms-settings:",
        "command prompt": "cmd",
        "calculator": "calc",
        "vscode": "code",
        "notepad": "notepad",
        "file explorer": "explorer",
        "task manager": "taskmgr",
        "control panel": "control",
        "calendar": "outlookcal:",
        "photos": "ms-photos:",
        "music": "ms-music:",
        "video": "ms-video:",
        "whatsapp": "https://web.whatsapp.com",
        "spotify": "spotify"
    }
    
    while True:
        query = recognize_speech()
        
        if query is None:
            continue
        
        intent = pipeline.predict([query])[0]
        
        if intent == "Open":
            app_name = None
            for word in query.split():
                if word in system_apps:
                    app_name = word
                    break
            if app_name:
                if app_name == "settings":
                    if "search" in query:
                        search_query = query.split("search", 1)[-1].strip()
                        os.system(f"{system_apps[app_name]} {search_query}")
                    else:
                        os.system(system_apps[app_name])
                elif app_name == "whatsapp":
                    speak(f"Opening {app_name}")
                    search_whatsapp_contact(query.split('whatsapp', 1)[-1].strip())
                else:
                    open_application(app_name)
                    speak(f"Opening {app_name}")
            else:
                speak("Sorry, I didn't recognize the application.")
        elif intent == "Search":
            if "youtube" in query:
                search_query = query.split("search", 1)[-1].strip()
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
                speak(f"Searching for {search_query} on YouTube")
            else:
                search_query = query.split("search", 1)[-1].strip()
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                speak(f"Searching for {search_query} on Google")
        elif intent == "Time":
            current_time = get_time()
            speak(f"The current time is {current_time}")
        elif intent == "Date":
            current_date = get_date()
            speak(f"Today's date is {current_date}")
        elif intent == "Exit":
            speak("Goodbye!")
            break
        elif intent == "Calculate":
            expression = query.split("calculate", 1)[-1].strip()
            speak(f"Calculating {expression}")
            type_in_calculator(expression)
        elif intent == "Weather":
            weather = get_weather()
            speak(weather)
        elif intent == "News":
            news = get_news()
            speak(news)
        elif intent == "Reminder":
            reminder = query.split("reminder", 1)[-1].strip()
            set_reminder(reminder)
        elif intent == "Music":
            song = query.split("play", 1)[-1].strip()
            play_music(song)
        elif intent == "Email":
            read_emails()
        else:
            answer = ask_openai(query)
            if answer:
                speak(answer)
            else:
                speak("I couldn't find an answer to your question.")
            speak("You can ask another question.")

if __name__ == "__main__":
    voice_assistant()
