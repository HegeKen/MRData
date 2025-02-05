import common
from datetime import date

# for device in common.fullDevices:
#   devcode = common.stringify(device)
#   devdata = common.loadJson(device)
#   for branch in devdata['branches']:
#     code = common.stringify(branch['code'])
#     type=common.stringify("MIUI")
#     region = common.stringify(branch['region'])
#     btag = common.stringify(branch['btag'])
#     tag = common.stringify(branch['branch'])
#     zone = int(branch['zone'])
#     for rom in reversed(branch['links']):
#       version = common.stringify(rom['miui'])
#       android = common.stringify(rom['android'])
#       recovery = common.stringify(rom['recovery'])
#       fastboot = common.stringify(rom['fastboot'])
#       ins_sql = f"INSERT INTO roms (device,code,type,region,branch,tag,zone,version,android,recovery,fastboot) VALUES (%s, %s, %s, %s, %s, %s, %d, %s, %s, %s, %s)" % (devcode,code,type,region,btag,tag,zone,version,android,recovery,fastboot)
#       common.db_job(ins_sql)

print(common.stringify(date.today().strftime("%Y-%m-%d")))