import urllib
from urllib import parse
import base64
from Crypto.Cipher import AES
import json

# dedata = {
#     "a" : "0", # Don't know what this is.
#     "c" : "7.0", # Same as 'c' above, it's the Android version.
#     "b" : "F", # Same as above, 'X' for weekly build.
#     "d" : "mido_global", # The device name, same as above, chiron for Chinese, chiron_global for global.
#     "g" : "00000000000000000000000000000000", # This seems to be the android_id of the device. Maybe encoded somehow.
#     "cts" : "0", # I don't know what this is.
#     "i" : "0000000000000000000000000000000000000000000000000000000000000000", # This seems to be the imei of the device, obviously encoded somehow.
#     "isR" : "0", # I don't know what this is.
#     "f" : "1", # I don't know what this is.
#     "l" : "en_US", # The locale.
#     "n" : "",  # I don't know what this parameter is
#     "sys" : "0", # I don't know what this is.
#     "p" : "msm8953", # The chipset
#     "unlock" : "1",  # 1 means bootloader is unlocked. 0 means locked.
#     "r" : "CN", # I don't know what this is, maybe region of device?
#     "sn" : "0x00000000", # Probably the serial number of the device, maybe encoded somehow.
#     "v" : "MIUI-V9.0.5.0.NCFMIEI", # The version of MIUI installed.
#     "bv" : "9", # I don't know what this is.
#     "id" : "", # I don't' know what this is.
# }

dedata = {
    "b" : "F", # Same as above, 'X' for weekly build.
    "c" : "7.1.2", # Same as 'c' above, it's the Android version.
    "d" : "vince_global", # The device name, same as above, chiron for Chinese, chiron_global for global.
    "f" : "1", # I don't know what this is.
    "id" : "", # This seems to be the imei of the device, obviously encoded somehow.
    "isR" : "0", # I don't know what this is.
    "l" : "fr-FR", # The locale.
    "n" : "",  # I don't know what this parameter is
    "r" : "FR", # I don't know what this is, maybe region of device?
    "sid" : "2", # Probably the serial number of the device, maybe encoded somehow.
    "sn" : "0xc67d1d89", # Probably the serial number of the device, maybe encoded somehow.
    "v" : "V9.5.11.0.NEGMIFA", # The version of MIUI installed.
}

new_txt = urllib.parse.unquote("RMnOGd%2Be0NNG2DwH7PkO1Wsudgf7Ss0CgFCRv5iTrpWO46ODkEI%2FQ9%2B9udjXENxgdcpwRKYiiGJW6Ov39q2eOUZtP%2BhwvQ4daM2Jd0wxBkWSuNYVfRIsZZMJyaPAtxnWP6whLNUi1DE%2F3zm%2BNX947TAAwJ%2BwisR031Am8nJDsHNv%2F22dtzK3XRJNCF9j2zhdriYDs5lIfV2R1CLKN6mlBKZ8%2Br8nROK5oXd1ji%2FW%2BdsY%2BsxSoaMyR221oMQYwg%2Flxw8nUX1ZQqyBd1Qtipr7L9QKPJYnwEnyVZqw3qG6nVI%3D")
dcode = base64.b64decode(new_txt)
password = b'miuiotavalided11' #秘钥，b就是表示为bytes类型
iv = b'0102030405060708' # iv偏移量，bytes类型
text = b'abcdefghijklmnhi' #需要加密的内容，bytes类型
aes = AES.new(password,AES.MODE_CBC,iv) #创建一个aes对象
den_text = aes.decrypt(dcode)
print(den_text)

password = b'miuiotavalided11' #秘钥，b就是表示为bytes类型
iv = b'0102030405060708' # iv偏移量，bytes类型
j = bytes(json.dumps(dedata),encoding="utf-8")
ecode = base64.b64encode(j)
new_txt = urllib.parse.quote(ecode)
aes = AES.new(password,AES.MODE_CBC,iv)
en_text = aes.encrypt(new_txt)
print(en_text)
