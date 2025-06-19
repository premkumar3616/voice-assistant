from ipaddress import summarize_address_range
from adodbapi.apibase import pyTypeToADOType
from pyautogui import leftClick
from pyexpat.errors import messages
from re import search, split
import requests
import pyttsx3
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import imdb
import wolframalpha
import pyautogui
import webbrowser
import time
import socket
from datetime import datetime
from decouple import config
from conv import random_text
from online import find_my_ip, youtube, search_on_google, search_on_wikipedia, send_email, get_news
from random import choice
import cv2



engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.0)
engine.setProperty('rate',225)
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[1].id)
USER = config('USER')
HOSTNAME = config('BOT')


def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_me():
     hour = datetime.now().hour
     if (hour>6) and (hour < 12):
         speak(f"Good Morning {USER}")
     elif (hour >=12) and (hour < 16):
         speak(f"Good Afternoon {USER}")
     elif (hour>=16) and (hour < 21):
         speak(f"Good Evening {USER}")
     speak(f"Hi i am {HOSTNAME}, How may i assist you?{USER}")
listening = False

def start_listening():
    global listening
    listening = True
    print("started Listening")

def pause_listening():
    global listening
    listening = False
    print("Stopped listening")
keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


def take_Command():
    if not listening:
        return 'none'

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)  # Reduce noise
        r.pause_threshold = 1  # Allow some silence
        print("Listening...")

        for _ in range(3):  # Allow up to 3 retries
            try:
                audio = r.listen(source, timeout=5)
                print("Recognizing...")
                query = r.recognize_google(audio, language='en-in')
                print(f"User said: {query}")
                stop_words = ["stop", "exit", "quit", "shutdown", "bye"]
                if any(word in query for word in stop_words):
                    speak("Goodbye! Have a great day!")
                    exit()
                return query.lower()
            except sr.UnknownValueError:
                print("Could not understand. Please repeat.")
                speak("Sorry, I didn't catch that. Can you repeat?")
            except sr.RequestError:
                print("Network error. Please check your internet connection.")
                speak("I am having trouble connecting to the speech service. Please check your internet.")
                return 'none'
            except Exception as e:
                print(f"Error: {e}")
                speak("An error occurred while recognizing your voice. Please try again.")
                return 'none'

    print("Max retries reached. Unable to understand.")
    speak("I'm sorry, but I couldn't understand your command.")
    return 'none'


def subscribe_to_channel(channel_name):
    """Subscribe to a YouTube channel by searching for it and clicking the subscribe button."""
    speak(f"Now I am subscribing to the channel {channel_name}")
    webbrowser.open("https://www.youtube.com/")
    time.sleep(3)

    # Locate and click search bar
    search_bar = locate_and_click("search_bar.png")
    if search_bar:
        pyautogui.typewrite(channel_name, interval=0.1)
        pyautogui.press('enter')
    else:
        speak("Could not locate the search bar.")
        return

    time.sleep(3)

    # Locate and click the channel name from search results
    channel_name_location = locate_and_click("channel_name.png")
    if not channel_name_location:
        speak("Could not locate the channel. Please try again.")
        return

    time.sleep(2)

    # Locate and click the subscribe button
    subscribe_button = locate_and_click("subscribe_button.png")
    if subscribe_button:
        speak("Subscription successful!")
    else:
        speak("Could not find the subscribe button.")

def locate_and_click(image_path, click=True, confidence=0.7):
    """Locate an image on the screen using OpenCV and click it."""
    location = pyautogui.locateOnScreen(image_path, confidence=confidence)
    if location:
        x, y = pyautogui.center(location)
        if click:
            pyautogui.click(x, y)
        return x, y
    else:
        print(f"Could not locate {image_path}")
        return None

def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=b5d926d3ca9c31ad3266e7b71537cdaa"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            weather_desc = data["weather"][0]["main"]
            return weather_desc, temp, feels_like

        else:
            speak("Sorry, I couldn't fetch the weather details.")
            return None, None, None

    except requests.exceptions.RequestException:
        speak("I couldn't connect to the weather service. Check your internet connection.")
        return None, None, None


def check_internet():
    """Checks if the internet is available."""
    try:
        socket.create_connection(("8.8.8.8", 53))  # Google's DNS server
        return True
    except OSError:
        return False
