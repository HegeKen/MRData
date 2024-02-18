import json
from sys import platform

devices = ["garnet","zircon","gold","sapphiren","sapphire","aurora","manet","vermeer","aristotle","corot","river","xun","babylon","fire","sky","heat","garnet","houji","shennong","pipa","yudi","yuechu","pearl",
           "ishtar","sweet_k6a","liuqin","marble","water","tapas","topaz","monet","vangogh","thyme",
           "venus","courbet","star","renoir","agate","vili","lisa","pissarroin","cupid","zeus","psyche","daumier","mayfly",
           "unicorn","thor","taoyao","plato","fuxi","nuwa","toco","cetus","odin","zizhan","nabu","elish","enuma","dagu","mona",
           "zijin","ziyi","merlin","lancelot","dandelion","angelica","angelican","cattail","selene","dandelion_c3l2","fog",
           "rock","earth","biloba","lime","cannon","gauguin","joyeuse","excalibur","curtana","mojito","curtana_in_rf","sweet",
           "camellia","chopin","rosemary","lilac","evergo","pissarro","spes","spesn","veux","fleur","viva","vida","light","lightcm",
           "opal","xaga","sunstone","ruby","redwood","apollo","alioth","haydn","ares","munch","ingres","rubens",
           "matisse","diting","mondrian","socrates","rembrandt","yunluo","ice","angelicain","frost","citrus","evergreen","rosemary_p",
           "surya","vayu","moonstone"]
for device in devices:
  codename = device
  if platform == "win32":
    devdata = json.loads(open("public/MRdata/data/devices/"+codename+".json", 'r', encoding='utf-8').read())["branches"]
  else:
    devdata = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/data/devices/"+codename+".json", 'r', encoding='utf-8').read())["branches"]
  for branch in devdata:
    for rom in branch["links"]:
      if rom["recovery"] == '':
        i = 0
      else:
        flag = rom["recovery"].split('_')[1]
        print(flag)
        if platform == "win32":
          fine = "public/MRdata/script/Flags.json"
        else:
          fine = "/sdcard/Codes/NuxtMR/public/MRdata/script/Flags.json"
        all_flags = json.loads(open("public/MRdata/script/crawler.json", 'r', encoding='utf-8').read())["RecoveryFlags"].__str__()
        if flag in all_flags:
          i = 0
        else:
          if platform == "win32":
            file = open("public/MRdata/script/Flags.json", "a", encoding='utf-8')
          else:
            file = open("/sdcard/Codes/NuxtMR/public/MRdata/script/Flags.json", "a", encoding='utf-8')
          file.write("\""+flag+"\":\""+codename+"\",\n")
          file.close()

