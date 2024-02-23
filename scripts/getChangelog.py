import common
import json

miui_key = b'miuiotavalided11'
miui_iv = b'0102030405060708'
check_url = 'https://update.miui.com/updates/miotaV3.php'


device = 'xun'
common.MiOTAForm['d'] = device + ''
common.MiOTAForm['R'] = 'CN'
common.MiOTAForm['b'] = 'F'
common.MiOTAForm['pn'] = common.MiOTAForm['d'].split('_global')[0]
common.MiOTAForm['c'] = '13'
common.MiOTAForm['sdk'] = common.sdk[common.MiOTAForm['c']]
common.MiOTAForm['p'] = device
common.MiOTAForm['options']['zone'] = '1'
common.MiOTAForm['options']['cv'] = 'V14.0.9.0.TMUCNXM'
common.MiOTAForm['options']['previewPlan'] = '1'
common.MiOTAForm['v'] = 'V14.0.10.0.TMUCNXM'


encrypted_form = common.miui_encrypt(json.dumps(common.MiOTAForm))
common.getChangelog(encrypted_form, device)
