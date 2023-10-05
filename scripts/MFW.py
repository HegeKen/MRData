from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import json
from sys import platform
import common


urls = ["https://mifirmware.com/xiaomi-software-update/","https://mifirmware.com/xiaomi-miui-14/","https://mifirmware.com/xiaomi-firmware/","https://mifirmware.com/xiaomi-software-update/","https://mifirmware.com/stable-beta/"]

options = Options()
# options.binary_location = r"C:\Users\Hege\AppData\Local\Microsoft\Edge SxS\Application\118.0.2047.0\msedge.exe"
driver = webdriver.Edge(options=options)
for url in urls:
  driver.get(url)
  soup = BeautifulSoup(driver.page_source, "lxml")
  lists = soup.find_all("a", attrs={"data-content" :"Download"})
  for list in lists:
    link = list.attrs['href']
    if "mifirmware"in link:
      i = 0
    else:
      if ".zip" in link:
        common.checkExit(link.split('/')[4])
      elif ".tgz" in link:
        common.checkExit(link.split('/')[4])
      else:
        common.writeData(link)
