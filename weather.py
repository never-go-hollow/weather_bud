import PIL
import requests
import tkinter as tk
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
import json, urllib.request
from air_pollution_level import AirPollutionLevel, city_aqi
import sqlite3
from datetime import datetime

# Scrape dat ugly-ass dynamic image link huh
page = requests.get('https://m.meteo.pl/gdynia/60')
soup = BeautifulSoup(page.text, 'html.parser')
images = []
for img in soup.findAll('img'):
    images.append(img.get('src'))

# Download mentioned image and slice it
date = images[2]
urllib.request.urlretrieve(date, "pogoda.png")
obraz = Image.open("./pogoda.png")
crop_opady = obraz.crop((38,143,695+88,80+143))
crop_temperatura = obraz.crop((38,55,695+88,78+60))
crop_timeline = obraz.crop((68,27,665+88,21+37))
crop_timeline_bot = obraz.crop((68,27,665+88,1231+27))

# Read token from secrets.conf
with open('secrets.conf', 'r') as file:
    token = file.read().replace('\n', '')

# Save all cropped images
crop_opady.save("cropped_opady" + ".png")
crop_temperatura.save("cropped_temperatura" + ".png")
crop_timeline.save("cropped_timeline" + ".png")
crop_timeline_bot.save("cropped_timeline_bot" + ".png")

# Request air quality data from aqicn.org; extract and present the most important information
air_quality_url = 'https://api.waqi.info/feed/gdynia/?token={}'.format(token)
with urllib.request.urlopen(air_quality_url) as url:
    air_quality_text = json.loads(url.read().decode())['data']['aqi']

# Check the range that current air quality index lies within
r1 = range(0, 50)
r2 = range(51, 100)
r3 = range(101, 150)
r4 = range(151-200)
r5 = range(201-300)

def check_aqi(aqt):
    if aqt in r1:
        return city_aqi.good
    elif aqt in r2:
        return city_aqi.moderate
    elif aqt in r3:
        return city_aqi.unhealthy
    elif aqt in r4:
        return city_aqi.very_unhealthy
    elif aqt in r5:
        return city_aqi.poor
    else:
        return city_aqi.hazardous

aqi_txt = "Air Quality Index in Gdynia at the moment: " + str(air_quality_text)
aqi_txt_imported = check_aqi(air_quality_text)

# Tkinter, main window; import cropped images as 'widgets', import air quality data
window = tk.Tk()
window.geometry("740x370")
window.title("WeatherBud")

img_time = "cropped_timeline.png"
img_temp = "cropped_temperatura.png"
img_opady = "cropped_opady.png"
img_temp_bot = "cropped_timeline_bot.png"

img = ImageTk.PhotoImage(Image.open(img_time))
img2 = ImageTk.PhotoImage(Image.open(img_temp))
img3 = ImageTk.PhotoImage(Image.open(img_opady))
img4 = ImageTk.PhotoImage(Image.open(img_temp_bot))

aqi_panel = tk.Label(window, text = aqi_txt, height = 1)
aqi_panel2 = tk.Label(window, text = aqi_txt_imported, height = 4)
panel = tk.Label(window, image = img)
panel2 = tk.Label(window, image = img2)
panel3 = tk.Label(window, image = img3)
panel4 = tk.Label(window, image = img4)

aqi_panel.pack()
aqi_panel2.pack()
panel.pack(side = "top", expand = "no")
panel2.pack(side = "top", expand = "no")
panel3.pack(side = "top", expand = "no")
panel4.pack(side = "top", expand = "no")

window.mainloop()

# Check current time and format it correctly, connect to database; create it if it doesn't exist, add entry
curr_time = str(datetime.now().strftime("%Y-%m-%d [%H:%M]"))

conn = sqlite3.connect("aqi_gdynia.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS customers (
            time text,
            quality text)
            """)

def new_entry():
    time = curr_time
    quality = air_quality_text
    c.execute("INSERT INTO customers (time, quality) VALUES(?, ?)", (time, quality))
    c.execute("SELECT * FROM customers")

new_entry()

# Show all db entries in the terminal window; unsure about it but I'll just leave it like that for now
items = c.fetchall()
for item in items:
    print(item)

conn.commit()
conn.close()
