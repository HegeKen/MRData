import requests
import json
from sys import platform

base_url = "https://update.miui.com/updates/miota-fullrom.php?d="
carriers = ["","chinatelecom","chinaunicom","chinamobile"]


cnbranches = ["","_factory","_pre","_demo","_ep_yunke","_soter","_mfw","_pre_miui14","_pre_miui15","_dev_soter","_shxc","_stable_soter",
              "_hi25","_by","_qiy","_tianyi","_tq","_xman","_yh","_yfan","_new","_3sat","_beta","_dev",
              "_gajw","_zc360","zq_360","_pre_wechat","_mtk","_nio","_bs","_clb","_gq","_hhxa","_hwl","_justsafed","_mdsw","_ntb",
              "_xiuyixiu","_hi2","_test","_gpp_pre","_gpp","_pre_7475vbl","_pre_dpp","_pre_gpp","_chenfeng","_dameng","_ahjw","_cqjw","_didi","_hbjw","_hnjwxd",
              "_hnxdjw","_jili","_lnjw","_scjw","_sjt","_tianshanjw","_tangshanjw","_wanguo","_whjw","_ydjw","_yunnanjw","_yunke","_camera","_port",
              "_aikesai","_aochuang","_hujing","_kplus","_ldrh","_liuniu","_lsjw","_qsh","_tl","_tly","_tongzhou","_tongzhuo","_wd",
              "_stable_cmcc","_stable_cmcc01","_stable_ct","_ep_stdee","_ep_xy","_ep_kywl","_ep_cqrcb","_ep_ec","_ep_sxht","_ep_yfan","_ep_yx",
              "_ep_stdce","_ep_xdja","_ep_litee","_ep_yy","_ep_by","_ep_tq","_ep_ui","_ep_wosq","_ep_xzm","_ep_dhao","_ep_qiy",
              "_ep_tly","_ep_tlkj","_ep_zc","_ep_zdjt","_ep_zzyglkg","_ep_zyyglkg","_ep_zzybp","_ep_sdlybjcg","_ep_justsafe",
              "_ep_justsafed","_ep_nio","_ep_txzx","_ep_dameng","_ep_yxyun","_ep_hujing","_ep_jwm","_ep_daote","_ep_jd","_ep_tpkj",
              "_ep_tjzf","_ep_tpybx","_ep_bds","_ep_hfw","_ep_hn","_ep_jyrj","_ep_xysw","_guazi","_cf","_gaotu","_gz","_hkdw","_huaxun",
              "_jds","_jlxf","_wanglong","_wlnd","_yhai","_yuxun","_zkcd","_cm","_ct","_beike","_yf","_yskj","_zyb","_ep_rb","_dxo",
              "_yaohui","_bcwl","_czht","_txzx","_ep_daotetest","_jkpd_factory","_miui13_pre","_test_pre","_hmh","_rrc","_zy",
              "_ep_sdlyjcb","_pre_ep_stdee","_haozu","_szkx","_xmzy","_yhhl","_huatian","_mcaas","_qkzq","_qzxx","_shzl","_sjyc","_gzdt"
              "_lls","_miui_factory","_shrq","_shrx","_taier","_tmg","wuweilab","_cmcc","_ajy","_dp","_zjzy","_fs","_langtuo","_ep_gy58tc",
              "_ep_jds","_ep_yhai","_zhutai","_bb2021","ep_czht","_ep_mjwxns","_ep_qdyh","_research","_sdlybjcg","_8475_pre","_ep_sbgl",
              "_miui_demo_factory","_bindsim","_ent_ct","_fxtc","_gzxc","_dqgx"]

twbranches = ["_tw_global","_pre_tw_global"]

gfbranches = ["_global","_tw_global","_eea_global","_ru_global","_id_global","_in_global","in_global","_in_fk_global","_kr_global",
              "in_in_global","_tr_global","_jp_global","_mx_global","_lm_global","_th_global","_pe_global","_za_global","_jp_kd_global",
              "_kr_gu_global","_kr_kt_global","_kr_sk_global","_h3g_global","_eea_hg_global","_eea_or_global","_eea_tf_global",
              "_eea_by_global","_eea_vf_global","_mx_tc_global","_mx_at_global","_lm_cr_global","_cl_en_global","_cl_global",
              "_eea_sf_global","_eea_ti_global""_th_as_global","_lm_ms_global","_pe_ms_global","_za_vc_global","_za_mt_global",]
