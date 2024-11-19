import common

fullDevices = ["hydrogen", "ice", "ido_xhdpi",
               "ingres", "ishtar", "jasmine", "jason", "joyeuse", "kate", "kenzo", "lancelot", "land", "latte",
               "laurel_sprout", "laurel", "laurus", "lavender", "lcsh92_wet_jb9", "lcsh92_wet_tdd", "lcsh92_wet_xm_td", "lcsh92",
               "leo", "libra", "light", "lightcm", "lilac", "lime", "lisa", "lithium", "liuqin", "lmi", "lotus", "lte26007",
               "marble", "markw", "matisse", "mayfly", "meri", "merlin", "mido", 
               "mocha", "mojito", "mona", "mondrian", "monet", "moonstone", "munch", "nabu", "natrium",
               "nikel", "nitrogen", "nuwa", "odin", "olive", "olivelite", "olivewood", "omega", "onc", "onclite", "opal", "oxygen", "pearl",
               "perseus", "phoenix", "picasso_48m", "picasso", "pine", "pipa", "pisces", "pissarro", "pissarroin",
               "platina", "plato", "polaris", "pond", "prada", "psyche", "pyxis", "raphael", "raphaels", "redwood",
               "rembrandt", "renoir", "riva", "rock", "rolex", "rosemary_p", "rosemary", "rosy", "rubens", "ruby",
               "sagit", "sakura", "santoni", "sapphire", "sapphiren", "scorpio", "sea", "selene", "shiva", "sirius",
               "sky", "socrates", "spes", "spesn", "star", "sunstone", "surya", "sweet_k6a", "sweet", "taoyao", "tapas", "taurus", "thor",
               "thyme", "tiare", "tiffany", "tissot", "toco", "topaz", "tucana", "tulip", "ugg", "ugglite", "umi", "unicorn", "ursa",
               "vangogh", "vayu", "vela", "venus", "veux", "vida", "vili", "vince", "violet", "virgo_lte_ct", "virgo", "viva", "water",
               "wayne", "whyred", "willow", "wt88047_pro", "wt88047", "wt93007", "wt93807", "wt96007", 
               "xaga", "xun"]

for device in fullDevices:
  devdata = common.loadJson(device)
  android = []
  miui = []
  for branch in devdata['branches']:
    if branch['btag'] == 'X' or branch['btag'] == 'D' or "Enterprise" in branch['en-us'] or "EP" in branch['en-us']:
      i = 0
    else:
      for rom in branch['links']:
        if len(rom['miui'].split("."))>=4:
          dcode = rom['miui'].split(".")[4][1:3]
          if rom['android'] in android:
            i = 0
          else:
            android.append(rom['android'])
          if rom['miui'][:5] in miui:
            i = 0
          else:
            miui.append(rom['miui'][:5])
        else:
          dcode = ""
  android.sort()
  miui.sort()
  string = "机型： "+device+" ， "+dcode+" ，android： "+str(android)+" ，miui： "+str(miui)
  print(string.replace('\'','"'))