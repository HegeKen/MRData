import common

for device in common.currentStable:
  for branch in common.loadJson(device)["branches"]:
    for rom in branch["links"]:
      if rom["recovery"] == "" :
        if  rom["fastboot"] == "":
          i = 0
        else:
          fb_flag = rom['fastboot'].split('_images')[0]
          if fb_flag in common.flags:
            i = 0
          else:
            common.writeFlag(fb_flag,device)
      else:
        re_flag = rom['recovery'].split('_')[1]
        if re_flag in common.flags:
          i = 0
        else:
          common.writeFlag(re_flag,device)

