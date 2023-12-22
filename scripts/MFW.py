from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import json
from sys import platform
import common


urls = ['https://mifirmware.com/xiaomi-software-update/','https://mifirmware.com/xiaomi-miui-14/','https://mifirmware.com/xiaomi-firmware/','https://mifirmware.com/xiaomi-software-update/','https://mifirmware.com/stable-beta/']
newurls = []

options = Options()
# options.binary_location = r'C:\Users\Hege\AppData\Local\Microsoft\Edge SxS\Application\118.0.2047.0\msedge.exe'
driver = webdriver.Edge(options=options)
for url in urls:
  driver.get(url)
  soup = BeautifulSoup(driver.page_source, 'lxml')
  a_tags = soup.find_all("a")
  download_links = [a for a in a_tags if a.text == "Download"]
  for link in download_links:
    if "#" in link["href"]:
      i = 0
    elif "firmware" in link["href"]:
      if link["href"] in newurls:
        i = 0
      else:
        newurls.append(link["href"])
    else:
      filename = link["href"].split('/')[4]
      common.checkExit(filename)
for url in newurls:
  common.MiFirm(url)
