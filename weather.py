import PIL
import requests
import tkinter as tk
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
import urllib.request

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
crop_timeline_bot = obraz.crop((68,27,665+88,1222+37))

# Save all cropped images

crop_opady.save("cropped_opady" + ".png")
crop_temperatura.save("cropped_temperatura" + ".png")
crop_timeline.save("cropped_timeline" + ".png")
crop_timeline_bot.save("cropped_timeline_bot" + ".png")

# Tkinter, main window
window = tk.Tk()
window.geometry("740x285")
window.title("WeatherBud")

img_time = "cropped_timeline.png"
img_temp = "cropped_temperatura.png"
img_opady = "cropped_opady.png"
img_temp_bot = "cropped_timeline_bot.png"

img = ImageTk.PhotoImage(Image.open(img_time))
img2 = ImageTk.PhotoImage(Image.open(img_temp))
img3 = ImageTk.PhotoImage(Image.open(img_opady))
img4 = ImageTk.PhotoImage(Image.open(img_temp_bot))

panel = tk.Label(window, image = img)
panel2 = tk.Label(window, image = img2)
panel3 = tk.Label(window, image = img3)
panel4 = tk.Label(window, image = img4)

panel.pack(side = "top", expand = "no")
panel2.pack(side = "top", expand = "no")
panel3.pack(side = "top", expand = "no")
panel4.pack(side = "top", expand = "no")

window.mainloop()
