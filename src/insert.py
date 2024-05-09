from pymysql import Connection
import config
import json

devices = [
    "agate", "air", "alioth", "andromeda", "angelica", "angelicain", "angelican", "apollo",
    "aqua", "ares", "aries", "aristotle", "armani", "atom", "babylon", "begonia", "beryllium",
    "biloba", "blue", "bomb", "cactus", "camellia", "cancro_lte_ct", "cancro", "cannon",
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
    "mocha", "mojito", "mona", "mondrian", "monet", "moonstone", "munch", "nabu", "natrium",
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
      for branches in devdata["branches"]:
        code = branches["code"]
        branch = branches["branch"]
        tag = branches["btag"]
        bid = len(branches["links"]) + 1
        for rom in branches["links"]:
          bid = bid - 1
          ver = rom["miui"]
          android = rom["android"]
          recovery = rom["recovery"]
          se_sql = "SELECT * FROM roms WHERE code = %s && branch = %s && tag = %s && ver = %s && android = %s"
          cursor.execute(se_sql, (code,branch,tag,ver,android))
          result = cursor.fetchone()
          if result:
            if 'telecom' in rom["fastboot"]:
              ctelecom = rom["fastboot"]
              up_sql = "UPDATE roms SET ctelecom = %s WHERE code = %s && branch = %s && tag = %s && ver = %s && android = %s"
              cursor.execute(up_sql, (ctelecom,code,branch,tag,ver,android))
            elif 'unicom' in rom["fastboot"]:
              cunicom = rom["fastboot"]
              up_sql = "UPDATE roms SET cunicom = %s WHERE code = %s && branch = %s && tag = %s && ver = %s && android = %s"
              cursor.execute(up_sql, (cunicom,code,branch,tag,ver,android))
            elif 'mobile' in rom["fastboot"]:
              cmobile = rom["fastboot"]
              up_sql = "UPDATE roms SET cmobile = %s WHERE code = %s && branch = %s && tag = %s && ver = %s && android = %s"
              cursor.execute(up_sql, (cmobile,code,branch,tag,ver,android))
            else:
              fastboot = rom["fastboot"]
              up_sql = "UPDATE roms SET fastboot = %s WHERE code = %s && branch = %s && tag = %s && ver = %s && android = %s"
              cursor.execute(up_sql, (fastboot,code,branch,tag,ver,android))
          else:
            ins_sql = "INSERT INTO roms (code,branch,tag,ver,bid,android,recovery) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(ins_sql, (code,branch,tag,ver,bid,android,recovery))
            if 'telecom' in rom["fastboot"]:
              ctelecom = rom["fastboot"]
              up_sql = "UPDATE roms SET ctelecom = %s WHERE code = %s && branch = %s && tag = %s && ver = %s && android = %s"
              cursor.execute(up_sql, (ctelecom,code,branch,tag,ver,android))
            elif 'unicom' in rom["fastboot"]:
              cunicom = rom["fastboot"]
              up_sql = "UPDATE roms SET cunicom = %s WHERE code = %s && branch = %s && tag = %s && ver = %s && android = %s"
              cursor.execute(up_sql, (cunicom,code,branch,tag,ver,android))
            elif 'mobile' in rom["fastboot"]:
              cmobile = rom["fastboot"]
              up_sql = "UPDATE roms SET cmobile = %s WHERE code = %s && branch = %s && tag = %s && ver = %s && android = %s"
              cursor.execute(up_sql, (cmobile,code,branch,tag,ver,android))
            else:
              fastboot = rom["fastboot"]
              up_sql = "UPDATE roms SET fastboot = %s WHERE code = %s && branch = %s && tag = %s && ver = %s && android = %s"
              cursor.execute(up_sql, (fastboot,code,branch,tag,ver,android))

except Exception as e:
    print(e)
finally:
    if cnx:
      cnx.close()
