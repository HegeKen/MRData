import requests
import common
import json
from sys import platform

miui_key = b"miuiotavalided11"
miui_iv = b"0102030405060708"
check_url = "https://update.miui.com/updates/miotaV3.php"


device = "fuxi"
common.MiOTAForm["d"] = device + ""
common.MiOTAForm["R"] = "CN"
common.MiOTAForm["b"] = "F"
common.MiOTAForm["pn"] = common.MiOTAForm["d"].split("_global")[0]
common.MiOTAForm["c"] = "14"
common.MiOTAForm["sdk"] = common.sdk[common.MiOTAForm["c"]]
common.MiOTAForm["p"] = device
common.MiOTAForm["options"]["zone"] = "1"
common.MiOTAForm["options"]["cv"] = "V14.0.5.0.UMCCNXM"
common.MiOTAForm["options"]["previewPlan"] = "1"
common.MiOTAForm["v"] = "V14.0.5.0.UMCCNXM"


common.getChangelog(common.miui_encrypt(json.dumps(common.MiOTAForm)),device)
