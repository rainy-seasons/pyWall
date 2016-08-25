#! python3

import re
import os
import sys
import datetime
import requests
import urllib
import shutil
import codecs
import ctypes
from random import randint
from bs4 import BeautifulSoup

imgDir = None
catNum = None
category = ""
nowTime = str(datetime.datetime.now().time()).replace(':', '.')
defaultSave = "cc_" + str(datetime.datetime.now().date()) + "_" + nowTime + ".png"

# handle argument inputs
if len(sys.argv) == 2:
	category = sys.argv[1]
	saveDir = defaultSave
	imgDir = str(os.getcwd()) + "\\" + saveDir
elif len(sys.argv) == 3:
	category = sys.argv[1]
	saveDir = sys.argv[2] + ".png"
	imgDir = saveDir
elif len(sys.argv) == 1:
	saveDir = defaultSave
	imgDir = str(os.getcwd()) + "\\" + saveDir

# set the url parameter based on category input
if category.lower() == "anime":
	catNum = '010'
elif category.lower() == "people":
	catNum = '001'
elif category.lower() == "general":
	catNum = '100'
elif category.lower() == "all":
	catNum = '111'
else:
	catNum = '111'

url = 'https://alpha.wallhaven.cc/search?categories=' + catNum + '&purity=100&resolutions=1920x1080&sorting=favorites&order=desc&page='
page = randint(1,20)
endpoint = url + str(page)
linkArray = []

def DownloadImage(link):
	response = requests.get('https:' + link)
	if response.status_code == 200:
		f = open(saveDir, 'wb')
		f.write(response.content)
		f.close()

# scrapes a random page in the favorites section
def ParseFavs():
	links = []
	for link in soup.find_all("a"):
		href = link.get("href")
		if not href:
			continue
		if "favorites" in href:
			continue
		if "thumbTags" in href:
			continue
		if "wallpaper" not in href:
			continue
		links.append(href)
		linkArray.append(href)
	return links

# get the direct image link for the wallpaper
def ParseImage():
	for link in soup.find_all("meta"):
		cont = link.get("content")
		if not cont:
			continue
		if "wallpapers.wallhaven.cc/wallpapers" not in cont:
			continue
		DownloadImage(cont)


r = requests.get(endpoint)
soup = BeautifulSoup(r.content, 'html.parser')


i = randint(0,len(ParseFavs()))
imagePage = linkArray[i]

r = requests.get(imagePage)
soup = BeautifulSoup(r.content, 'html.parser')

ParseImage()

# set current wallpaper to the downloaded image
SPI_SETDESKWALLPAPER = 20
ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, imgDir, 0)
