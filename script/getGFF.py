import requests
import json
from sys import platform

base_url = "https://update.miui.com/updates/miota-fullrom.php?d="
carriers = ["","chinatelecom","chinaunicom","chinamobile"]


cnbranches = ["","_demo","_ep_yunke","_ep_stdee","_ep_xy","_ep_kywl","_ep_cqrcb","_ep_ec","_ep_sxht","_ep_yfan","_ep_yx","_ep_stdce",
              "_ep_xdja","_ep_litee","_ep_yy","_ep_tly","_ep_sdlybjcg","_tl","_ep_tl","_ep_tkgwdl"]

twbranches = ["_tw_global"]

gfbranches = ["_global","_tw_global","_eea_global","_ru_global","_id_global","_in_global","in_global","_in_fk_global","_kr_global",
              "in_in_global","_tr_global","_jp_global","_mx_global","_lm_global","_th_global","_pe_global","_za_global","_jp_kd_global",
              "_kr_gu_global","_kr_kt_global","_kr_sk_global","_h3g_global","_eea_hg_global","_eea_or_global","_eea_tf_global",
              "_eea_by_global","_eea_vf_global","_mx_tc_global","_mx_at_global","_lm_cr_global","_cl_en_global","_cl_global",
              "_eea_sf_global","_eea_ti_global""_th_as_global","_lm_ms_global","_pe_ms_global","_za_vc_global","_za_mt_global",]
gbbranches = ["_global","_mx_global","_lm_global","_th_global","_pe_global","_za_global","_mx_tc_global","_mx_at_global","_lm_cr_global",
              "_cl_en_global","_cl_global","_th_as_global","_lm_ms_global","_pe_ms_global","_za_vc_global","_za_mt_global","_gt_tg_global","_gt_global"]

eeabranches = ["_eea_global","_h3g_global","_eea_hg_global","_eea_or_global","_eea_ee_global","_eea_tf_global","_eea_by_global","_eea_vf_global","_eea_sf_global","_eea_ti_global"]

rubranches = ["_ru_global"]

inbranches = ["_in_global","in_global","_in_fk_global","_in_jo_global","in_in_global"]

idbranches = ["_id_global"]

trbranches = ["_tr_global"]

krbranches = ["_kr_global","_kr_gu_global","_kr_kt_global","_kr_sk_global"]

jpbranches = ["_jp_global","_jp_sb_global","_jp_kd_global""_jp_rk_global"]


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



devices = ["garnet","manet","vermeer","aristotle","corot","river","xun","babylon","fire","sky","heat","garnet","houji","shennong","pipa","yudi","yuechu","pearl",
           "ishtar","sweet_k6a","liuqin","marble","water","tapas","topaz","monet","vangogh","thyme",
           "venus","courbet","star","renoir","agate","vili","lisa","pissarroin","cupid","zeus","psyche","daumier","mayfly",
           "unicorn","thor","taoyao","plato","fuxi","nuwa","toco","cetus","odin","zizhan","nabu","elish","enuma","dagu","mona",
           "zijin","ziyi","merlin","lancelot","dandelion","angelica","angelican","cattail","selene","dandelion_c3l2","fog",
           "rock","earth","biloba","lime","cannon","gauguin","joyeuse","excalibur","curtana","mojito","curtana_in_rf","sweet",
           "camellia","chopin","rosemary","lilac","evergo","pissarro","spes","spesn","veux","fleur","viva","vida","light","lightcm",
           "opal","xaga","sunstone","ruby","redwood","apollo","alioth","haydn","ares","munch","ingres","rubens",
           "matisse","diting","mondrian","socrates","rembrandt","yunluo","ice","angelicain","frost","citrus","evergreen","rosemary_p",
           "surya","vayu","moonstone"]

onedevices=["tissot","jasmine","laurel","tiare","ice","water"]

for device in devices:
  if platform == "win32":
    devdata = json.loads(open("static/data/data/devices/"+device+".json", 'r', encoding='utf-8').read())
  else:
    devdata = json.loads(open("/sdcard/Codes/NuxtMR/static/data/data/devices/"+device+".json", 'r', encoding='utf-8').read())
  if device in onedevices:
    for branch in gfbranches:
      url = base_url+device+branch+"&b=F&r=&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
  else:
    for branch in cnbranches:
      for carrier in carriers:
        url = base_url+device+branch+"&b=F&r=cn&n="+carrier
        print("\r"+url+"                                      ",end="")
        getFastboot(url,devdata)
    for branch in gbbranches:
      url = base_url+device+branch+"&b=F&r=global&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
    for branch in eeabranches:
      url = base_url+device+branch+"&b=F&r=eea&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
      url = base_url+device+branch+"&b=F&r=global&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
    for branch in rubranches:
      url = base_url+device+branch+"&b=F&r=ru&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
      url = base_url+device+branch+"&b=F&r=global&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
    for branch in inbranches:
      url = base_url+device+branch+"&b=F&r=in&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
      url = base_url+device+branch+"&b=F&r=global&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
    for branch in idbranches:
      url = base_url+device+branch+"&b=F&r=id&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
      url = base_url+device+branch+"&b=F&r=global&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
    for branch in trbranches:
      url = base_url+device+branch+"&b=F&r=tr&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
      url = base_url+device+branch+"&b=F&r=global&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
    for branch in krbranches:
      url = base_url+device+branch+"&b=F&r=kr&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
      url = base_url+device+branch+"&b=F&r=global&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
    for branch in jpbranches:
      url = base_url+device+branch+"&b=F&r=jp&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
      url = base_url+device+branch+"&b=F&r=global&n="
      print("\r"+url+"                                      ",end="")
      getFastboot(url,devdata)
