import requests
import common
import json
from sys import platform

miui_key = b"miuiotavalided11"
miui_iv = b"0102030405060708"
check_url = "https://update.miui.com/updates/miotaV3.php"


device = "mondrian"
common.MiOTAForm2["d"] = device + ""
common.MiOTAForm2["pn"] = "cn"
common.MiOTAForm2["b"] = "F"
common.MiOTAForm2["c"] = "13"
common.MiOTAForm2["sdk"] = common.sdk[common.MiOTAForm2["c"]]
common.MiOTAForm2["pn"] = device + ""
common.MiOTAForm2["options"]["zone"] = "1"
common.MiOTAForm2["options"]["previewPlan"] = "0"
common.MiOTAForm2["v"] = "V14.0.28.0.TMNCNXM"


common.getChangelog(common.miui_encrypt(json.dumps(common.MiOTAForm2)),device)
