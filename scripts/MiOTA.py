import requests
import common
import json
from sys import platform

miui_key = b"miuiotavalided11"
miui_iv = b"0102030405060708"
check_url = "https://update.miui.com/updates/miotaV3.php"




# for device in common.currentStable:
#   if platform == "win32":
#     devdata = json.loads(open("static/data/data/devices/"+device+".json", 'r', encoding='utf-8').read())
#   else:
#     devdata = json.loads(open("/sdcard/Codes/NuxtMR/static/data/data/devices/"+device+".json", 'r', encoding='utf-8').read())
#   for branch in devdata["branches"]:
#     latest = 0
#     common.MiOTAForm["d"] = branch["code"]
#     common.MiOTAForm["p"] = branch["code"]
#     common.MiOTAForm["pn"] = branch["pn"]
#     common.MiOTAForm["b"] = branch["btag"]
#     for link in branch["links"]:
#       common.MiOTAForm["c"] = link["android"].split(".")[0]
#       common.MiOTAForm["v"] = "MIUI-"+ link["miui"]
#       common.MiOTAForm["options"]["cv"] = link["miui"]
#       if latest == link["android"]:
#         i = 0
#       else:
#         data = "q=" + common.miui_encrypt(json.dumps(common.MiOTAForm)) + "&s=1&t="
#         response = requests.post(check_url, headers=headers, data=data)
#         print("\r"+"正在抓取"+devdata["cnname"]+"(" + devdata["codename"]+ ") 的 " + branch["code"]+ "分支，安卓版本为："+link["android"]+"                          ",end="")
#         if "code" in response.text:
#           print(json.loads(response.text)["desc"])
#         else:
#           data = common.miui_decrypt(response.text.split("q=")[0])
#           if "LatestRom" in data:
#             package = data["LatestRom"]["filename"].split("?")[0]
#             common.checkExit(package)
#           elif "CrossRom" in data:
#             package = data["CrossRom"]["filename"].split("?")[0]
#             common.checkExit(package)
#             print(package)
#             i = 0
#           else:
#             print(data)
#             i = 0
#         latest = link["android"]

for device in common.currentStable:
  if platform == "win32":
    devdata = json.loads(open("static/data/data/devices/"+device+".json", 'r', encoding='utf-8').read())
  else:
    devdata = json.loads(open("/sdcard/Codes/NuxtMR/static/data/data/devices/"+device+".json", 'r', encoding='utf-8').read())
  for branch in devdata["branches"]:
    latest = 0
    common.MiOTAForm2["d"] = branch["code"]
    if branch["region"] == "cn":
      common.MiOTAForm2["pn"] = branch["code"]
    else:
      if branch["code"] == devdata["codename"]+"_global":
        common.MiOTAForm2["pn"] = branch["code"]
      else:
        common.MiOTAForm2["pn"] = branch["code"].split("_global")[0]
    common.MiOTAForm2["b"] = branch["btag"]
    common.MiOTAForm2["options"]["zone"] = branch["zone"]
    if branch["ep"] == 1:
      latest = 0
    else:
      i = 0
    for link in branch["links"]:
      if latest == link["android"]:
        i = 0
      else:
        if link["android"] == "":
          common.MiOTAForm2["c"] = "14"
        else:
          common.MiOTAForm2["c"] = link["android"].split(".0")[0]
        common.MiOTAForm2["sdk"] = common.sdk[common.MiOTAForm2["c"]]
        common.MiOTAForm2["v"] = "MIUI-"+ link["miui"]
        if common.getFromApi(common.miui_encrypt(json.dumps(common.MiOTAForm2)),device) == 0:
          if platform == "win32":
            file = open("static/data/scripts/checkOTA.txt", "a", encoding='utf-8')
          else:
            file = open("/sdcard/Codes/NuxtMR/static/data/script/checkOTA.txt", "a", encoding='utf-8')
          if branch["branch"] == "cnmp":
            i = 0
          else:
            file.write(devdata["cnname"]+"("+device+"),\t"+branch["code"]+",\t"+branch["cnname"]+",\t"+link["android"]+",\t"+branch["zone"]+"\n")
            file.close()
        else:
          i = 0
        latest = link["android"]
  print("\r"+devdata["cnname"]+"已完成                            ",end="")
