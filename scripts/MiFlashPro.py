import sqlite3
import common


# C:\Users\Hege\AppData\Roaming\Xiaomi\miflash_pro\Config
conn = sqlite3.connect('public/MRdata/scripts/MiFlashPro/download.db3')
c = conn.cursor()
query = '''SELECT dl_rom_name from download_storage'''
cursor = c.execute(query)
for row in cursor:
  common.checkExist(row[0])
