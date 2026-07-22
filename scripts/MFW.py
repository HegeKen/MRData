from selenium import webdriver
import common
from selenium.webdriver.common.by import By
import subprocess
from sys import platform


urls = []
links = ['https://mifirmware.com/xiaomi-software-update/','https://mifirmware.com/xiaomi-miui-14/','https://mifirmware.com/xiaomi-firmware/','https://mifirmware.com/xiaomi-software-update/','https://mifirmware.com/stable-beta/']

options = webdriver.EdgeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Edge(options=options)
for link in links:
  driver.get(link)
  elements = driver.find_elements(By.TAG_NAME,"a")
  for element in elements:
    link = element.get_attribute("href")
    if link is None:
      i = 0
    elif "-firmware" in link:
      urls.append(link)
    elif ".zip" in link or ".tgz" in link:
      common.checkExist(link.split('/')[-1])
    else:
      i = 0
driver.quit()

subprocess.run(["cls"] if platform == "win32" else ["clear"])
for url in urls:
  print('\r'+url + '              ',end='')
  common.MiFirm2(url)