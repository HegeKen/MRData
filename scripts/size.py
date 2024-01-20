import requests
import json
import time


def get_file_size(url):
    resp = requests.head(url, allow_redirects=True)
    headers = resp.headers
    if "Content-Length" in headers:
      file_size = int(headers["Content-Length"])/1024/1024/1024
      time.sleep( 2 )
      return round(file_size,3)
    else:
      raise Exception("Can't determine file size.")


UI = ['gold', 'garnet', 'zircon', 'river', 'air', 'gale', 'gust', 'aristotle', 'umi', 'cmi', 'vangogh', 'cas', 'thyme', 'venus', 'star',
      'renoir', 'lisa', 'cupid', 'zeus', 'psyche', 'daumier', 'mayfly', 'unicorn', 'thor', 'taoyao', 'fuxi', 'nuwa', 'ishtar', 'cetus',
      'odin', 'zizhan', 'babylon', 'nabu', 'elish', 'enuma', 'dagu', 'pipa', 'liuqin', 'yudi', 'mona', 'zijin', 'ziyi', 'yuechu', 'earth',
      'camellia', 'chopin', 'rosemary', 'selene', 'evergo', 'pissarro', 'light', 'lightcm', 'xaga', 'sunstone', 'sky', 'ruby', 'redwood',
      'marble', 'pearl', 'alioth', 'haydn', 'ares', 'munch', 'ingres', 'rubens', 'matisse', 'diting', 'mondrian', 'socrates', 'corot',
      'rembrandt', 'yunluo', 'xun']


OS = ["redwood", "yunluo", "sky", "light", "lightcm", "earth", "yuechu", "pipa", "agate", "liuqin",
                 "yudi", "marble", "dagu", "cupid", "zeus", "mayfly", "unicorn", "thor", "corot",
                 "duchamp", "daumier", "vermeer", "manet", "houji", "shennong", "fuxi", "nuwa",
                 "ishtar", "rubens", "matisse", "ingres", "diting", "mondrian", "socrates", "zizhan", "babylon"]
ui_sizes = []
os_sizes = []
for device in UI:
  devdata = json.loads(open('static/data/data/devices/'+device+'.json', 'r', encoding='utf-8').read())
  print('目前正在完成'+devdata['cnname']+'('+devdata['codename']+')')
  for branch in devdata['branches']:
    if branch['branch'] == 'cnmp' or branch['branch'] == 'cnmo' or branch['branch'] == 'cnms':
      for rom in branch['links']:
        if rom['recovery'] =='':
          k = 0
        else:
          url = 'https://cdnorg.d.miui.com/'+rom['miui']+'/'+rom['recovery']
          ui_sizes.append(get_file_size(url))
          print("\r"+str(sum(ui_sizes))+" GB                               ",end="")
        if rom['fastboot'] =='':
          k = 0
        else:
          url = 'https://cdnorg.d.miui.com/'+rom['miui']+'/'+rom['fastboot']
          ui_sizes.append(get_file_size(url))
          print("\r"+str(sum(ui_sizes))+" GB                               ",end="")

print("MIUI 总计大小为:"+str(round(sum(ui_sizes)/1024,3))+" TB")
for device in OS:
  devdata = json.loads(open('D:/Projects/HyperOS.fans/Web/public/data/devices/'+device+'.json', 'r', encoding='utf-8').read())
  for i in range(0,len(devdata['branches'])):
    j = i -1
    for branch in devdata['branches']:
      if branch['idtag'] == 'Dev' or branch['idtag'] == 'CnOO':
        for rom in devdata["branches"][j]["roms"]:
          current = devdata['branches'][j]["roms"][rom]
          if current['recovery'] =='':
            k = 0
          else:
            url = 'https://cdnorg.d.miui.com/'+current['os']+'/'+current['recovery']
            os_sizes.append(get_file_size(url))
            print("\r"+str(sum(os_sizes)+" GB                               "),end="")

          if current['fastboot'] =='':
            k = 0
          else:
            url = 'https://cdnorg.d.miui.com/'+current['os']+'/'+current['fastboot']
            os_sizes.append(get_file_size(url))
            print("\r"+str(sum(os_sizes)+" GB                               "),end="")
print("HyperOS 总计大小为:"+str(round(sum(os_sizes)/1024,3))+" TB")
