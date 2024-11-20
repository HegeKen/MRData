import common

branches = []
for device in common.fullDevices:
  devdata = common.loadJson(device)
  android = []
  miui = []
  for branch in devdata['branches']:
    code = branch['code'].replace(devdata['codename'],"")
    # print(code)
    if branch['btag'] == 'X' or branch['btag'] == 'D' or "Enterprise" in branch['en-us'] or "EP" in branch['en-us']:
      i = 0
    else:
      for rom in branch['links']:
        i = 0
        tag = rom['miui'][-4:]
        if branch['region']  == "tr" and branch['tag'] == "JPXM":
          print(device)
        string = "'code:' '"+code+"', 'tag': '"+tag+"', 'region': '"+branch['region']+"', 'carrier': '"+str(branch['carrier'])+"', 'zone': '"+branch['zone']+"',"
        if string in branches:
          i = 0
        else:
          branches.append(string)

# print(branches)
