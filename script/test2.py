import urllib.parse
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# 解码字符串A
A = "RMnOGd%2Be0NNG2DwH7PkO1Wsudgf7Ss0CgFCRv5iTrpWO46ODkEI%2FQ9%2B9udjXENxgdcpwRKYiiGJW6Ov39q2eOUZtP%2BhwvQ4daM2Jd0wxBkWSuNYVfRIsZZMJyaPAtxnWP6whLNUi1DE%2F3zm%2BNX947TAAwJ%2BwisR031Am8nJDsHNv%2F22dtzK3XRJNCF9j2zhdriYDs5lIfV2R1CLKN6mlBKZ8%2Br8nROK5oXd1ji%2FW%2BdsY%2BsxSoaMyR221oMQYwg%2Flxw8nUX1ZQqyBd1Qtipr7L9QKPJYnwEnyVZqw3qG6nVI%3D"
B = urllib.parse.unquote(A)

# Base64解码内容B
C = base64.b64decode(B)

# AES解码内容C
key = b'miuiotavalided11'
iv = b'0102030405060708'
cipher = AES.new(key, AES.MODE_CBC, iv)
decoded_data = unpad(cipher.decrypt(C), AES.block_size)

# 反加密回字符串A的状态

re_cipher = AES.new(key, AES.MODE_CBC, iv)
reencoded_data = re_cipher.encrypt(b'decoded_data')
reencoded_base64 = base64.b64encode(reencoded_data)
reencoded_B = reencoded_base64.decode()
reencoded_A = urllib.parse.quote(reencoded_B)

print("Original A:", A)
print("Decoded B:", B)
# print("Decoded C:", decoded_data)
# print("Reencoded A:", reencoded_A)
