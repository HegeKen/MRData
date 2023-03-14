import requests
import json

# 往上走 https://api.vip.miui.com/api/alpha/detail?planId=479
# https://web.vip.miui.com/page/info/mio/mio/testDetails?id=479
# 往下走 https://api.vip.miui.com/api/alpha/detail?planId=135
# https://web.vip.miui.com/page/info/mio/mio/testDetails?id=135
# https://www.xiaomi.cn/board/12180376
# https://new.c.mi.com/global/forum-sub/11888
# https://api-alpha.vip.miui.com/api/alpha/user
headers = {"user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36 Edg/110.0.0.0"}
headers['Referer'] = "https://api.vip.miui.com/"
headers['Cookie'] = ""
list = []
for id in range(0,200):
  url = "https://api.vip.miui.com/api/alpha/detail?&planId="+str(id)
  response = requests.get(url, headers=headers)
  if (response.status_code != 404):
    content = response.content.decode("utf8")
    packages = json.loads(content)
    print(str(id)+"\t"+packages)
  else:
    i = 0
  list.append(id)

print(list)
