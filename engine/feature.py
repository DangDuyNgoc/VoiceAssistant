import os
import platform
import struct
import time
import pvporcupine
import webbrowser
import eel
import sqlite3
import pyaudio
import wikipedia
import requests
import datetime
import googletrans
from googletrans import Translator
from bs4 import BeautifulSoup
import pyautogui as autogui
from hugchat import hugchat
import pywhatkit as kit

from playsound import playsound
from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term

conn = sqlite3.connect("assistant.db")
cursor = conn.cursor()

@eel.expose
def playAssistantSound():
    audio_file = "www\\assets\\audio\\start_sound.mp3" 
    playsound(audio_file)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":
        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])
                else:
                    speak("Opening "+query)
                    try:
                        # os.system('start '+query)
                        autogui.press("super")
                        autogui.typewrite(app_name)
                        autogui.sleep(2)
                        autogui.press("enter")
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

def SearchGoogle(query):
    speak("What do you want to search on google?")
    kit.search(query)

def SearchWikipedia(query):
    speak("Searching from Wikipedia")
    query = query.replace("wikipedia", "")
    query = query.replace("search wikipedia", "")
    results = wikipedia.summary(query, sentences = 2)
    speak("According to Wikipedia")
    print(results)
    speak(results)

def temperatureSearch(query):
    if "temperature" in query or "weather" in query:
        search = "temperature in Viet Nam"
        url = f"https://www.google.com/search?q={search}"
        try:
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp = data.find("div", class_="BNeawe").text
            speak(f"Current {search} is {temp}")
        except Exception as e:
            speak("Sorry, I couldn't retrieve the temperature at the moment.")

def getCurrentDateTime(query):
    if "time" in query:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        speak(f"The current time is {current_time}")
    elif "date" in query:
        now = datetime.datetime.now()
        current_date = now.strftime("%d-%m-%Y")
        speak(f"Today's date is {current_date}")

def shutdownSystem():
    system_platform = platform.system()
    if system_platform == "Windows":
        os.system("shutdown /s /t 1")
    elif system_platform == "Linux":
        os.system("shutdown now")
    elif system_platform == "Darwin":  # macOS
        os.system("shutdown -h now")
    else:
        # Hệ điều hành không được hỗ trợ
        print("Shutdown not supported on this operating system")

def scheduleDay(task, filepath): 
    try: 
        with open(filepath, "a") as file:
            file.write(task + "\n")
        print("Task added")
    except Exception as e:
       print(f"Have an error {e}")

def setArlam(hour, minute):
    now = time.localtime()
    current_hour = now.tm_hour
    current_minute = now.tm_min

    alarm_time = hour * 3600 + minute * 60
    current_time = current_hour * 3600 + current_minute * 60

    if alarm_time < current_time:
        speak("")

def translateLanguage(element):
    print(element)
    translator = Translator()
    translated = translator.translate(element, src='en', dest='vi')
    speak(str(translated.text))
    print(translated.text)

def keyword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
        porcupine=pvporcupine.create(keywords=["americano","computer"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detected for not
            if keyword_index>=0:
                print("keyword detected")

                # pressing shortcut key win+b
                autogui.keyDown("win")
                autogui.press("b")
                time.sleep(2)
                autogui.keyUp("win")
                
    except Exception as e:
        print("An error occurred:", e)

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookie.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

def sendEmail():
    return True