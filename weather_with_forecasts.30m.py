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
#
# 2022-08-03: added forecasts using new url ('forecast' instead of 'weather')
#

import datetime
import json
import string
import urllib2
from random import randint

import base64
from PIL import Image
import os


location = '3109642'
api_key = ''
units = 'metric' # kelvin, metric, imperial
lang = 'gl'


def get_wx():
  """Get infor from openweathermap, using free api (forecast endpoint). Returns array with: first key with actually temp, next keys with forecasts"""

  if api_key == "":
    return False

  try:
    url = 'http://api.openweathermap.org/data/2.5/forecast'
    wx = json.load(urllib2.urlopen(url + '?id=' + location + '&units=' + units + '&lang=' + lang + '&appid=' + api_key + "&v=" + str(randint(0,100))))
    #print( url + '?id=' + location + '&units=' + units + '&lang=' + lang + '&appid=' + api_key + "&v=" + str(randint(0,100)))
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

# actually we need to parse hourly forecast 
  try:
    weather_data = []
    for prevision in wx['list']:
      weather_data.append({
        'temperature': str(round(prevision['main']['temp'], 1)),
        'condition': str(prevision['weather'][0]['description'].encode('utf-8')),
        'feels_like': str(round(prevision['main']['feels_like'], 1)),
        'unit':  unit,
        'icon': str(prevision['weather'][0]['icon']),
        'time': prevision['dt_txt']
      })
  except KeyError:
    return False

  return weather_data



def render_wx():
  """returns string to render with xbar, use get_wx() returned array with data"""
  weather_data = get_wx()
  
  if weather_data is False:
    return 'Could not get weather'

  # get first element to header
  first_element = weather_data[:1][0]
  img = save_icon_and_get_encoded(first_element['icon'])

  # 
  string_to_return = first_element['condition'] + ' ' + first_element['temperature'] + first_element['unit'] + "| templateImage="+ img +"\n"
  string_to_return += "---" +"\n"

  # loop data to: 1) split by day; 2) get min and max from each day; 3) get most frequent description from each day
  detailed_forecast = ''
  day = ''
  hour = ''
  day_temps = {}
  day_forecast_descriptions = {}
  day_icons = {}
  for prevision in weather_data[1:]:
    # separation by day and show by hour
    if day !=  prevision['time'].split(' ')[0]:
      day = prevision['time'].split(' ')[0]  
      detailed_forecast += day +"\n"
      day_temps[day] = []
      day_forecast_descriptions[day] = []
      day_icons[day] = []
    # else:
    #   detailed_forecast += "--.."

    day_temps[day].append(prevision['temperature'])
    day_forecast_descriptions[day].append(prevision['condition'])
    day_icons[day].append(prevision['icon'])

    hour = ':'.join(str(e) for e in prevision['time'].split( ' ')[1].split(':')[:2])
    img = save_icon_and_get_encoded(prevision['icon'])
    detailed_forecast += "--.." + hour + ": " + prevision['condition'] + " " +prevision['temperature'] + prevision['unit']
    detailed_forecast += " | color=#000000"
    detailed_forecast += " | templateImage=" + img +"\n"

  # we need to order dictionary
  for d in sorted(day_temps.items()):
    day_temp = d[0]
    img = save_icon_and_get_encoded(most_frequent(day_icons[day_temp]))

    string_to_return += day_temp +": " + max(day_temps[day_temp]) + prevision['unit'] + " - " + min(day_temps[day_temp]) + prevision['unit'] 
    string_to_return += " (" + most_frequent(day_forecast_descriptions[day_temp]) + ")"
    string_to_return += " | color=#000000"
    string_to_return += " | templateImage=" + img +"\n"

  string_to_return += "---\n"
  string_to_return += "Detailed:\n" + detailed_forecast.rstrip()
  
  # print(string_to_return)

  return string_to_return 



def save_icon_and_get_encoded(icon):
  """# download icon if we haven't previously download and encode img"""
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

  	# resize to 30x30 (images are 50x50, looks too big on my mac mini)
  	img = Image.open(imgTmp)
  	img = img.resize((30, 30), Image.ANTIALIAS)
  	img.save(imgTmpResized)

  with open(imgTmpResized, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

  if os.path.isfile(imgTmp):
    os.remove(imgTmp)

  return encoded_string



def most_frequent(List):
    return max(set(List), key = List.count)


print render_wx()