if __name__ == '__main__':
    # speak('Hi i am your virtual assistant')
    # print('hi am i am your virtual assistant')
    greet_me()
    while True:
        if not check_internet():
            speak("It looks like you're offline. Some features may not work.")
        if listening:
            query = take_Command().lower()
            if "how are you" in query or "how r u" in query:
                speak("I'm good! Thanks for asking. How about you?")
            elif "open command prompt" in query:
                speak("opening command prompt")
                os.system('start cmd')
            elif "open camera" in query:
                speak("opening camera")
                sp.run('start microsoft.windows.camera:',shell=True)
            elif "open notepad" in query:
                speak("Opening notepad")
                notepad_path="C:\\Users\\prem kumar\\AppData\\Local\\Microsoft\\WindowsApps\\Microsoft.WindowsNotepad_8wekyb3d8bbwe\\notepad.exe"
                os.startfile(notepad_path)
            # elif "open whatsapp" in query:
            #     speak("Opening whatsapp")
            #     wapp_path="C:\\Users\\prem kumar\\AppData\\Local\\Microsoft\\WindowsApps\\whatsapp.exe"
            #     os.startfile(wapp_path)
            elif "ip address" in query:
                ip_address= find_my_ip()
                speak(f"your ip address id {ip_address}")
                print(f"your ip address id {ip_address}")
            elif "open youtube" in query:
                speak("What do you want to play on youtube sir?")
                video = take_Command().lower()
                youtube(video)
            elif "open google" in query:
                speak("What do you want to search on google?")
                query = take_Command().lower()
                search_on_google(query)
            elif "wikipedia" in query:
                speak(f"What do you want to search on wikipedia {USER}")
                search = take_Command().lower()
                results = search_on_wikipedia(search)
                if results:
                    speak(f"According to Wikipedia, {results}")
                    print(results)
                else:
                    speak("Sorry, I couldn't find any relevant information.")
            elif "send an email" in query:
                speak("To whom should i send sir?. Please enter the email address of the person in terminal")
                reciever_add=input("Enter Email address: ")
                speak("What should be the subject?")
                subject=take_Command().capitalize()
                speak("what is the message?")
                message=take_Command().capitalize()
                if send_email(reciever_add,subject,message):
                    speak("I have sent the message sir")
                else:
                    speak("Sorry sir! some error has occur please check the error log")
            elif "give me news" in query:
                speak(f"I am reading out the latest news of today")
                speak(get_news())
                speak("I am printing it on screen sir!")
                print(get_news(),sep='\n')
            elif "weather" in query:
                speak("Tell me the name of your city")
                city = input("Enter the name of your city: ")
                speak(f"Getting weather report of your city {city}")

                weather, temp, feels_like = get_weather(city)

                if weather and temp and feels_like:
                    speak(f"The current temperature is {temp}°C, but it feels like {feels_like}°C.")
                    speak(f"Also, the weather report talks about {weather}.")
                    print(f"Description: {weather}\nTemperature: {temp}°C\nFeels like: {feels_like}°C")
                else:
                    speak("I couldn't get the weather details right now.")
            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak(f"Please tell me the movie name")
                text=take_Command()
                movies=movies_db.search_movie(text)
                speak("Searching for"+text)
                speak("I found these")
                for movie in movies:
                    title= movie["title"]
                    year = movie["year"]
                    speak(f"{title}--{year}")
                    info= movie.getID()
                    movie_info=movies_db.get_movie(info)
                    rating=movie_info["rating"]
                    cast=movie_info["cast"]
                    actors=cast[0:5]
                    plot=movie_info.get('plot outline','plot summary is not available')
                    speak(f"{title} was released in {year} has imdb ratings of {rating}.It has a cast of{actors}."
                          f" The plot summary of the movie is {plot}")
                    print(
                        f"{title} was released in {year} has imdb ratings of {rating}.It has a cast of{actors}."
                        f" The plot summary of the movie is {plot}")
            elif "calculate" in query:
                app_id="KU6UHY-285J7WHKVR"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind +1:]
                result= client.query(" ".join(text))
                try:
                    ans= next(result.results).text
                    speak("The answer is "+ans)
                    print("The answer is " + ans)
                except StopIteration:
                    speak("Sorry i couldn't find that, please try again")
            elif "what is" in query or "who is" in query or "which is" in query:
                app_id="KU6UHY-285J7WHKVR"
                client = wolframalpha.Client(app_id)
                try:
                    ind = query.lower().index('what is') if "what is" in query.lower() else \
                        query.lower().index('who is') if 'who is' in query.lower() else \
                        query.lower().index('which is') if 'which is' in query.lower() else None
                    if ind is not None:
                        text= query.split()[ind + 2:]
                        result=client.query(" ".join(text))
                        ans = next(result.results).text
                        speak("The answer is "+ans)
                        print("The answer is "+ans)
                    else:
                        speak("I couldn't find that")
                except StopIteration:
                    speak("I couldn't find that.Please try again")
            # elif "subscribe" in query:
            #     speak("what is the channel name?")
            #     channel=take_Command().lower()
            #     speak(f"Now i am subcribing to the channel {channel}")
            #     webbrowser.open("https://www.youtube.com/")
            #     pyautogui.moveTo(806,125,1)
            #     pyautogui.click(x=806,y=125,clicks=1,interval=0,button='left')
            #     pyautogui.typewrite(channel,0.1)
            #     time.sleep(1)
            #     pyautogui.press('enter')
            #     pyautogui.moveTo(971,314,1)
            #     pyautogui.moveTo(1638,314,1)
            #     pyautogui.click(x=1638,y=314,clicks=1,interval=0,button='left')
            #     pyautogui.moveTo(1750,314,1)
            #     pyautogui.click(x=1750,y=314,clicks=1,interval=0,button='left')
            #     pyautogui.click(x=1750,y=320,clicks=1,interval=0,button='left')

            elif "subscribe" in query:
                speak("What is the channel name?")
                channel_name=input("Enter channel name: ")
                subscribe_to_channel(channel_name)
            elif "functions" in query:
                speak("I am now reading out the functions i can do :")
                list = ['greets you','sending email','open browser and searching','opening youtube and playing video',
                        'updating you with latest news','weather report','calculating basic sums',
                        'say some something about entertainment','subscribe to particular channel in youtube',
                        'information about something or someone using wikipedia','telling about movies']
                for i in list:
                    speak(f'{i}')
                speak("i am now printing it on terminal")
                for i in list:
                    print(f'{i}')
                speak('what do you need me to do?')