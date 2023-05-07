import requests
import json



devices = ["yuechu","babylon","sweet_k6a","ishtar","pipa","liuqin","marble","water","tapas","topaz","umi","cmi","monet","vangogh","cas","thyme",
           "venus","courbet","star","renoir","agate","vili","lisa","pissarroin","cupid","zeus","psyche","daumier","mayfly",
           "unicorn","thor","taoyao","plato","fuxi","nuwa","toco","cetus","odin","zizhan","nabu","elish","enuma","dagu","mona",
           "zijin","ziyi","merlin","lancelot","dandelion","angelica","angelican","cattail","selene","dandelion_c3l2","fog","atom",
           "bomb","rock","earth","biloba","lime","cannon","gauguin","joyeuse","excalibur","curtana","mojito","curtana_rf","sweet",
           "camellia","chopin","rosemary","lilac","evergo","pissarro","spes","spesn","veux","fleur","viva","vida","light","lightcm",
           "opal","xaga","sunstone","ruby","redwood","lmi","cezanne","apollo","alioth","haydn","ares","munch","ingres","rubens",
           "matisse","diting","mondrian","socrates","rembrandt","yunluo","ice","angelicain","frost","citrus","evergreen","rosemary_p",
           "surya","vayu","moonstone"]
devices=["ice"]
base_url = "http://update.miui.com/updates/miota-fullrom.php?d="
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76",
           "Connection": "close"}

for device in devices:
  dataurl = "https://data.miuier.com/data/devices/"+device+".json"
  mrdata = requests.get(dataurl)
  devdata = json.loads(mrdata.text)
  for branch in devdata["branches"]:
    code = branch["code"]
    btag = branch["btag"]
    region = branch["region"]
    carriers = branch["carrier"]
    if len(carriers)==0:
      carrier = ""
      url = base_url+code+"&b="+btag+"&r="+region+"&n="+carrier
      print("\r"+url+"                                   ",end="")
      response = requests.post(url, headers=headers)
      if (response.status_code == 200):
        content = response.content.decode("utf8")
        if content == "":
          i = 0
        else:
          data = json.loads(content)["LatestFullRom"]
          if len(data)>0:
            if data["filename"] in devdata.__str__():
              print(data["filename"])
              i= 0
            else:
              print("发现一条新数据\t"+data["filename"])
              filename = "static/data/script/2023NewROMs.txt"
              file = open(filename, "a", encoding='utf-8')
              file.write(data["filename"]+"\n")
              file.close()
          else:
            i = 0
      else:
        i = 0
      response.close()
    else:
      for carrier in carriers:
        url = base_url+code+"&b="+btag+"&r="+region+"&n="+carrier
        print("\r"+url+"                                   ",end="")
        response = requests.post(url, headers=headers)
        if (response.status_code == 200):
          content = response.content.decode("utf8")
          if content == "":
            i = 0
          else:
            data = json.loads(content)["LatestFullRom"]
            if len(data)>0:
              if data["filename"] in devdata.__str__():
                print(data["filename"])
                i= 0
              else:
                print("发现一条新数据\t"+data["filename"])
                filename = "static/data/script/2023NewROMs.txt"
                file = open(filename, "a", encoding='utf-8')
                file.write(data["filename"]+"\n")
                file.close()
            else:
              i = 0
        else:
          i = 0
        response.close()

