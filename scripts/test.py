import common
import os

roms = []

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'NewROMs.txt'), 'r') as f:
    new = [line.strip() for line in f if line.strip()]

for rom in new:
  result = common.getData(rom)
  if result == 0:  # 检查是否返回了0
    print(f"Error processing ROM {rom}: common.getData returned invalid value")
    continue  # 跳过此次循环
  else:
    device, code, android, version, type, bigver, region,tag,zone, branch, filetype, filename = result
    common.checkDatabase(device, code, android, version, type, bigver, region,tag,zone,branch, filetype, filename)
    common.add_rom_to_json(device, code, android, version, filetype, filename, devdata=None)
    common.checkExist(rom)