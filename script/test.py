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

# dedata = {
#     "b" : "F", # Same as above, 'X' for weekly build.
#     "c" : "7.1.2", # Same as 'c' above, it's the Android version.
#     "d" : "vince_global", # The device name, same as above, chiron for Chinese, chiron_global for global.
#     "f" : "1", # I don't know what this is.
#     "id" : "", # This seems to be the imei of the device, obviously encoded somehow.
#     "isR" : "0", # I don't know what this is.
#     "l" : "fr-FR", # The locale.
#     "n" : "",  # I don't know what this parameter is
#     "r" : "FR", # I don't know what this is, maybe region of device?
#     "sid" : "2", # Probably the serial number of the device, maybe encoded somehow.
#     "sn" : "0xc67d1d89", # Probably the serial number of the device, maybe encoded somehow.
#     "v" : "V9.5.11.0.NEGMIFA", # The version of MIUI installed.
# }


miui_key = b'miuiotavalided11'
miui_iv = b'0102030405060708'
check_url = "https://update.miui.com/updates/miotaV3.php"

def decipher(en_resp):
  aes = AES.new(miui_key,AES.MODE_CBC,miui_iv)
  resp = aes.decrypt(base64.b64decode(urllib.parse.unquote(en_resp)))
  print(resp)

def encipher(jdata):
  aes = AES.new(miui_key,AES.MODE_CBC,miui_iv)
  postdata = urllib.parse.quote(base64.b64encode(aes.encrypt(pad(bytes(jdata,encoding="utf-8"), AES.block_size))))
  headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58",
           "Referer": "https://update.miui.com/updates/miotaV3.php",
           "Connection": "close",
           "Cookie":"serviceToken=dPqTWVPUWqtN82LDNULi8UFheo1%2FikWf9ZsouFs6K9yTB%2B6mpEaCgRviU1phJLLB6niJ5kmfywbD9d%2BNJp9V%2F8de%2FDVlhWPt6Esh6inka2zx4cPW%2BafEPlN67Zgrb5pG4M%2B%2BKm0VN83q9yr1nsx5VSw8m6fvNFFfYjR0IMTCwXx5eHD9JLCEw%2BOndXmqKLPOJ4Lmc5xtu76UZ%2FV5mPC9iY%2Fxll0ZYyckcWUrCfER1OrQa3ruH%2FMuHt6SiY7JSE1bYVhyYSAMEp6BUraEE8JG5MIopjlcqopc6BjNqhoB%2B%2BqMK7Q%2FKT9gxeLs9V1RRAGZwwkn7YO46iKlRd%2F6sKpBew%3D%3D;uid=pBXZ5LXVPT%2FOlnXiNTO48g%3D%3D;s=1;"}
  r = requests.post(check_url, data=postdata)
  # print(r.headers)
# decipher("fKsXkyNB/WrbSw4e0Gnk1l9/Y0ekWJjpCEEg1Rve1Ttrc6pWHxNQASzLRUf+5aDRHk69NONgaJjDzkwvmSSzm5brvJcJn4bT1e7HoWeckv7IwN313C1zdLT0MmLC4fFf7IquBoYE7xWD97UmhQbd8PPT9lsrD7k6w4idqr2Y7+HVG13n6D1yd9jwpdyqS9Ve2ms+3npJl0bTf5Tml8Ff8mR0qDslTAIVDUOI/4WCvA07WuboP/EbF9i2W3kxU5Z6AsQlT9OjmDnbYTkHtN4oqFnHikH2Hrdb9eFwmqmKjtNTHokAb3xq6M3hodMIzBQe8U3ei+FQwZhz7sb2ImK9RM05RhBEjHGXF/zGrBH2qmqv/yPAcNqdZ7ddhrt4dpw9fFSOhKJYGcJveP2dQQFilFi5cqpry1aQ8hb18orj5YgWyecUTMRAbHU2QWgWVvu8Qhv2GMHjZj0Xd1a2eTY8qczajJK1LzQAAi/rXQ45aAjnQiT1F1TqnpS6M5bvbnthr/+s53Yob25zUFm262ykTdvTFgBm2N7jFPEmEaPyHYQ435UC3+U89jNOCsk7H6y3bmnbHT3mDop6c3NHZifmsZ3M9A6Ad9UCyfg1zWsCsYt7QyXDOPZB6ZoFM922GdIXdB+ivcyG1tapzOblHAlMPvjeFoDCTxyEUVlJkXL6/oHzZP1OS583uHAOrBpfAoXXjdhVfeLerJl3dLm32aTaSx46DwZ3MdQ7GOF5xrXxBR8rpYJx0kDqaPqKGer/N0MCocLwDJ60v5lvQRU8nf2e1+ceCp60T5upF/56PRGK9FjjUAc8iDAEcLa+tX4J2Sz1WPy33IBX2QkQVx7OQoMgIqWrxNPVkcJxuHd09xrHzK55RCXOemBFUmjft2y+pBIsmvXpLMRIDbMUv0ogBndhtA9ivwgXs7v1UbCyNwnrzVxAiQq5g/zL8Ci45wznHurREOuXPuuDqPvoUx0W3bKPpEXle/0LG0PWisws0roeV+O41vmt8mr639op5EYPVV+adzamPfC61TzIE5LUUFzOLg==")


headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58",
           "Referer": "https://update.miui.com/updates/miotaV3.php",
           "Connection": "close",
           "Cookie":"serviceToken=dPqTWVPUWqtN82LDNULi8UFheo1%2FikWf9ZsouFs6K9yTB%2B6mpEaCgRviU1phJLLB6niJ5kmfywbD9d%2BNJp9V%2F8de%2FDVlhWPt6Esh6inka2zx4cPW%2BafEPlN67Zgrb5pG4M%2B%2BKm0VN83q9yr1nsx5VSw8m6fvNFFfYjR0IMTCwXx5eHD9JLCEw%2BOndXmqKLPOJ4Lmc5xtu76UZ%2FV5mPC9iY%2Fxll0ZYyckcWUrCfER1OrQa3ruH%2FMuHt6SiY7JSE1bYVhyYSAMEp6BUraEE8JG5MIopjlcqopc6BjNqhoB%2B%2BqMK7Q%2FKT9gxeLs9V1RRAGZwwkn7YO46iKlRd%2F6sKpBew%3D%3D;uid=pBXZ5LXVPT%2FOlnXiNTO48g%3D%3D;s=1;"}
r = requests.post(check_url, data="q=d82gJJ5jtvk6N5hmkPFTA9yzH03DF0b4o4BAacuT%2BRe3Zyj6jYQ54uBL49fcISkmjL5mCAinORgG47DrOAQhs1m9ZxNh5wCCpLR%2FiH1sbeyYB9GiS3IGl1wtCzITARvRL%2FiyEvAWYiQ6ClESlcNO6%2FAL4ySpo%2F7HqtFgHSxw%2FAuI3bbsk6OsFvxVaa%2B1L2U0CxGImkLZpZUegJz2QkOoIwdClmZ53loR5tlzHJXnwNim5oVOZkogjAl4lHxJo3QJ2A8OPEKvhLsZ6SlDYzOLgxKsZCKQpKgvG9B4%2BFPazKj%2FzvB4ifJ6gU8Nb9qB2ilFm1g6hECg6wi8ezXOZUQOATwBSh2uJDORmWvB%2FkmcwbJjk%2BflSs%2Bsc40uHS07JpmIK9EKj5ctC7zddWCJJgjrrmmcLjK16QsQKMcdVhy%2FATyt6L6QwoxKsfbo21AG%2Fu0tdpSbh63bbD%2FF8MOOceqW%2FP86W62hRXp7HKXPDBXvpPVJsuMSfFFk0Fo7wdgQ0WsLskos9gKz6FggFAQRyXFQ7atG%2FA8lyvlEtTwdp7HMG%2BBX4laDaixj6IE00Fc7fbqdWcEsQ3rc0%2Bri9EZxKmgKHE0deT1TKrbFFRxOGA%2Fx6q46Yn8pqo05AFd34nQ8kydZzZSQDsXqPeqGO70TuD1FTGtOGunSXOR5JR2Cz2epUh1NaZZdnol%2FcrMo5VVZNZwcmAlC6K8%2FCSkYKQI6Fwvshg%3D%3D&s=2&t=dPqTWVPUWqtN82LDNULi8UFheo1%2FikWf9ZsouFs6K9yTB%2B6mpEaCgRviU1phJLLB6niJ5kmfywbD9d%2BNJp9V%2F8de%2FDVlhWPt6Esh6inka2zx4cPW%2BafEPlN67Zgrb5pG4M%2B%2BKm0VN83q9yr1nsx5VSw8m6fvNFFfYjR0IMTCwXx5eHD9JLCEw%2BOndXmqKLPOJ4Lmc5xtu76UZ%2FV5mPC9iY%2Fxll0ZYyckcWUrCfER1OrQa3ruH%2FMuHt6SiY7JSE1bYVhyYSAMEp6BUraEE8JG5MIopjlcqopc6BjNqhoB%2B%2BqMK7Q%2FKT9gxeLs9V1RRAGZwwkn7YO46iKlRd%2F6sKpBew%3D%3D")
print(r.status_code)
# encipher(json.dumps(dedata))