gbbranches = ["_global","_factory","_pre_global","_pre_dpp_global","_dev_soter_global","_dc_global","_test_pre_global","_pre_miui14_global","_pre_miui15_global","_mx_global","_lm_global","_th_global","_pe_global","_za_global","_mx_tc_global","_mx_at_global","_pre_mx_tc_global","_pre_mx_at_global","_lm_cr_global",
              "_cl_en_global","_pre_cl_en_global","_cl_global","_th_as_global","_lm_ms_global","_lm_cr_global","_pre_lm_cr_global","_pe_ms_global","_za_vc_global","_za_mt_global",
              "_it_tim_global","_it_vodafone_global","_mx_telcel_global","_es_vodafone_global","_dck_global","_gpp_pre_global",
              "_gt_tg_global","_gt_global","_gpp_global","_qc_global","_mcaas_global","_cl_wom_global","_cl_movistar_global","_ita_vodafone_global",
              "_tr_turkcell_global","_p70_global","_fr_orange_global","_wlnd_global"]

eeabranches = ["_eea_global","_pre_eea_global","_pre_eea_miui15_global","_h3g_global","_eea_hg_global","_eea_ee_global","_pre_eea_ee_global","_eea_or_global","_eea_tf_global","_eea_by_global","_eea_vf_global","_eea_sf_global","_eea_ti_global"]

rubranches = ["_ru_global","_pre_ru_global"]

inbranches = ["_in_global","_pre_in_global","in_global","_in_fk_global","_in_jo_global","in_in_global"]

idbranches = ["_id_global","_pre_id_global"]

trbranches = ["_tr_global","_pre_tr_global"]

krbranches = ["_kr_global","_kr_gu_global","_kr_kt_global","_kr_sk_global"]

jpbranches = ["_jp_global","_jp_kd_global","_jp_sb_global","_jp_rk_global"]


def getFastboot(url,devdata):
  headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
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
            filename = "public/MRdata/script/2023NewROMs.txt"
          else:
            filename = "/sdcard/Codes/NuxtMR/public/MRdata/script/2023NewROMs.txt"
          file = open(filename, "a", encoding='utf-8')
          file.write(data["filename"]+"\n")
          file.close()
      else:
        i = 0
  else:
    i = 0
  response.close()



devices = ["agate","alioth","angelica","angelicain","angelican","ares","aries","biloba","bomb","cactus","camellia",
           "camellian","cannon","cannong","cas","cattail","cetus","chopin","citrus","clover","courbet","cupid",
           "curtana","curtana_in_rf","dagu","dandelion","dandelion_c3l2","daumier","diting","earth","elish",
           "enuma","evergo","evergreen","excalibur","fire","fleur","fog","frost","fuxi","gauguin","haydn",
           "heat","ice","ingres","ishtar","joyeuse","lancelot","light","lightcm","lilac","lime","lisa","liuqin",
           "lmi","marble","matisse","mayfly","merlin","mojito","mona","mondrian","monet","moonstone","munch","nabu",
           "nuwa","odin","opal","pearl","pipa","pissarro","pissarroin","plato","psyche","redwood","rembrandt",
           "renoir","riva","river","rock","rosemary","rosemary_p","rubens","ruby","sea","selene","shennong","shiva",
           "sky","socrates","spes","spesn","star","sunstone","surya","sweet","sweet_k6a","taoyao","tapas","thor",
           "thyme","toco","topaz","umi","unicorn","ursa","vangogh","vayu","venus","veux","vida","vili","viva","water",
           "xaga","xun","yudi","yuechu","yunluo","zeus","zijin","ziyi","zizhan","draco"]

onedevices=["tissot","jasmine","laurel","tiare","ice","water"]

for device in devices:
  if platform == "win32":
    devdata = json.loads(open("public/MRdata/data/devices/"+device+".json", 'r', encoding='utf-8').read())
  else:
    devdata = json.loads(open("/sdcard/Codes/NuxtMR/public/MRdata/data/devices/"+device+".json", 'r', encoding='utf-8').read())
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
        url = base_url+device+branch+"&b=X&r=cn&n="+carrier
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
