import requests
import json


# https://api.vip.miui.com/api/alpha/detail?&planId=322
headers = {"user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36 Edg/110.0.0.0"}
headers['Referer'] = "https://api.vip.miui.com/"
headers['Cookie'] = "__utmz=230417408.1674223281.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_3c5ef0d4b3098aba138e8ff4e86f1329=1674223281; __utma=230417408.1804466382.1674223281.1677938643.1678271386.5; miui_vip_serviceToken=IA2BKMwRB8IbWsAlqNmMoEZJ0/EGpA2CVh6O66x/QeWCrSQQ3DZPXrGPLJjLicacVQecp4qyQN2JJtT6aXa2SS84tcHWe9RSnRj6j3JvueLNVg1fwSh1UtW0IZsCJYc+i/jYZmE/dy86gpY1k4NuObwRGsyj/P+z9Sg0gcyc0YOAPhV2RP6bvwc0jz6oFnu/oWN+rBexvNOzUgTjyfBxSFQR8irD9P6UDE+pDPJfyS9OtTDX/CHHdNads8GV9bAebP8XQrhhZZcbMD+A5VxhpRx+gYvC2c9cIAmjIsus+J0=; cUserId=9u5KHaCbEsQlJgXDRN6g2WhjGLE; miui_vip_slh=mxbYjqwJvRuGMsuHJZmkVWQUpfU=; miui_vip_ph=botdN5KMs+ZVWCc9Cr2ZlQ=="
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
