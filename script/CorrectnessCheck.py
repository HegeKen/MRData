import json
from sys import platform

devices = ["aether","agate","alioth","aliothin","amber","andromeda","angelica","angelicain","angelican","apollo","aqua","ares","aresin",
           "aries","aristotle","armani","atom","babylon","begonia","beryllium","bhima","biloba","bomb","cactus","camellia","camellian",
           "cancro_lte_ct","cancro","cannon","cannong","cappu","capricorn","cas","cattail","cepheus","cereus","cetus","cezanne","chiron",
           "chopin","citrus","cloud","clover","cmi","corot","courbet","crux","cupid","curtana_in_rf","curtana","dagu","daisy",
           "dandelion_c3l2","dandelion","daumier","davinci","dior","dipper","diting","draco","earth","elish","enuma","eos",
           "equuleus","evergo","evergreen","excalibur","ferrari","fire","fleur","fog","frost","fuxi","galahad","garnet","gauguin",
           "gauguininpro","gauguinpro","gemini","ginkgo","gram","grus","gucci","haydn","haydnin","heat","helium","hennessy","hermes",
           "HM2013023","HM2014011","HM2014501","houji","hydrogen","ice","ido_xhdpi","ido","ingres","iris","ishtar","jasmine","jason",
           "joyeuse","karna","kate","kenzo","lancelot","land","latte","laurel_sprout","laurel","laurus","lavender","lcsh92_wet_jb9",
           "lcsh92_wet_tdd","lcsh92_wet_xm_td","lcsh92","lemon","leo","libra","light","lightcm","lilac","lime","lisa","lithium","liuqin",
           "lmi","lmipro","lotus","lte26007","maltose","marble","markw","matisse","mayfly","meri","merlin","merlinnfc","mido","miel",
           "mione_plus","mione","mocha","mojito","mona","mondrian","monet","moonstone","munch","nabu","natrium","nikel","nitrogen","nuwa",
           "ocean","odin","olive","olivelite","olivewood","omega","onc","onclite","opal","oxygen","pearl","perseus","peux","phoenix",
           "picasso_48m","picasso","pine","pipa","pisces","pissarro","pissarroin","pissarroinpro","pissarropro","platina","plato","polaris",
           "pomelo","prada","psyche","pyxis","rain","raphael","raphaels","redwood","rembrandt","renoir","riva","river","rock","rolex",
           "rosemary_p","rosemary","rosy","rubens","ruby","rubyplus","rubypro","sagit","sakura","santoni","scorpio","sea","secret","selene",
           "shennong","shiva","sirius","sky","snow","socrates","spes","spesn","star","sunstone","surya","sweet_k6a","sweet","taoyao","tapas",
           "taurus","thor","thunder","thyme","tiare","tiffany","tissot","toco","topaz","tucana","tulip","ugg","ugglite","umi","unicorn",
           "ursa","vangogh","vayu","vela","venus","veux","vida","vili","vince","violet","virgo_lte_ct","virgo","viva","water","wayne",
           "whyred","willow","wind","wt86047_pro","wt86047","wt88047_pro","wt88047","wt93007","wt93807","wt96007","wt98007","xaga",
           "xagain","xagapro","xun","ysl","yudi","yuechu","yunluo","zeus","zijin","ziyi","zizhan"]

for device in devices:
  devdata = json.loads(open("static/data/data/devices/"+device+".json", 'r', encoding='utf-8').read())["branches"]
  for branch in devdata:
    if branch["cnname"] == "开发者预览版" or branch["cnname"] == "原生安卓":
      i = 0
    else:
      for rom in branch["links"]:
        if rom["recovery"] == "":
          if rom["android"] in rom["fastboot"]:
            i = 0
            # print(device + branch["cnname"] +rom["miui"] + "check passed")
          else:
            print(device +"\t"+ branch["cnname"] +"\t"+rom["miui"] +"\t"+ " android version check failed")
          if rom["miui"] in rom["fastboot"]:
            i = 0
            # print(device + branch["cnname"] +rom["miui"] + "check passed")
          else:
            print(device +"\t"+ branch["cnname"] +"\t"+rom["miui"] +"\t"+ " miui version check failed")
        elif rom["android"] in rom["recovery"]:
          i = 0
          # print(device + branch["cnname"] +rom["miui"] + "check passed")
        elif rom["miui"] in rom["recovery"]:
          i = 0
        else:
          print(device +"\t"+ branch["cnname"] +"\t"+rom["miui"] +"\t"+ "check failed")
