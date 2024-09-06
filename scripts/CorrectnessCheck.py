import common

for device in common.currentStable:
  for branch in common.loadJson(device)["branches"]:
    for link in branch["links"]:
      if link["miui"] == "":
        print(f"机型： "+device+" ,分支： " + branch['branch'] +""+" ,版本为空，请核查。")
      if link["android"] == "":
        print(f"机型： "+device+" ,分支： " + branch['branch'] +" ,安卓版本为空，请核查。")
      if link["recovery"] == "":
        i = 0
      elif link["android"] not in link["recovery"] or link["miui"] not in link["recovery"]:
        print(f"机型： "+device+" ,分支： " + branch['branch'] +" ,版本 "+ link["miui"]+"，卡刷包与版本号、安卓版本不匹配，请核查。")
      else:
         i = 0
      if link["fastboot"] == "":
        i = 0
      elif link["android"] not in link["fastboot"] or link["miui"] not in link["fastboot"]:
        print(f"机型： "+device+" ,分支： " + branch['branch'] +" ,版本 "+ link["miui"]+"，线刷包与版本号、安卓版本不匹配，请核查。")
      else:
         i = 0