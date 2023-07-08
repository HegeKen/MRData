import urllib
import requests
from urllib import parse
import base64
from Crypto.Cipher import AES
import json
from Crypto.Util.Padding import pad

dedata = {
  "a" : "0", # Don't know what this is.
  "c" : "7.0", # Same as 'c' above, it's the Android version.
  "b" : "F", # Same as above, 'X' for weekly build.
  "d" : "mido_global", # The device name, same as above, chiron for Chinese, chiron_global for global.
  "g" : "00000000000000000000000000000000", # This seems to be the android_id of the device. Maybe encoded somehow.
  "cts" : "0", # I don't know what this is.
  "i" : "0000000000000000000000000000000000000000000000000000000000000000", # This seems to be the imei of the device, obviously encoded somehow.
  "isR" : "0", # I don't know what this is.
  "f" : "1", # I don't know what this is.
  "l" : "en_US", # The locale.
  "n" : "",  # I don't know what this parameter is
  "sys" : "0", # I don't know what this is.
  "p" : "msm8953", # The chipset
  "unlock" : "1",  # 1 means bootloader is unlocked. 0 means locked.
  "r" : "CN", # I don't know what this is, maybe region of device?
  "sn" : "0x00000000", # Probably the serial number of the device, maybe encoded somehow.
  "v" : "MIUI-V9.0.5.0.NCFMIEI", # The version of MIUI installed.
  "bv" : "9", # I don't know what this is.
  "id" : "", # I don't' know what this is.
}

miui_key = b'miuiotavalided11'
miui_iv = b'0102030405060708'
check_url = "https://update.miui.com/updates/miotaV3.php"

def miui_decrypt(encrypted_response):
  decipher = AES.new(miui_key,AES.MODE_CBC,miui_iv)
  decrypted = decipher.decrypt(base64.b64decode(encrypted_response))
  print(decrypted)
  plaintext = decrypted.decode('utf-8').strip()
  pos = plaintext.rfind('}')
  if pos != -1:
    return json.loads(plaintext[:pos + 1])
  else:
    return json.loads(plaintext)

miui_decrypt("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")


def miui_encrypt(json_request):
  cipher = AES.new(miui_key,AES.MODE_CBC,miui_iv)
  cipher_text = cipher.encrypt(pad(bytes(json_request,"ascii"),AES.block_size))
  encrypted_request = base64.b64encode(cipher_text)
  return encrypted_request
