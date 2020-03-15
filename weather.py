from PIL import Image
from datetime import date
import urllib.request

# Import actual time and format it appropriately
import_time = date.today()
formatted_time = str(import_time.strftime("%Y%m%d"))

# Download images and crop 'em
date = "https://www.meteo.pl/um/metco/mgram_pict.php?ntype=0u&fdate=" + formatted_time + "12&row=342&col=208&lang=pl"
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
