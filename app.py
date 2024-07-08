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

# Function to build the dataset
def build_dataset():
    X_train = [
        "open youtube",
        "search youtube",
        "open google",
        "search google",
        "open settings",
        "open command prompt",
        "open calculator",
        "open vscode",
        "open notepad",
        "open file explorer",
        "open task manager",
        "open control panel",
        "open calendar",
        "open photos",
        "open music",
        "open video",
        "open whatsapp",
        "time",
        "date",
        "exit",
        "add",
        "subtract",
        "multiply",
        "divide",
        "calculate",
        "close"
    ]
    y_train = [
        "Open", "Search", "Open", "Search", "Open", "Open", "Open", "Open",
        "Open", "Open", "Open", "Open", "Open", "Open", "Open", "Open", "Open",
        "Time", "Date", "Exit", "Calculate", "Calculate", "Calculate",
        "Calculate", "Calculate", "Close"
    ]
    return X_train, y_train

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
        "whatsapp": "https://web.whatsapp.com"
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
    # Close Chrome tabs
    os.system("taskkill /im chrome.exe /f")
    # Add more commands to close other applications if needed
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
    # Mapping words to calculator key presses
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
        'x': '*',  # Handle 'x' as multiplication
    }

    # Replace words with symbols
    for word, symbol in key_mapping.items():
        expression = expression.replace(word, symbol)

    # Removing any non-arithmetic characters for security
    expression = re.sub(r'[^0-9+\-*/=%]', '', expression)

    # Simulate key presses
    for char in expression:
        pyautogui.press(char)
        time.sleep(0.1)

    pyautogui.press('enter')

# Function to search a contact on WhatsApp Web
def search_whatsapp_contact(contact_name):
    # Start the WebDriver with Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://web.whatsapp.com")
    
    # Check if WhatsApp is already logged in
    if "Click to reload QR code" not in driver.page_source:
        speak("Already logged in to WhatsApp Web.")
    else:
        # Wait for user to scan QR code and WhatsApp Web to load
        speak("Please scan the QR code to log in to WhatsApp Web.")
        while "Click to reload QR code" in driver.page_source:
            time.sleep(5)
        speak("Logged in to WhatsApp Web.")
    
    # Search for the contact
    search_box = None
    while search_box is None:
        try:
            search_box = driver.find_element("xpath", "//div[@contenteditable='true'][@data-tab='3']")
        except:
            pass

    search_box.click()
    search_box.send_keys(contact_name)
    time.sleep(2)  # Wait for search results to appear
    search_box.send_keys(Keys.ENTER)
    speak(f"Opening chat with {contact_name}")

    # Keep the browser open indefinitely
    while True:
        time.sleep(10)

# Main function for voice assistant
def voice_assistant():
    speak("Hello, how can I help you today?")
    
    # Build the dataset
    X_train, y_train = build_dataset()
    
    # Create a pipeline with TF-IDF vectorizer and Random Forest classifier
    pipeline = make_pipeline(
        TfidfVectorizer(preprocessor=lambda x: x.lower()),
        RandomForestClassifier(n_estimators=100, random_state=42)
    )
    
    # Train the classifier
    pipeline.fit(X_train, y_train)
    
    # Dictionary mapping user commands to system applications
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
        "whatsapp": "https://web.whatsapp.com"
    }
    
    while True:
        query = recognize_speech()
        
        if query is None:
            continue
        
        # Predict the intent
        intent = pipeline.predict([query])[0]
        
        if intent == "Open":
            # Extract the application name
            app_name = None
            for word in query.split():
                if word in system_apps:
                    app_name = word
                    break
            if app_name:
                if app_name == "settings":
                    # Open Settings and search if the query contains 'search'
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
            # Perform search based on query
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
        
        else:
            # Handle general knowledge questions using OpenAI
            answer = ask_openai(query)
            if answer:
                speak(answer)
            else:
                speak("I couldn't find an answer to your question.")
            speak("You can ask another question.")

if __name__ == "__main__":
    voice_assistant()
