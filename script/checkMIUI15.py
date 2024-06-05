import requests
import json
from sys import platform

devices = ["sky","pearl","corot","marble","yuechu","sea","fire","babylon","sweet_k6a","ishtar","pipa","liuqin","marble","water","tapas","topaz","umi","cmi","monet","vangogh","cas","thyme",
           "venus","courbet","star","renoir","agate","vili","lisa","pissarroin","cupid","zeus","psyche","daumier","mayfly",
           "unicorn","thor","taoyao","plato","fuxi","nuwa","toco","cetus","odin","zizhan","nabu","elish","enuma","dagu","mona",
           "zijin","ziyi","merlin","lancelot","dandelion","angelica","angelican","cattail","selene","dandelion_c3l2","fog","atom",
           "bomb","rock","earth","biloba","lime","cannon","gauguin","joyeuse","excalibur","curtana","mojito","curtana_in_rf","sweet",
           "camellia","chopin","rosemary","lilac","evergo","pissarro","spes","spesn","veux","fleur","viva","vida","light","lightcm",
           "opal","xaga","sunstone","ruby","redwood","lmi","cezanne","apollo","alioth","haydn","ares","munch","ingres","rubens",
           "matisse","diting","mondrian","socrates","rembrandt","yunluo","ice","angelicain","frost","citrus","evergreen","rosemary_p",
           "surya","vayu","moonstone"]
carriers = ["","chinatelecom","chinaunicom","chinamobile"]
base_url = "https://update.miui.com/updates/miota-fullrom.php?d="
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
           "Connection": "close"}

def getFastboot(url,devdata):
  response = requests.post(url, headers=headers)
  if (response.status_code == 200):
    content = response.content.decode("utf8")
    if content == "":
      i = 0
    else:
      data = json.loads(content)["LatestFullRom"]
      if len(data)>0:
        if data["filename"] in devdata.__str__():
          i= 0
        else:
          print("发现一条新数据")
          if platform == "win32":
            filename = "public/MRdata/script/2023NewROMs.txt"
          else:
            filename = "/sdcard/Codes/NuxtMR/public/MRdata/script/2023NewROMs.txt"
          file = open(filename, "a", encoding='utf-8')
          file.write(data["filename"]+"\n")
          file.close()
      else:
        i = 0
  else:
    i = 0
  response.close()
for device in devices:
  if platform == "win32":
    devdata = json.loads(open("public/MRdata/data/devices/"+device+".json", 'r', encoding='utf-8').read())
  else:
    devdata = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/data/devices/"+device+".json", 'r', encoding='utf-8').read())
  for carrier in carriers:
    url = base_url+device+"_pre_miui15&b=X&r="+carrier+"&n="
    getFastboot(url,devdata)
    print("\r"+url+"                                   ",end="")
    url = base_url+device+"_pre_miui15&b=F&r="+carrier+"&n="
    getFastboot(url,devdata)
    print("\r"+url+"                                   ",end="")
