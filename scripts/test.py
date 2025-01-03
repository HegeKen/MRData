import common
import os

branches = []
for device in common.fullDevices:
  devdata = common.loadJson(device)
  android = []
  miui = devdata['ismiui']
  if miui == '0':
    file_path = 'D:/Projects/HyperOS.fans/Web/public/data/devices/'+device+'.json'
    if os.path.exists(file_path):
      i = 0
    else:
      print(device,"MIUI标识错误，请核实,文件位置： ",'D:/Projects/HyperOS.fans/Nuxt3MR/public/MRData/data/devices/'+device+'.json')
  else:
    i = 0
#   for branch in devdata['branches']:
#     code = branch['code'].replace(devdata['codename'],"")
#     if 
#     # print(code)
# #     if branch['btag'] == 'X' or branch['btag'] == 'D' or "Enterprise" in branch['en-us'] or "EP" in branch['en-us']:
# #       i = 0
# #     else:
# #       for rom in branch['links']:
# #         i = 0
# #         tag = rom['miui'][-4:]
# #         if branch['region']  == "tr" and branch['tag'] == "JPXM":
# #           print(device)
# #         string = "'code:' '"+code+"', 'tag': '"+tag+"', 'region': '"+branch['region']+"', 'carrier': '"+str(branch['carrier'])+"', 'zone': '"+branch['zone']+"',"
# #         if string in branches:
# #           i = 0
# #         else:
# #           branches.append(string)

# # # print(branches)
