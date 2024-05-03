import pyttsx3
import speech_recognition as sr
import eel
import os

def speak(text):
    text = str(text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate',180)
    print(voices)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takeCommand(): 
    recognizer  = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening....")
        eel.DisplayMessage("Listening....")
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, 10, 6)
    try: 
        print("Recognizing")
        eel.DisplayMessage("Recognizing....")
        query = recognizer.recognize_google(audio, language='en-vi')
        print(f"You Said: {query}")
        eel.DisplayMessage(query)
    except Exception as ex: 
        print("sorry, could not recognize")
        return ""

    return query.lower()

@eel.expose
def allCommands(message = 1): 
    if(message == 1):
        query = takeCommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try: 
        if "open" in query:
            from engine.feature import openCommand
            openCommand(query)
        elif "on youtube" in query: 
            from engine.feature import PlayYoutube
            PlayYoutube(query)
        elif "google" in query:
            from engine.feature import SearchGoogle
            query = takeCommand().lower()
            SearchGoogle(query)
        elif "wikipedia" in query: 
            from engine.feature import SearchWikipedia
            query = takeCommand().lower()
            SearchWikipedia(query)
        elif "hello" in query:
            speak("Hello sir, how are you?")
        elif "temperature" in query or "weather" in query:
            from engine.feature import temperatureSearch
            temperatureSearch(query)
        elif "time" in query or "date" in query:
            from engine.feature import getCurrentDateTime
            getCurrentDateTime(query)
        elif "shutdown system" in query:
            from engine.feature import shutdownSystem
            shutdownSystem(query)
        elif "focus mode" in query:
            speak("Enter the focus mode")
            os.startfile("C:\\Users\\ADMIN\\Documents\\VoiceAssistant\\focus_mode.py")
            # exit()
        else:
            from engine.feature import chatBot
            chatBot(query)
    except Exception as e:
        print(f"Error {e}")
    eel.ShowHood()