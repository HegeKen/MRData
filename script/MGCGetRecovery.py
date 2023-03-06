import json
import requests


headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
domains = ["https://sgp-api.buy.mi.com/bbs/api/","https://ams-api.buy.mi.com/bbs/api/"]
params = "/phone/getdevicelist?phone_id="
regions = ["rs","bd","id","my","pk","ph","tr","vn","th","de","es","fr","it","pl","uk","ru","ua","mie","br","co","mx","pe","cl","ng","eg"]
states = ["eea","global","in","ru","eea","global","in","ru","images"]

def getRec(region):
  ids = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["CurrentIDS"]
  for id in ids:
    for domain in domains:
      url = domain+region+params+id
      print("\r"+url+"      ",end="")
      response = requests.get(url, headers=headers)
      content = response.content.decode("utf8")
      if (response.status_code != 404):
        did = json.loads(content)["data"]["device_data"]["device_list"]
        if did == None:
          i = 0
        else:
          for branch in did:
            rom_url = did[branch]["stable_rom"]["rom_url"]
            packname = rom_url.split('/')[4]
            # flag = rom_url.split('_')[1]
            flag = rom_url.split('/')[3][-6:]
            flags = json.loads(open("static/data/script/crawler.json", 'r', encoding='utf-8').read())["VersionFlags"]
            if flag in flags:
              devdata = json.loads(open("static/data/data/devices/"+flags[flag]+".json", 'r', encoding='utf-8').read()).__str__()
              if packname in devdata:
                i = 0
              else:
                print("发现未收录版本")
                file = open("static/data/script/MGC/MGCGetRec.txt", "a", encoding='utf-8')
                file.write(packname+"\n")
                file.close()
            elif flag in states:
              i = 0
              print(url)
            else:
              print("发现未收录机型以及版本")
              file = open("static/data/script/MGC/MGCFlags.txt", "a", encoding='utf-8')
              file.write(id +"\t"+ flag +"\t"+ packname+"\n")
              file.close()
      else:
        i = 0

getRec("global")

for region in regions:
  getRec(region)
