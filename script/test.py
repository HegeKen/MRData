import urllib
import requests
from urllib import parse
import base64
from Crypto.Cipher import AES
import json
from Crypto.Util.Padding import pad

dedata = {
    "a":"0",
  "b":"F",
  "c":"11",
  "unlock":"0",
  "d":"raphael",
  "lockZoneChannel":"",
  "f":"2",
  "g":"a3e178346e97182fa11631a197801c4d",
  "channel":"",
  "i":"4178f5336815cc2a4641611c1619834817ab14bd0b4c7396a55be2f172c95a56",
  "i2":"b92243889a47bc62dc8b5fb4f50ce60c373553e4221d3ebc4b3bd9791ccaa0a7",
  "isR":"0",
  "l":"zh_CN",
  "sys":"0",
  "n":"",
  "p":"raphael",
  "r":"CN",
  "bv":"140",
  "v":"v12.5.5.0.RFKCNXM",
  "id":"2303711789",
  "sn":"0x77309938",
  "sdk":"30",
  "pn":"raphael",
  "options":{"zone":1,"hashId":"2371ef99a72a282c","ab":"1","previewPlan":"0","sv":3,"av":"8.1.6","cv":""}
}



miui_key = b'miuiotavalided11'
miui_iv = b'0102030405060708'
check_url = "https://update.miui.com/updates/miotaV3.php"

def decipher(en_resp):
  aes = AES.new(b'bWl1aW90YXZhbGlkZWQxMQ==',AES.MODE_CBC,miui_iv)
  resp = aes.decrypt(base64.b64decode(urllib.parse.unquote(en_resp)))
  print(resp)

def encipher(jdata):
  aes = AES.new(miui_key,AES.MODE_CBC,miui_iv)
  postdata = urllib.parse.quote(base64.b64encode(aes.encrypt(pad(bytes(jdata,encoding="utf-8"), AES.block_size))))
  headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58",
           "Referer": "https://update.miui.com/updates/miotaV3.php",
           "Connection": "close",
           "Cookie":"serviceToken=%2B5iaXSr%2BmOVGJeYvnm%2BLRbireHZXGyDmZbqq0f%2BbY0AHqDGQ2ZLutkS2Gu2ptm62sKrIEMCS%2FkulQbBAIe18A2ekUd%2BWXtEEx%2Bg7HXRPj7y%2FzbROzxK05t68nxdOcFLat2TTIVF6cFpo%2Bz0LZmG9mOn6nZBjWXjdockMmFMPKd7%2F9Yqm%2FFbnzE6thnolonkEtM4H8%2F3eyk6xlooeIktte5aoSzcIW%2BZu1poNVCIKFTp%2FAglt2Mp97CM1GcFCBXVXF2lqo7dY%2BymYY4UFD%2BKNEv5ECbX9aHuNQJ4Y6ILOOVnYyN8MBbVhs%2FPgJth3QHg%2FbcxkQN7hBK2mzpk1y%2BGjjw%3D%3D;uid=ZmUADmzPdNUgFptbfp57dA%3D%3D;s=1;"}
  r = requests.post(check_url, data=postdata, headers=headers)
  # print(r.headers)
# decipher("fKsXkyNB/WrbSw4e0Gnk1l9/Y0ekWJjpCEEg1Rve1Ttrc6pWHxNQASzLRUf+5aDRHk69NONgaJjDzkwvmSSzm5brvJcJn4bT1e7HoWeckv7IwN313C1zdLT0MmLC4fFf7IquBoYE7xWD97UmhQbd8PPT9lsrD7k6w4idqr2Y7+HVG13n6D1yd9jwpdyqS9Ve2ms+3npJl0bTf5Tml8Ff8mR0qDslTAIVDUOI/4WCvA07WuboP/EbF9i2W3kxU5Z6AsQlT9OjmDnbYTkHtN4oqFnHikH2Hrdb9eFwmqmKjtNTHokAb3xq6M3hodMIzBQe8U3ei+FQwZhz7sb2ImK9RM05RhBEjHGXF/zGrBH2qmqv/yPAcNqdZ7ddhrt4dpw9fFSOhKJYGcJveP2dQQFilFi5cqpry1aQ8hb18orj5YgWyecUTMRAbHU2QWgWVvu8Qhv2GMHjZj0Xd1a2eTY8qczajJK1LzQAAi/rXQ45aAjnQiT1F1TqnpS6M5bvbnthr/+s53Yob25zUFm262ykTdvTFgBm2N7jFPEmEaPyHYQ435UC3+U89jNOCsk7H6y3bmnbHT3mDop6c3NHZifmsZ3M9A6Ad9UCyfg1zWsCsYt7QyXDOPZB6ZoFM922GdIXdB+ivcyG1tapzOblHAlMPvjeFoDCTxyEUVlJkXL6/oHzZP1OS583uHAOrBpfAoXXjdhVfeLerJl3dLm32aTaSx46DwZ3MdQ7GOF5xrXxBR8rpYJx0kDqaPqKGer/N0MCocLwDJ60v5lvQRU8nf2e1+ceCp60T5upF/56PRGK9FjjUAc8iDAEcLa+tX4J2Sz1WPy33IBX2QkQVx7OQoMgIqWrxNPVkcJxuHd09xrHzK55RCXOemBFUmjft2y+pBIsmvXpLMRIDbMUv0ogBndhtA9ivwgXs7v1UbCyNwnrzVxAiQq5g/zL8Ci45wznHurREOuXPuuDqPvoUx0W3bKPpEXle/0LG0PWisws0roeV+O41vmt8mr639op5EYPVV+adzamPfC61TzIE5LUUFzOLg==")


headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58",
           "Referer": "https://update.miui.com/updates/miotaV3.php",
           "Connection": "close",
           "Cookie":"serviceToken=%2B5iaXSr%2BmOVGJeYvnm%2BLRbireHZXGyDmZbqq0f%2BbY0AHqDGQ2ZLutkS2Gu2ptm62sKrIEMCS%2FkulQbBAIe18A2ekUd%2BWXtEEx%2Bg7HXRPj7y%2FzbROzxK05t68nxdOcFLat2TTIVF6cFpo%2Bz0LZmG9mOn6nZBjWXjdockMmFMPKd7%2F9Yqm%2FFbnzE6thnolonkEtM4H8%2F3eyk6xlooeIktte5aoSzcIW%2BZu1poNVCIKFTp%2FAglt2Mp97CM1GcFCBXVXF2lqo7dY%2BymYY4UFD%2BKNEv5ECbX9aHuNQJ4Y6ILOOVnYyN8MBbVhs%2FPgJth3QHg%2FbcxkQN7hBK2mzpk1y%2BGjjw%3D%3D;uid=ZmUADmzPdNUgFptbfp57dA%3D%3D;s=1;"}
r = requests.post(check_url, data=encipher(json.dumps(dedata)), headers=headers)
print(r.text)

decipher("0KqDAtSNqAl5E2hQ4bnCkpGt6mpGL2oLlXRsuAUB3c7NTPlyNmYiUTZb1mUN5OqMhKb/9e/R5iyHaRaZagtWVmaZWefPOULpIn44j+dQduOhOlcyh098Q1N/b1j5xF2598egEKMoifAZE46TXeIjxTU07AZhLH/6x9uM5/5vEN6H5vl36Rgt4os/JUmwdZE7Ey+d74Hc6VlCSpPid4B0736fPp3XmvhIL/rYMy8fcXz52Y26sj70QSS/zNUyhHMYAIM1ZbV2DD1tX0eDHklNLyCuAKPMtWlrPvhokJiSrqyx9P5yAvYKFtTubJBjTcU3+FxRWhgaY6xt/8YYvroP/rzO2gjQBrd7GZQFl8/cLJD0wOcamWLMZFDQ+kbsBQJRMZVE4c1DFzogkNMCcQE+dcKS/1uAVf97HhkcebLuoimwk/4dNkkHG9Rspmix80N7DZkCjG8Pw0wR8ZyDgqvcf0exsTRD9n+UHjD4Kmk8vhNAQulBcfhoo3keSIFt8mruzs2n8mSRh+/OkmbK5WYaxOksXuom4VTnmcLpkzdlS5eg0z6WxJC82mb9G/2WpOi2wGqLliIA8t93ZagJO686iScRxY/5Vv+NftaNgrgd5ZLDLgYbUs4o63ztJb59HSuCdD6bKt8Qt7GnCMB8tN48XyBMo9S7xxgS0PU2vf6/YtOYckhPlWszZff3hUNdUtJEXVf25Kxk9+5NPs1lW9EnzvvzC+UhxPsvYB1w/aFoM//pUY37AfJSQptScqFuNseHgMJecZo5/RV4Y0ExRZDhZLfoRYgMORsHS3RJewPHdAFbID5moHa2deGVQ5RTw0KPeyDbnWSSUW86QZdR/SFlwOJHmq7NwCN4nN8FXMrxJNyYLpZQuQtC3PAQmVl4LR97wuo8I6D69kj0pflU52eQq6js7zrhkX2wTY1gVAzayRfinVnb5Q4FehAtUSDML1LeCD5+CoJ3YosDqh4dvyvyJXAsWLPxmkIV1Hs8kXDKQLwFLhr02h3wvo0JCe8rgMYWIVlVFHWOiJylzEOTDhNmWAwCMjj/u+jPn3jRtE7r8qyaCB4vDAKipqLBSs7uwno2qMGwcVSMgiP6bCVZC9aUbzkL558QyZvNWCtEnUllZTpkNK2/qGKi30gsboIMtJWTkCI7srCbsyIMhw+/M3krMYZYKxmpJFSoWSgPntDIOpVbGLcXvaYx0yZDPs/V44N5oMu9FQ6pxFia0p/cULqhSImigLuH28MrIUFHogaUzg9evVkCOHJU1zM9E1YflTmsq9uKcSbpi8e20bh4YIfdcqJaHXG7YbBySjmoEGCnKyHevoOjnc21KT7OH7jXmGxTvArSANjSC+z642Q5Y/eCzUk271ouKpzlXt0YhRyOwZkvszEfPIR1mSuct3/M3UqiTyU908uXQm3IKTmjMGJAly2LUK4jTJpnFzH9ZGyRX1Tx1PGsl+J3WpBzKVL90pU8yK78CL6YLl24hLAUudBcSIqid2sc1QXeDBlfZZdmuyiGT9mLjxUsGKuXDpUtDa/klOpPwKuzcAtHwYvxeR9iGEkX9c8+KeOCkmiHdaRiaZ9pX/F5Ar3eQ4J0jFC9l45Opt3f86RWSI9X7oRkD6av7orGG4j89Dtgk8IuDz1CNc0viu2eBcYCNHsShCBJlW+1pyPuj89BFDnncAJ4Yene6+lf5RZ9cN11xwJt5Z6g0n3RhjounPHQ1aSe8GOicV6Iw1eu4ff47x93Ly+TwzLrRfVknEfPaAn/rgbxCvUQmOvUj349PAAuWGgIJYITB6v72O+TMh5/w+4P3l/XBHbpkjMFqFMDpdecvfI+bes7QNqX4G24GPkZfpvlHMqWvASc6TlbkMY5CKNG8+4XJjKOOxkDDlR4zuUP6a0NormrJ/9kaFqZBgVJHYp5rBZ6uyc00ZH4m89BGgJW0zjsLvGiKFl0XWcoowUrk6Kbi7edreaYW4OqHI/smU3amyWDj+NNNwBXvHdPWWdjjqwirV/8odgLVIxbQmL5hRSWDUMn6/N2FlNYZ3Sgy2ftLA8cIAo0jgRHGESVFVl9kSa6HxXSI9+U8ZMd2IWoXYNk3K9aaya45s8XgvdFhaJARRikinLRNB1A0XG/GVuP79GYoLlxKG8XoD5k0Z5UXnK2K3qh2apki3mOQEowhbCYUzpohV6ShzET05YLepiXeKQfP276AQLu7GiZh5901I69z9+G9GRM9grqoOzfGGlmi2WtSp7/aI7p3S6k96zfbaZtkALXgOILIAMbbsUb80D6R7sy2VmMi1J3id6xSmw0kXBP4xDDWurdsNFiqhzUbDs0Fb/pZ7APBJeIq0SJQUWMxwhukk6YK15FgB1mjEh9PmDUElkcPnNapUsHy5HZjcI+plI5KuAHZR716+R0fUFCka4ui4Wr78RcvVpmx5YOY0bvArRgyo8Wn2c/i4Cc5jBx3xYqJXGCKU0LV5001DPrgBP4/RShnLW0fQxs68EJ46Yid0XK8nvA6/OT/nFQLMQMioOYYOEPtGd+VhSLBjuzkOp2vMPlDYooon5iZx92rRdO3pOywZB4jEuzxLlPhxk7HTNydSvl8+gy5ZYg7gQ1t6MdSFJxkqhyUqy2LnxE/dMsqbsK1fjuzzi/Dff2bbCDSHfBBarLVqoLKxg37ClvVleOTbAg1Uk3INiPz5lqAxtBzMUposk9lm1SxAmLzA6BUblGGA7F1v+ZNR8hjclae3mekWa16BYZwqyS6fg7j1DURo2xT2uL8p5R3S7sj1rRtL58bWqnuB5oxGRn/wEeFJbufpwHePpjpMhSSecJA+l0RBQWRxhdi7pAo+DKVCnRyq3qXUx+j+tZ/tSqrSI9Yw/S4dmisAi8PTg4K8sbmh43oy2EOvDeTya+gc4sCglQzVhcEtYAMvT0Pcf6TpHFwESPM0P6wGttNQjC9EWyL0CAH++C39zssw7wzul1kPtq4n1YlYJaaKVo6dlS6Akj1I4msweb17iO/15sI/Dk2WWpU7Wn+A+goLp44QIC5US7CbxPiMgpsUKp5CQszCTXil+zUKOdRRwcfdZ0g0Xo5nwGAxABkfBOurSjwWlLFEki43GnM+NrOBu0KhVkrOM97e3RtF/HL336Wzj/Tw8uvLwOv3KhkFbh8ahqo8XhqERbRagr32hhkSacrMf5RI4l/wjg1jBLZtiHOa20tw/BxPTkhO5pzkLkhgwLR9q43WbmNinxnaIfBfttyKGE8REO5RZDIMP/8ZqfM1Ul/LYpKc0EqTZS5JcpyXQ4I6+SMMx6jxm4FEwCQKkhzyLH4D6S7V20qBZFed47qZW8tViX1mohO6VXWt2OLRqJRGMnInX3A1lMrO86o2NlXxYdEmRY747kCOpac2sRzTRVNmHtGS/RDHpZWlKSPIVJ4jk59p+VIQLizTXIi2TQFp213o53VnVW10L6VWirpvFYqQAfsYhTV4exPRPIULOxff80NXkAGo4NT4ZE2+EgTn9f6VbT70pfbxoKfVIFbnIwcdaRv1WaQ2A7GDGA95RHEgP4V0fiwxM+6sCufB5vbjBq1lbIUS3iDKtrSJjdc3mvRw9o9vKdckDRJxqpnfto5MhPGY2rHb5jrtNDZ3EVtN7mOL1NqyK+Psm42AOr3dHafnTWvwFCtct0Y0NL/OsC2ri0q+wbrlj/POjv0aCB07hzVksoaBEq3yNfwI16u14J7rVhV6batIm9yKhpkqpfweAkcKoag5/fPZu0WsByDWjOKSu1eg8cClz80A+8KPTgH9E14hUU63laGBnjkZfwxxZY1MoaEoTUKLjrA2E5mGJhB+F7inGNCKcfhLpjfUrqLssOKwxtO4uCw3lcdRbzh+wg9z3NdipNvjrshYlj0/7LQFcEgdmMPz8wcryXJrsOqZ0nwtS0eaNxJ0oMutLtxNAy67Sxtz6DC03+BwRWFU1xXu+mOhXUOmsG/Q3fRzlVkPtZRzzlW/wUWavPCci1G5Tc8oSFjQrzbqJ+YtpXbQ3I4nSfJgdCETAl3V4my5ZTRzCRg+TP1NKWyT1qb6LnDE51g8wOf3xuBj2pT8LUAeLFS0cl2NtencSlv5CQfWUgHBV+zWm2WpwUIT7RSxkUeRAelh7Z3fxswNg5gkQlnGVBuUsV624Zw1KeQaQ74hyvkbAmxsTqQpt51kAV6MKUIcxG28vM4N+jtU7WuFp3t+WS+guvRBJRY2nzawUArh2zokyLeR8z7/5smKqH+PTsanXfQN671P+SrI+f3lUmyJ9Wk7VD6px/A+TgLfPsUL3aGbmrrcb1JpzZ1Naw388tgwrlkGCdwXvnHjkAsb7SVTNbNYg8WYhfGdo4ff4BQQvwEynDuOXZhBgNyfOT+Dg21zdC1xeq7UQEAORGjG5EwWgQtfrx8ToIHtlPqdxnFpFedw4ZGbgqJhCadmB19N4+BwLtQjt2axJSS7eXf4VI5L0V0dkmq/H/W3/gDQJ05u64sHnkvs2qNcImhRAY+0UAbhO/dEOTJ9eK3SgWrcdhz68FZVLZFrEVR43NkmRFC/KbQAZYJXAP73u7")
# encipher(json.dumps(dedata))
