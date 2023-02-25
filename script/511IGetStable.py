import requests
import json
from bs4 import BeautifulSoup
import re
import time

headers = {"user-agent": "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36 Edg/110.0.0.0"}
headers['Referer']= "http://miui.511i.cn/?index=rom_list"
url = "http://miui.511i.cn/?index=rom_list"
full = ["ANGELICAIN", "FROST", "ICE", "BERYLLIUM", "SHIVA", "GRAM", "CITRUS", "EVERGREEN", "ROCK", "ROSEMARYP", "PHOENIXIN", "SURYA", "VAYU",
        "MOONSTONE", "UMI", "MONET", "CMI", "CAS", "VANGOGH", "THYME", "VENUS", "COURBET", "STAR", "RENOIR", "AGATE", "VILI", "LISA",
        "CUPID", "TAOYAO", "ZEUS", "DAUMIER", "MAYFLY", "UNICORN", "THOR", "PLATO", "PSYCHE", "FUXI", "NUWA", "MIONE", "TAURUS", "ARIES",
        "CANCRO", "PISCES", "LIBRA", "FERRARI", "AQUA", "GEMINI", "MERI", "CAPRICORN", "NATRIUM", "TIFFANY", "SAGIT", "WAYNE", "DIPPER",
        "PLATINA", "EQUULEUS", "SIRIUS", "URSA", "CEPHEUS", "CRUX", "GRUS", "TISSOT", "JASMINE", "DAISY", "LAUREL", "PYXIS", "TUCANA",
        "VELA", "LAURUS", "MONA", "ZIJIN", "ZIYI", "OXYGEN", "NITROGEN", "HYDROGEN", "HELIUM", "LITHIUM", "CHIRON", "POLARIS", "PERSEUS",
        "ANDROMEDA", "CETUS", "ZIZHAN", "ODIN", "SCORPIO", "JASON", "VIRGO", "LEO", "TOCO", "LOTUS", "MOCHA", "LATTE", "CAPPU", "CLOVER",
        "NABU", "ENUMA", "ELISH", "DAGU", "SELENE", "DANDELION", "FOG", "MERLIN", "ATOM", "BOMB", "EARTH", "LTE26007", "IDO", "LAND",
        "PRADA", "MARKW", "ROLEX", "SANTONI", "ROSY", "VINCE", "RIVA", "CEREUS", "SAKURA", "CACTUS", "ONCLITE", "PINE", "OLIVE", "OLIVELITE",
        "OLIVEWOOD", "LANCELOT", "CATTAIL", "ANGELICA", "ANGELICAN", "TIARE", "DAVINCI", "DAVINCIIN", "RAPHAEL", "RAPHAELIN",
        "RAPHAELS", "PHOENIX", "PICASSO", "LMI", "CEZANNE", "PICASSO48M", "APOLLO", "ALIOTH", "HAYDN", "ARES", "MUNCH", "RUBENS", "MATISSE",
        "INGRES", "DITING", "MONDRIAN", "SOCRATES", "REMBRANDT", "LCSH92", "MOJITO", "CAMELLIA", "CAMELLIAN", "SWEET", "CHOPIN", "ROSEMARY",
        "LILAC", "HERMES", "KENZO", "HENNESSY", "KATE", "NIKEL", "DIOR", "GUCCI", "MIDO", "WHYRED", "UGGLITE", "UGG", "TULIP", "LAVENDER",
        "VIOLET", "GINKGO", "BILOBA", "BEGONIA", "BEGONIAIN", "WILLOW", "LIME", "CANNON", "GAUGUIN", "EXCALIBUR", "CURTANA", "CANNONG",
        "SPES", "SELENES", "EVERGO", "SPESN", "VIVA", "PISSARRO", "LIGHT", "VEUX", "FLEUR", "XAGA", "SUNSTONE", "RUBY", "REDWOOD", "JOYEUSE",
        "OMEGA", "YSL", "ONC", "YUNLUO", "ARMANI", "WT88047", "WT86047"]
