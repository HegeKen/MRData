import common

for device in common.currentStable:
  for branch in common.LoadJson(device)["branches"]:
    for link in branch["links"]:
      if link["recovery"] == "":
        if link["fastboot"] == "":
          i = 0
        elif link["miui"] in link or link["android"] in link["fastboot"]:
          i = 0
        else:
          print(f"{branch['branch']} - {link['miui']} - {link['android']} - No for device "+ device)
      elif link["miui"] in link or link["android"] in link["recovery"]:
        i = 0
      else:
        print(f"{branch['branch']} - {link['miui']} - {link['android']} - No for device "+ device)

# import json
# from sys import platform
# import common
# for device in common.currentStable:
#   devdata = json.loads(open('static/data/data/devices/'+device+'.json', 'r', encoding='utf-8').read())['branches']
#   for branch in devdata:
#     if branch['zh-cn'] == '开发者预览版' or branch['zh-cn'] == '原生安卓':
#       i = 0
#     else:
#       for rom in branch['links']:
#         if rom['miui'] == '':
#           print(device +'\t'+ branch['zh-cn'] +'\t'+rom['miui'] +'\t'+ ' MIUI 版本为空')
#         if rom['android'] == '':
#           print(device +'\t'+ branch['zh-cn'] +'\t'+rom['miui'] +'\t'+ ' Android 版本为空')
#         if rom['recovery'] == '':
#           if rom['android'] in rom['fastboot']:
#             i = 0
#             # print(device + branch['zh-cn'] +rom['miui'] + 'check passed')
#           else:
#             print(device +'\t'+ branch['zh-cn'] +'\t'+rom['miui'] +'\t'+ ' android version check failed')
#           if rom['miui'] in rom['fastboot']:
#             i = 0
#             # print(device + branch['zh-cn'] +rom['miui'] + 'check passed')
#           else:
#             print(device +'\t'+ branch['zh-cn'] +'\t'+rom['miui'] +'\t'+ ' miui version check failed')
#         elif rom['android'] in rom['recovery']:
#           i = 0
#           # print(device + branch['zh-cn'] +rom['miui'] + 'check passed')
#         elif rom['miui'] in rom['recovery']:
#           i = 0
#         else:
#           print(device +'\t'+ branch['zh-cn'] +'\t'+rom['miui'] +'\t'+ 'check failed')
