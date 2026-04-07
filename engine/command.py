import eel
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import write
import speech_recognition as sr
import numpy as np
import time
import subprocess
import webbrowser
import pywhatkit
import random

# ---------- SPEAK FUNCTION ----------
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Female voice
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()


# ---------- HANDLE COMMAND ----------
def handle_command(text):
    text = text.lower()
    found = False

    # ---------- INTRODUCTION ----------
    if "who are you" in text or "what are you" in text:
        eel.showStatus("Introducing myself...")
        responses = [
            "Hello, I am Darling, your personal AI voice assistant.",
            "Hi, I am Darling. I can help you with tasks on your computer.",
            "I am Darling, your friendly AI assistant."
        ]
        speak(random.choice(responses))
        found = True
        return

    if "what can you do" in text or "tell me about yourself" in text:
        eel.showStatus("Describing my abilities...")
        responses = [
            "I can open apps, browse websites, play YouTube videos, and respond to your commands.",
            "I am your AI assistant. I can help you with tasks like opening apps or searching videos on YouTube."
        ]
        speak(random.choice(responses))
        found = True
        return

    # ---------- LOCAL APPS ----------
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    }

    for key in apps:
        if f"open {key}" in text:
            eel.showStatus(f"Opening {key.capitalize()}...")
            speak(f"Opening {key}")
            subprocess.Popen([apps[key]])
            found = True
            return

    # ---------- WEBSITES ----------
    websites = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "github": "https://www.github.com",
    }

    for key in websites:
        if f"open {key}" in text:
            eel.showStatus(f"Opening {key.capitalize()}...")
            speak(f"Opening {key}")
            webbrowser.open(websites[key])
            found = True
            return

    # ---------- PLAY YOUTUBE VIDEOS ----------
    if "play" in text and "youtube" in text:
        search_query = text.replace("darling", "").replace("play", "").replace("on youtube", "").strip()
        if search_query:
            eel.showStatus(f"Playing {search_query} on YouTube...")
            speak(f"Playing {search_query} on YouTube")
            pywhatkit.playonyt(search_query)
            found = True
            return

    # ---------- NOT RECOGNIZED ----------
    if not found:
        eel.showStatus("Command not recognized")
        speak("Sorry, I did not understand the command")


# ---------- LISTEN FUNCTION ----------
@eel.expose
def listen():
    fs = 44100  # Sampling frequency
    seconds = 4  # Duration of recording

    print("Listening...")
    eel.showStatus("Listening...")

    # Record audio
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()

    # Convert to 16-bit PCM and save
    recording = (recording * 32767).astype(np.int16)
    write("input.wav", fs, recording)

    print("Recognizing...")
    eel.showStatus("Recognizing...")

    recognizer = sr.Recognizer()

    with sr.AudioFile("input.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)

        # Update UI
        eel.showUserText(text)

        # Speak what user said
        speak(text)

        # Handle commands
        handle_command(text)

        # Reset UI to idle
        time.sleep(2)
        eel.showHood()()

        return text

    except sr.UnknownValueError:
        eel.showUserText("Could not understand")
        speak("Sorry, I did not understand")
        return None
    except sr.RequestError:
        eel.showUserText("Recognition service failed")
        speak("Sorry, recognition service failed")
        return None