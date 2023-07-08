import network
import json
from time import sleep
import urequests
from picounicorn import PicoUnicorn
import sys
import secrets
from character_map import CHARACTERS

API_KEY = secrets.WEATHER_API_DOT_COM_API_KEY
POSTAL_CODE = secrets.POSTAL_CODE
WEATHER_URI = "https://api.weatherapi.com/v1/current.json?key=" + API_KEY + "&q=" + POSTAL_CODE + "&aqi=no"
CONNECTED = False


def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.WIFI_NETWORK, secrets.WIFI_PASSWORD)
    while wlan.isconnected() == False:
        sleep(1)
        continue
    CONNECTED = True
    ip = wlan.ifconfig()[0]
    print("Connected on " + ip)
    return ip


def get_forecast():
    try:
        request = urequests.get(WEATHER_URI)
        res = request.content
        request.close()
        data = json.loads(res)
        target_key = "temp_c"
        if secrets.USE_CELSIUS is False:
            target_key = "temp_f"
        fl_val = float(data["current"][target_key])
        return fl_val
    except Exception as e:
        print(e)
        sleep(10)
    return get_forecast()


picounicorn = PicoUnicorn()
# picounicorn.set_pixel(0, 0, 255, 255, 255)
sleep(2)
connect()

w = picounicorn.get_width()
h = picounicorn.get_height()


def set_display_all_colours(r, g, b):
    # Reset the display
    for x in range(w):
        for y in range(h):
            picounicorn.set_pixel(x, y, r, g, b)


# Display a rainbow across Pico Unicorn

r = 255
g = 255
b = 255

RED = [255, 0, 0]
ORANGE = [255, 165, 0]
YELLOW = [255, 255, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
INDIGO = [75, 0, 130]
VIOLET = [238, 130, 238]

set_display_all_colours(0, 0, 0)
set_display_all_colours(RED[0], RED[1], RED[2])
sleep(1 / 4)
set_display_all_colours(ORANGE[0], ORANGE[1], ORANGE[2])
sleep(1 / 4)
set_display_all_colours(YELLOW[0], YELLOW[1], YELLOW[2])
sleep(1 / 4)
set_display_all_colours(GREEN[0], GREEN[1], GREEN[2])
sleep(1 / 4)
set_display_all_colours(BLUE[0], BLUE[1], BLUE[2])
sleep(1 / 4)
set_display_all_colours(INDIGO[0], INDIGO[1], INDIGO[2])
sleep(1 / 4)
set_display_all_colours(VIOLET[0], VIOLET[1], VIOLET[2])
sleep(1 / 4)
set_display_all_colours(ORANGE[0], ORANGE[1], ORANGE[2])
sleep(1 / 4)
set_display_all_colours(YELLOW[0], YELLOW[1], YELLOW[2])
sleep(1 / 4)
set_display_all_colours(GREEN[0], GREEN[1], GREEN[2])
sleep(1 / 4)
set_display_all_colours(BLUE[0], BLUE[1], BLUE[2])
sleep(1 / 4)
set_display_all_colours(INDIGO[0], INDIGO[1], INDIGO[2])
sleep(1 / 4)
set_display_all_colours(VIOLET[0], VIOLET[1], VIOLET[2])
sleep(1 / 4)

counter = 0
while True:
    counter += 1
    fl_number = get_forecast()
    string_number = '%.1f' % fl_number
    rgb = [r, g, b]

    offset = 1
    set_display_all_colours(0, 0, 0)
    for a_number in string_number:
        number_width = CHARACTERS[a_number]["width"]
        characters = CHARACTERS[a_number]["chars"]
        for char in characters:
            x_pos = (char[0] + offset)
            if x_pos > w - 1:
                continue
            picounicorn.set_pixel(x_pos, (char[1] + 1), rgb[0], rgb[1], rgb[2])
        offset += (number_width + 1)
    print("Read... " + string_number)
    sleep(10)
