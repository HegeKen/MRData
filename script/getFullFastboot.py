import requests
import json
from sys import platform

base_url = "http://update.miui.com/updates/miota-fullrom.php?d="
regions = ["cn","tw","global","eea","ru","in","id","jp","tr"]
carriers = ["","chinatelecom","chinaunicom","chinamobile"]
eps = ["","_demo","_ep_yunke","_ep_stdee","_ep_xy","_ep_kywl","_ep_cqrcb","_ep_ec","_ep_sxht","_ep_yfan","_ep_yx","_ep_stdce",
       "_ep_xdja","_ep_litee","_ep_yy","_ep_tly"]
branches = ["F","X"]
gbranches = ["_global","_tw_global","_eea_global","_ru_global","_id_global","_in_global","_in_global","_in_fk_global",
             "in_in_global","_tr_global","_jp_global","_jp_kd_global","_kr_gu_global","_kr_kt_global","_kr_sk_global",
             "_kr_global","_mx_tc_global","_mx_at_global","_lm_cr_global","_mx_global","_lm_global","_cl_en_global",
             "_h3g_global","_eea_hg_global","_th_as_global","_th_global","_lm_ms_global","_pe_ms_global","_za_vc_global",
             "_pe_global","_za_global","_za_mt_global","_eea_or_global","_eea_tf_global","_eea_by_global","_eea_vf_global",
             "_eea_sf_global","_eea_ti_global"]


devices = ["gauguininpro","aliothin","haydnin","amber","pissarroinpro","galahad","lemon","pomelo","eos","thunder","rain","wind",
           "aether","merlinnfc","cannong","gauguinpro","secret","maltose","camellian","iris","miel","peux","pissarropro",
           "xagapro","ocean","rubypro","rubyplus","lmipro","xagain","snow","cloud","aresin","karna","bhima",
           "yuechu","babylon","ishtar","sweet_k6a","pipa","liuqin","marble","water","tapas","topaz","umi","cmi","monet","vangogh","cas","thyme",
           "venus","courbet","star","renoir","agate","vili","lisa","pissarroin","cupid","zeus","psyche","daumier","mayfly",
           "unicorn","thor","taoyao","plato","fuxi","nuwa","toco","cetus","odin","zizhan","nabu","elish","enuma","dagu","mona",
           "zijin","ziyi","merlin","lancelot","dandelion","angelica","angelican","cattail","selene","dandelion_c3l2","fog","atom",
           "bomb","rock","earth","biloba","lime","cannon","gauguin","joyeuse","excalibur","curtana","mojito","curtana_rf","sweet",
           "camellia","chopin","rosemary","lilac","evergo","pissarro","spes","spesn","veux","fleur","viva","vida","light","lightcm",
           "opal","xaga","sunstone","ruby","redwood","lmi","cezanne","apollo","alioth","haydn","ares","munch","ingres","rubens",
           "matisse","diting","mondrian","socrates","rembrandt","yunluo","ice","angelicain","frost","citrus","evergreen","rosemary_p",
           "surya","vayu","moonstone"]

def getFastboot(url,devdata):
  headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76",
             "Connection": "close"}
  response = requests.post(url, headers=headers)
  if (response.status_code == 200):
    content = response.content.decode("utf8")
    if content == "":
      i = 0
    else:
      data = json.loads(content)["LatestFullRom"]
      if len(data)>0:

        if data["filename"] in str(devdata).__str__():
          i= 0
        else:
          print("发现一条新数据")
          if platform == "win32":
            filename = "static/data/script/2023NewROMs.txt"
          else:
            filename = "/sdcard/Codes/NuxtMR/static/data/script/2023NewROMs.txt"
          file = open(filename, "a", encoding='utf-8')
          file.write(data["filename"]+"\n")
          file.close()
      else:
        i = 0
  else:
    i = 0
  response.close()


for device in devices:
  devdata = json.loads(requests.get("https://data.miuier.com/data/devices/"+device+".json").text)
  for region in regions:
    if region =="cn":
      for branch in branches:
        for ep in eps:
          for carrier in carriers:
            url = base_url+device+ep+"&b="+branch+"&r=cn&n="+carrier

            print("\r"+url+"                                      ",end="")
            getFastboot(url,devdata)
    else:
      for branch in gbranches:
        url = base_url+device+branch+"&b=F&r="+region+"&n="
        print("\r"+url+"                                         ",end="")
        getFastboot(url,devdata)
