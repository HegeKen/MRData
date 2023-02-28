import requests
import json
from bs4 import BeautifulSoup
import re
import time

headers = {"user-agent": "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36 Edg/110.0.0.0"}
payload = (('search[value]', ''))
response = requests.post("https://mifirmware.com/wp-admin/admin-ajax.php?action=get_wdtable&table_id=127", data=payload, headers=headers)
content = response.content.decode("utf8")
print(response)