current = ["MONET", "CMI", "CAS", "VANGOGH", "THYME", "VENUS", "STAR", "RENOIR", "COURBET", "AGATE", "VILI", "LISA", "CUPID", "ZEUS", "PSYCHE", "DAUMIER",
           "MAYFLY", "UNICORN", "THOR", "FUXI", "NUWA", "CETUS", "ODIN", "ZIZHAN", "NABU", "ELISH", "ENUMA","DAGU", "MONA", "ZIJIN", "ZIYI", "SELENE", "DANDELION",
           "FOG", "MERLIN", "ATOM", "BOMB", "EARTH", "ANGELICA", "ANGELICAN", "MOJITO", "CAMELLIA", "CAMELLIAN", "SWEET", "CHOPIN", "ROSEMARY","LILAC", "BILOBA",
           "WILLOW", "LIME", "CANNON", "GAUGUIN", "EXCALIBUR", "CURTANA", "CANNONG", "SPES", "SELENES", "EVERGO", "SPESN", "VIVA", "VEUX", "FLEUR", "CHOPIN",
           "PISSARRO", "XAGA", "SUNSTONE", "RUBY", "REDWOOD", "JOYEUSE", "PHOENIX", "PICASSO", "LMI", "CEZANNE", "PICASSO48M", "APOLLO", "ALIOTH", "HAYDN", "ARES",
           "MUNCH", "RUBENS", "MATISSE", "INGRES", "DITING", "MONDRIAN", "SOCRATES", "REMBRANDT", "FROST", "ICE", "SHIVA", "GRAM", "CITRUS", "EVERGREEN", "ROCK",
           "ROSEMARYP", "SURYA", "VAYU","MOONSTONE"]

st = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
for device in current:
    payload = (('dh', device), ('lx', '0'))
    response = requests.post(url, data=payload, headers=headers, timeout=10)
    content = response.content.decode("utf8")
    soup = BeautifulSoup(content, 'lxml')
    lists = soup.find_all("a")
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(t+"\t机型："+device+"\t分支："+'0')
    for list in lists:
      rom_url = list.attrs['href']
      regex = r'miui_.*?.zip'
      matches = re.finditer(regex, rom_url, re.MULTILINE)
      for match in matches:
        if device == "ROSEMARYP":
          device = "ROSEMARY_P"
        elif device == "PHOENIXIN":
          device = "PHOENIX"
        elif device == "MIONE":
          device = "MIONE_PLUS"
        elif device == "IDO":
          device = "IDO_XHDPI"
        elif device == "ANGELICAN":
          device = "ANGELICA"
        elif device == "DAVINCIIN":
          device = "DAVINCI"
        elif device == "RAPHAELIN":
          device = "RAPHAEL"
        elif device == "PICASSO48M":
          device = "PICASSO_48M"
        elif device == "LCSH92":
          device = "LCSH92_WET_JB9"
        elif device == "CAMELLIAN":
          device = "CAMELLIA"
        elif device == "BEGONIAIN":
          device = "BEGONIA"
        elif device == "CANNONG":
          device = "CANNON"
        elif device == "SELENES":
          device = "SELENE"
        else:
          i = 0
        codename = device.lower()
        recovery = match.group()
        android = recovery.split('_')[4].strip(".zip")
        ver = recovery.split('_')[2]
        devicedata = open("static/data/data/devices/" + codename+".json", 'r', encoding='utf-8')
        devdata = json.loads(devicedata.read())
        if recovery in devdata.__str__():
          i = 0
        else:
          devlist = open("static/data/script/crawler.json", 'r', encoding='utf-8')
          all_devices = json.loads(devlist.read())["MDbeta"]
          for all in all_devices:
            code = all["code"]
            if code==device.lower():
              cname = all["NameCn"]
              ename = all["NameEn"]
              datas = {'code':device.lower(),'NameCn':cname,'NameEn':ename,'miui': ver, 'android': android, 'recovery':recovery,'fastboot':""}
              file = open("static/data/script/511ICNGetStable.json","a", encoding='utf-8')
              person_json = json.dumps(datas, ensure_ascii=False)
              file.write(person_json+",")
              file.close()
              print("\r"+recovery+"                              ")
              devicedata.close()
            else:
              i = 0
    response.close
      # time.sleep(2)
et = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(st + "\t" + et)
