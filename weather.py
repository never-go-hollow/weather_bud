import PIL
import requests
from PIL import Image
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
crop_opady = obraz.crop((68,143,495+68,80+143))
crop_temperatura = obraz.crop((68,55,495+68,80+55))
crop_timeline = obraz.crop((68,27,495+68,25+27))

# Show and save all cropped images
crop_opady.show()
crop_opady.save("cropped_opady" + ".png")

crop_temperatura.show()
crop_temperatura.save("cropped_temperatura" + ".png")

crop_timeline.show()
crop_timeline.save("cropped_timeline" + ".png")
