from pymysql import Connection
import config
import json

devices = [
    "agate", "air", "alioth", "andromeda", "angelica", "angelicain", "angelican", "apollo",
    "aqua", "ares", "aries", "aristotle", "armani", "atom", "babylon", "begonia", "beryllium",
    "biloba", "blue", "bomb", "cactus", "camellia", "camellian", "cancro_lte_ct", "cancro", "cannon",
    "cappu", "capricorn", "cas", "cattail", "cepheus", "cereus", "cetus", "cezanne", "chiron", "chopin", "citrus", "clover",
    "cmi", "corot", "courbet", "crux", "cupid", "curtana_in_rf", "curtana", "dagu", "daisy", "dandelion_c3l2", "dandelion", "daumier",
    "davinci", "dior", "dipper", "diting", "earth", "elish", "emerald", "enuma", "equuleus", "evergo",
    "evergreen", "excalibur", "ferrari", "fire", "fleur", "fog", "frost", "fuxi", "gale", "garnet", "gauguin",
    "gemini", "ginkgo", "gold", "gram", "grus", "gucci", "haydn",
    "helium", "hennessy", "hermes", "hydrogen", "ice", "ido_xhdpi",
    "ingres", "ishtar", "jasmine", "jason", "joyeuse", "kate", "kenzo", "lancelot", "land", "latte",
    "laurel_sprout", "laurel", "laurus", "lavender", "lcsh92_wet_jb9", "lcsh92_wet_tdd", "lcsh92_wet_xm_td", "lcsh92", 
    "leo", "libra", "light", "lightcm", "lilac", "lime", "lisa", "lithium", "liuqin", "lmi", "lotus", "lte26007",
    "marble", "markw", "matisse", "mayfly", "meri", "merlin", "mido", "mione_plus",
    "mione", "mocha", "mojito", "mona", "mondrian", "monet", "moonstone", "munch", "nabu", "natrium",
    "nikel", "nitrogen", "nuwa", "odin", "olive", "olivelite", "olivewood", "omega", "onc", "onclite", "opal", "oxygen", "pearl",
    "perseus", "phoenix", "picasso_48m", "picasso", "pine", "pipa", "pisces", "pissarro", "pissarroin",
    "platina", "plato", "polaris", "prada", "psyche", "pyxis", "raphael", "raphaels", "redwood",
    "rembrandt", "renoir", "riva","rock", "rolex", "rosemary_p", "rosemary", "rosy", "rubens", "ruby",
    "sagit", "sakura", "santoni", "sapphire", "sapphiren", "scorpio", "sea", "selene", "shiva", "sirius",
    "sky", "socrates", "spes", "spesn", "star", "sunstone", "surya", "sweet_k6a", "sweet", "taoyao", "tapas", "taurus", "thor",
    "thyme", "tiare", "tiffany", "tissot", "toco", "topaz", "tucana", "tulip", "ugg", "ugglite", "umi", "unicorn", "ursa",
    "vangogh", "vayu", "vela", "venus", "veux", "vida", "vili", "vince", "violet", "virgo_lte_ct", "virgo", "viva", "water",
    "wayne", "whyred", "willow", "wt86047_pro", "wt86047", "wt88047_pro", "wt88047", "wt93007", "wt93807", "wt96007", "wt98007",
    "xaga", "xun", "ysl", "yudi", "yuechu", "yunluo", "zeus", "zijin", "zircon", "ziyi", "zizhan"
]
cnx = None
try:
    cnx = Connection(
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port,
        database=config.database,
        autocommit=True
    )
    cursor = cnx.cursor()
    for codename in devices:
      devdata = json.loads(open('public/MRdata/data/devices/' + codename +'.json', 'r', encoding='utf-8').read())
      cnname = devdata["zh-cn"]
      enname = devdata["en-us"]
      for branchs in devdata["branches"]:
        code = branchs["code"]
        branch = branchs["btag"]
        cnbranch = branchs["zh-cn"]
        enbranch = branchs["en-us"]
        region = branchs["region"]
        tag =  branchs["branch"]
        os = 0
        ui = 1
        ep = int(branchs["ep"])
        carrier = str(branchs["carrier"])
        zone = branchs["zone"]
        listed = branchs["show"]
        if branch == "X" or ep == 1:
          if branch == "X":
            mark = ""
          else:
            marks = branchs["links"][0]["miui"].split(".")
            mark = str(marks[len(marks) - 3]) + "." + str(marks[len(marks) - 2]) + "." + str(marks[len(marks) - 1])
        else:
          if branchs["links"][0]["miui"][0] in ['K','J','I']:
            mark = branchs["links"][0]["miui"][:5]
            if mark[:3] != "JLB":
              mark = mark
            elif mark[:3] == "ICS":
              mark = "ICS"
            else:
              mark = "JLB"
          else:
            mark = branchs["links"][0]["miui"][-6:]
          if mark.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
             mark = ""
        cursor = cnx.cursor()
        ins_sql = "INSERT INTO branches (codename,code,branch,tag,cnname,enname,cnbranch,enbranch,region,os,ui,mark,carrier,zone,ep,listed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(ins_sql, (codename,code,branch,tag,cnname,enname,cnbranch,enbranch,region,os,ui,mark,carrier,zone,ep,listed))


except Exception as e:
    print(e)
finally:
    if cnx:
        cnx.close()
