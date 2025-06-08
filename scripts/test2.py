import common


for device in common.fullDevices:
  data = common.loadJson(device)
  for branch in data["branches"]:
    for i in range(len(branch["links"])-1):
      if branch["links"][i]['miui'] == branch["links"][i+1]['miui']:
        continue
      else:
        if common.compare(branch["links"][i]['miui'], branch["links"][i+1]['miui']) == False:
          if branch["links"][i]['android'] == branch["links"][i+1]['android']:
            if branch["links"][i]['miui'].startswith('K') and branch["links"][i+1]['miui'].startswith('J'):
              continue
            else:
              print(device,branch["links"][i]['miui'],branch["links"][i+1]['miui'])
          else:
            i = 0
        else:
          i = 0