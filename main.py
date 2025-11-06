import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY") #create your OpenAI account and get the key from there
NEWS_KEY = os.getenv("NEWS_API_KEY") #create your News API account and get the key from there and put in .env file

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    client = OpenAI(api_key=OPENAI_KEY)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Jarvis. Respond short and smart."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = c.replace("play", "").strip()
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found mate")
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_KEY}")
        for article in r.json().get('articles', []):
            speak(article['title'])
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Jarvis is online mate")
    while True:
        try:
            with sr.Microphone() as source:
                r = sr.Recognizer()
                print("Listening for wake word...")
                audio = r.listen(source, timeout=5, phrase_time_limit=1)
            word = r.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Yes mate?")
                with sr.Microphone() as source:
                    print("Listening command...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)

        except Exception as e:
            print("Error:", e)
