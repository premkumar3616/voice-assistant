import os

import requests
import pywhatkit as kit
import wikipedia
from email.message import EmailMessage
from decouple import config
import smtplib

EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")


def find_my_ip():
    ip_address= requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]
def search_on_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)  # Fetch first 2 sentences
        return results
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Your search query is too broad. Try specifying: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find anything on Wikipedia for that."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def search_on_google(query):
    kit.search(query)
def youtube(video):
    kit.playonyt(video)

def send_email(reciever_add,subject,message):
    try:
        email=EmailMessage()
        email['To']=reciever_add
        email['Subject']=subject
        email['From']=EMAIL
        email.set_content(message)

        s=smtplib.SMTP("smtp.gmail.com",587)
        s.starttls()
        s.login(EMAIL,PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False

def get_news():
    news_headline=[]
    result= requests.get(f"https://newsapi.org/v2/everything?q=tesla&from=2025-01-22&sortBy=publishedAt&apiKey=6fc291c6b9524a63858422dea3ce3562").json()
    articles= result["articles"]
    for article in articles:
        news_headline.append(article["title"])
    return news_headline[:6]
def get_weather(city):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=6fc291c6b9524a63858422dea3ce3562&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                temp = data["main"]["temp"]
                weather_desc = data["weather"][0]["description"]
                speak(f"The temperature in {city} is {temp}°C with {weather_desc}.")
            else:
                speak("Sorry, I couldn't fetch the weather details.")
        except requests.exceptions.RequestException:
            speak("I couldn't connect to the weather service. Check your internet connection.")