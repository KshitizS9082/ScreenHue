"""
RGB Bulb Device
"""
import time
import tinytuya

import json
lampDetails=None
with open('devices.json', "r") as f:
    devices = json.load(f)
    for device in devices:
        if(device["name"]=="Lamp"):
            lampDetails=device
assert lampDetails!=None
DEVICE_ID=lampDetails["id"]
LOCAL_KEY=lampDetails["key"]
IP_ADDRESS=lampDetails["ip"]
VERSION=lampDetails["version"]
VERSION=float(VERSION)

d = tinytuya.BulbDevice(DEVICE_ID, IP_ADDRESS, LOCAL_KEY, version=VERSION)
d.set_version(3.4)  # IMPORTANT to set this regardless of version
d.set_socketPersistent(True)  # Optional: Keep socket open for multiple commands
data = d.status()

# Show status of first controlled switch on device
print('Dictionary %r' % data)

# Set to RED Color - set_colour(r, g, b):
d.turn_on()
d.set_colour(255,244,0)  
d.set_brightness_percentage(100)

import mss
from PIL import Image
from colorthief import ColorThief
import io
def capture_screen():
    with mss.mss() as sct:
        # Capture a small portion of the screen (e.g., 200x200 pixels from the center)
        monitor = {
            "top": 540,    # 540px from the top of the screen
            "left": 960,   # 960px from the left of the screen
            "width": 200,  # 200px wide
            "height": 200  # 200px tall
        }
        sct_img = sct.grab(monitor)
        
        # Convert the captured screen to a PIL image
        img = Image.frombytes('RGB', (sct_img.width, sct_img.height), sct_img.rgb)
        
        return img

def get_dominant_color(image):
    # Save image to an in-memory file
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    
    # Use ColorThief to get the dominant color
    color_thief = ColorThief(io.BytesIO(img_byte_arr))
    dominant_color = color_thief.get_color(quality=1)
    
    return dominant_color

from colorsysx import rgb_to_hsv

from math import sqrt
old_color = (0, 0, 0)
while True:
    start = time.time()
    screen_image = capture_screen()
    dominant_color = get_dominant_color(screen_image)
    if old_color == dominant_color:
        continue
        # pass
    else:
        r, g, b = dominant_color
        d.set_colour(r,g,b)  
        # brigtness = sqrt((r*r+b*b+g*g)/3)*100/255
        # d.set_brightness_percentage(brigtness)
        print(f"New Color: {dominant_color}")
        old_color = dominant_color
    print("time taken: ", time.time()-start)
    # Wait for a few seconds before the next capture
    # time.sleep(1)  # Adjust the sleep time as needed