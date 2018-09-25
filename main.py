from weather import Weather, Unit
import feedparser
from flask import Flask, render_template
from datetime import datetime
import json

app = Flask(__name__)
WOEID = 12799510

@app.route("/")
def home():
    return render_template("index.html",
                        weather=get_weather_formatted(), 
                        classes=get_classes(),
                        homework=get_homework(),
                        imgur_album="nCUUFIa")

@app.route("/news")
def news():
    return render_template("news.html", headlines=get_headlines("https://reddit.com/r/worldnews.rss", 3))

@app.route("/weather")
def weather():
    file_str = "cloud.png"
    return render_template("weather.html", location=get_location(), weather_img=file_str, date=get_date_formatted(), weather=get_weather_formatted())

@app.route("/school")
def school():
    return render_template("school.html", classes=get_classes(), homework=get_homework())

@app.route("/twitter")
def twitter():
    return render_template("twitter.html")

@app.route("/imgur")
def imgur():
    return render_template("imgur.html", imgur_album="nCUUFIa")

def get_homework():
    with open("static/data/school_data.json") as f:
        d = json.loads(f.read())
        return d["homework"][str(datetime.today().weekday())]

def get_classes():
    with open("static/data/school_data.json") as f:
        d = json.loads(f.read())
        return d["classes"][str(datetime.today().weekday())]

def get_date_formatted():
    return get_weather().condition.date

def get_location():
    return get_weather().location.city

def get_weather_formatted():
    w = get_weather().condition
    return "It's currently {} and {}°F outside.".format(w.text, w.temp)

def get_weather():
    return Weather(unit=Unit.FAHRENHEIT).lookup(WOEID)

def get_headlines_formatted(url, number):
    headlines = get_headlines(url, number)
    headlines_listed = ""
    for i in range(0, len(headlines)):
        if i == (len(headlines) - 1):
            headlines_listed += " and \"" + headlines[i] + "\"."
        else:
            headlines_listed += "\"" + headlines[i] + "\","

    return headlines_listed[:-1] + "."

def get_headlines(url, number):
    headlines = []
    rss_data = feedparser.parse(url)


    for i in range(0, number):
        try:
            headlines.append(rss_data.entries[i]["title"])
        except KeyError:
            break
    	
    return headlines

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
