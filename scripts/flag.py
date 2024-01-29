import common
import json
from sys import platform

devices = ["agate", "aristotle", "babylon", "corot", "cupid", "dagu", "daumier", "diting", "duchamp", "earth", "fire", "fuxi",
           "houji", "ingres", "ishtar", "light", "lightcm", "liuqin", "manet", "marble", "matisse", "mayfly", "mondrian", "moonstone",
           "nuwa", "pipa", "plato", "redwood", "rock", "rubens", "ruby", "sea", "shennong", "sky", "socrates", "sunstone", "taoyao",
           "tapas", "thor", "topaz", "unicorn", "vermeer", "xun", "yudi", "yuechu", "yunluo", "zeus", "zizhan"]


def localData(codename):
    if platform == 'win32':
        devdata = json.loads(open('static/data/data/devices/' + codename+'.json', 'r', encoding='utf-8').read())
    else:
        devdata = json.loads(open('/sdcard/Codes/NuxtMR/static/data/data/devices/' + codename+'.json', 'r', encoding='utf-8').read())
    return devdata


for device in devices:
  if device in common.currentStable:
    if int(localData(device)["ismiui"]) > 0:
      print(device+"\t"+localData(device)["ismiui"])
    else:
      i = 0
  else:
    i = 0
