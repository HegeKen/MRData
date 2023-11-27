import requests
import common
import json
from sys import platform

miui_key = b"miuiotavalided11"
miui_iv = b"0102030405060708"
check_url = "https://update.miui.com/updates/miotaV3.php"


device = "sky"
common.MiOTAForm["d"] = device + ""
common.MiOTAForm["R"] = "CN"
common.MiOTAForm["b"] = "F"
common.MiOTAForm["pn"] = common.MiOTAForm["d"].split("_global")[0]
common.MiOTAForm["c"] = "13"
common.MiOTAForm["sdk"] = common.sdk[common.MiOTAForm["c"]]
common.MiOTAForm["p"] = device
common.MiOTAForm["options"]["zone"] = "1"
common.MiOTAForm["options"]["cv"] = "V14.0.8.0.TMWCNXM"
common.MiOTAForm["options"]["previewPlan"] = "1"
common.MiOTAForm["v"] = "V14.0.8.0.TMWCNXM"


common.getChangelog(common.miui_encrypt(json.dumps(common.MiOTAForm)),device)
