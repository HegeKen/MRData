import requests
import common
import json
from sys import platform

miui_key = b'miuiotavalided11'
miui_iv = b'0102030405060708'
check_url = 'https://update.miui.com/updates/miotaV3.php'


device = 'pipa'
common.MiOTAForm2['d'] = device + ''
common.MiOTAForm2['R'] = 'CN'
common.MiOTAForm2['b'] = 'F'
common.MiOTAForm2['pn'] = common.MiOTAForm2['d'].split('_global')[0]
common.MiOTAForm2['c'] = '13'
common.MiOTAForm2['sdk'] = common.sdk[common.MiOTAForm2['c']]
common.MiOTAForm2['pn'] = device + ''
common.MiOTAForm2['options']['zone'] = '1'
common.MiOTAForm2['options']['previewPlan'] = '0'
common.MiOTAForm2['v'] = 'MIUI-'+'V14.0.10.0.TMZCNXM'


common.getFromApi(common.miui_encrypt(json.dumps(common.MiOTAForm2)),device)
