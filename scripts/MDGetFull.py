import requests
import json
import time
from bs4 import BeautifulSoup
from sys import platform
import common

# miuimenubutton
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'}
headers = {'Connection': 'close'}
for device in common.currentStable:
  response = requests.get('https://miuidownload.com/miui/'+device+'/', headers=headers)
  content = response.content.decode('utf8')
  soup = BeautifulSoup(content,'lxml')
  branches = soup.find_all('a', attrs={'class' :'miuimenubutton'})
  if len(branches) == 0 :
    i = 0
  else:
    for branch in branches:
      new_url = 'https://miuidownload.com'+branch.attrs['href']+'/'
      print('\r'+new_url+'              ',end='')
      bresp = requests.get(new_url, headers=headers)
      bcon = bresp.content.decode('utf8')
      bsoup = BeautifulSoup(bcon,'lxml')
      lists = bsoup.find_all('a', attrs={'class' :'downloadbutton'})
      if len(lists) == 0 :
        i = 0
      else:
        for list in lists:
          rom_url = list.attrs['href']
        if(rom_url == ''):
           i = 0
        else:
          if 'blockota' in rom_url:
            i = 0
          else:
            packname = rom_url.split('/')[4]
            common.checkExist(packname)
      bresp.close()
  response.close()
