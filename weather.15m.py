#!/usr/bin/env python
# -*- coding: utf-8 -*-

# <bitbar.title>Weather - OpenWeatherMap</bitbar.title>
# <bitbar.version>v1.0.2</bitbar.version>
# <bitbar.author>Daniel Seripap</bitbar.author>
# <bitbar.author.github>seripap</bitbar.author.github>
# <bitbar.desc>Grabs simple weather information from openweathermap. Needs configuration for location and API key.</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

# Alexandre Espinosa Menor: added icon (resized to 30x30 px)
# It needs import Image, os and base64 to work

import json
import urllib2
from random import randint

import base64
from PIL import Image
import os


location = '3109642' #Ames, Galiza
api_key = ''
units = 'metric' # kelvin, metric, imperial
lang = 'gl'

def get_wx():

  if api_key == "":
    return False

  try:
    wx = json.load(urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?id=' + location + '&units=' + units + '&lang=' + lang + '&appid=' + api_key + "&v=" + str(randint(0,100))))
  except urllib2.URLError:
    return False

  if units == 'metric':
    unit = 'C'
  elif units == 'imperial':
    unit = 'F'
  else:
    unit = 'K' # Default is kelvin

  # more data from # <bitbar.title>OWM_Weather</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Jack Zhang</bitbar.author>
  try:
    weather_data = {
      'temperature': str(int(round(wx['main']['temp']))),
      'condition': str(wx['weather'][0]['description'].encode('utf-8')),
      'city': wx['name'],
      'feels_like': str(int(round(wx['main']['feels_like']))),
      'temp_min': str(int(round(wx['main']['temp_min']))),
      'temp_max': str(int(round(wx['main']['temp_max']))),
      'unit': '°' + unit,
      'icon': str(wx['weather'][0]['icon']),
    }
  except KeyError:
    return False

  return weather_data

def render_wx():
  weather_data = get_wx()

  if weather_data is False:
    return 'Could not get weather'

  img = save_icon_and_get_encoded(weather_data['icon'])

  # test with real image (at night is just a black dot)
  #img = save_icon_and_get_encoded("10d")


  string_to_return = weather_data['condition'] + ' ' + weather_data['temperature'] + weather_data['unit'] + "| templateImage="+ img +"\n"
  string_to_return += "---" +"\n"

  string_to_return += "Feels like: " + weather_data['feels_like'] + weather_data['unit'] +"\n"
  string_to_return += "Temp_min: " + weather_data['temp_min'] + weather_data['unit'] + " / " + "Temp_max: " + weather_data['temp_max'] + weather_data['unit']

  #return weather_data['condition'] + ' ' + weather_data['temperature'] + weather_data['unit'] + "| templateImage="+ img
  return string_to_return 


# download icon if we haven't previously download
# and encode img
def save_icon_and_get_encoded(icon):
  imgTmp = "/tmp/icon-weather-bitbar-" +icon+ ".png"
  imgTmpResized = "/tmp/icon-weather-bitbar-" +icon+ "-encoded.png"

  # check if exists encoded icon to skip connections
  if os.path.isfile(imgTmpResized) == False:
  	url = "http://openweathermap.org/img/wn/" + icon + ".png"

  	imgRequest = urllib2.Request(url)
  	imgData = urllib2.urlopen(imgRequest).read()

  	output = open(imgTmp,'wb')
  	output.write(imgData)
  	output.close()

  	# resize to 30x30 (images are 50x50, looks too big on my imac)
  	img = Image.open(imgTmp)
  	img = img.resize((30, 30), Image.ANTIALIAS)
  	img.save(imgTmpResized)

  with open(imgTmpResized, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

  if os.path.isfile(imgTmp):
    os.remove(imgTmp)

  return encoded_string


print render_wx()
