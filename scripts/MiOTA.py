import urllib
import requests
import base64
from Crypto.Cipher import AES
import json
from Crypto.Util.Padding import pad



miui_key = b'miuiotavalided11'
miui_iv = b'0102030405060708'
check_url = "https://update.miui.com/updates/miotaV3.php"

checkUpdateget = "zbMQ2f3hwqJ3ayjYdJgQ/sLyiphdAvtZo6QCEYSYMCj+5IWoSWOESplfdJ7xyDlKE0ZAq6HUmVfgoAPQFeuKc+GVH3+AU4ux8w+GRSIrNp5tp0sC6HzHUOP/85CEXERLbzPTXj7JGZxhLT89yLZDfr3hy8DKdAe8USnAaqo08rTuOeh+MVbhXzG3de2AF0jrEil1w8byBXw7uIz+Se70Mdw1hwEK/TZ495rz+LX3WeMhlS0tXAPoXpacH+/wPm6gnWQGYWJS/FVPPCsQc6w1eHMaMyVtGAxKiOSyuwOb0y1kjxY19/nYhVP2G6Q0OgVpychoqS3FnmoN4crbZg+i5DwVKzC1nitKKkclzPGx8t4pqMvgEavsdaj9LycpWYVpDYk0UkbUWy6SvCDob1vaDDC9LCXW/INrhywvmm9wqrziA3xbTS0bh42xMVsOwanupwQj95YddJ62ZlimbsTfwS7hJLkcqQ2A9AzVyGsillbPY+Cb5jawVCV2uKIXR/OWk5DbP1EOurHq8pQEGK4WJQuyohm1Ka1CkEE27gufQNYOY5YmigzqQh33rc5eg/OewYUH8KgxQSuN3uFuSlLPVN+hWSdU4Q1ChZ7T2Nsi/jcQ+zLhUTbD9f5yMv1Cb9W2kz2lTy9bAOH1U7ZvVjJGFosLdp0EybKyjZqJjY+SDiHWqRrXXizzx+m2JpOjCgsCpBxMn3SADeNKg+btZ64+Lg=="
def miui_decrypt(encrypted_response):
  decipher = AES.new(miui_key,AES.MODE_CBC,miui_iv)
  print(encrypted_response)
  decrypted = decipher.decrypt(base64.b64decode(encrypted_response))
  plaintext = decrypted.decode('utf-8').strip()
  pos = plaintext.rfind('}')
  if pos != -1:
    return json.loads(plaintext[:pos + 1])
  else:
    return json.loads(plaintext)

def miui_encrypt(json_request):
  cipher = AES.new(miui_key,AES.MODE_CBC,miui_iv)
  cipher_text = cipher.encrypt(pad(bytes(str(json_request),encoding="ascii"),AES.block_size))
  encrypted_request = urllib.parse.quote(base64.b64encode(cipher_text).decode('utf-8'))
  return encrypted_request

headers = {"user-agent": "Dalvik/2.1.0 (Linux; U; Android 13; MI 9 Build/TKQ1.220829.002)",
           "Connection": "Keep-Alive",
           "Content-Type":"application/x-www-form-urlencoded",
           "Cache-Control":"no-cache",
           "Host":"update.miui.com",
           "Accept-Encoding":"gzip",
           "Content-Length":"795",
           "Cookie":"serviceToken=;"
           }
data = "q=zbMQ2f3hwqJ3ayjYdJgQ%2FsLyiphdAvtZo6QCEYSYMCj%2B5IWoSWOESplfdJ7xyDlKE0ZAq6HUmVfgoAPQFeuKc%2BGVH3%2BAU4ux8w%2BGRSIrNp5tp0sC6HzHUOP%2F85CEXERLbzPTXj7JGZxhLT89yLZDfr3hy8DKdAe8USnAaqo08rTuOeh%2BMVbhXzG3de2AF0jrEil1w8byBXw7uIz%2BSe70Mdw1hwEK%2FTZ495rz%2BLX3WeMhlS0tXAPoXpacH%2B%2FwPm6gnWQGYWJS%2FFVPPCsQc6w1eHMaMyVtGAxKiOSyuwOb0y1kjxY19%2FnYhVP2G6Q0OgVpychoqS3FnmoN4crbZg%2Bi5DwVKzC1nitKKkclzPGx8t4pqMvgEavsdaj9LycpWYVpDYk0UkbUWy6SvCDob1vaDDC9LCXW%2FINrhywvmm9wqrziA3xbTS0bh42xMVsOwanupwQj95YddJ62ZlimbsTfwS7hJLkcqQ2A9AzVyGsillbPY%2BCb5jawVCV2uKIXR%2FOWk5DbP1EOurHq8pQEGK4WJQuyohm1Ka1CkEE27gufQNYOY5YmigzqQh33rc5eg%2FOewYUH8KgxQSuN3uFuSlLPVN%2BhWSdU4Q1ChZ7T2Nsi%2FjcQ%2BzLhUTbD9f5yMv1Cb9W2kz2lTy9bAOH1U7ZvVjJGFosLdp0EybKyjZqJjY%2BSDiHWqRrXXizzx%2Bm2JpOjCgsCpBxMn3SADeNKg%2BbtZ64%2BLg%3D%3D&s=1&t="

devdata = {
    "a": "0",
    "b": "F",
    "c": "13",
    "unlock": "0",
    "d": "marble",
    "lockZoneChannel": "",
    "f": "1",
    "g": "fe16781d9c15788b1c69642d1fdf383f",
    "channel": "",
    "i": "b56c6d74741c00c2d6d1166e0fa701443dd48ec82e8d757934241a70f2348ea1",
    "i2": "5b6fec00263cbeaff1ea1070d6f6ba048ed698eade41bdd95f666d5f3f375214",
    "isR": "0",
    "l": "zh_CN",
    "sys": "0",
    "n": "",
    "p": "marble",
    "r": "CN",
    "bv": "140",
    "v": "MIUI-V14.0.1.0.TNOCNXM",
    "id": "",
    "sn": "0x0f380c2c",
    "sdk": "33",
    "pn": "marble",
    "options": {
      "zone": 1,
      "hashId": "2aa14e25716f1a9e",
      "ab": "0",
      "previewPlan": "1",
      "sv": 0,
      "av": "8.1.7",
      "cv": ""
    }}
data = "q=" + miui_encrypt(devdata) + "&s=1&t=0"
response = requests.post(check_url, headers=headers, data=data)
if "code" in response.text:
  print(json.loads(response.text)["desc"])
else:
  response = miui_decrypt(urllib.parse.unquote(response.text).split("q=")[0])
  if "LatestRom" in response:
    print(response["LatestRom"]["filename"].__str__().split("?")[0])
