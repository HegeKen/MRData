import json
import os
from typing import Dict, List

def update_devices_with_android_miui():
	"""
	读取 devlist.json 并根据 code 字段匹配 devices/ 目录下的 JSON 文件，
	将匹配到的设备文件中的 android 和 miui 字段添加到 devlist.json 中的设备对象
	"""
	
	# 读取 devlist.json 文件
	with open('public/MRData/data/devlist.json', 'r', encoding='utf-8') as f:
		devlist_data = json.load(f)
	
	# 遍历所有品牌
	for brand in devlist_data['brands']:
		print(f"Processing brand: {brand.get('brand', 'Unknown')}")
		
		# 遍历该品牌下的所有系列
		for series in brand.get('series', []):
			# 遍历该系列下的所有设备
			for device in series.get('devices', []):
				code = device.get("code")	# 获取设备的code字段
				if not code:
					continue
				
				# 构造设备文件路径
				device_file_path = f"public/MRData/data/devices/{code}.json"
				
				# 检查设备文件是否存在
				if os.path.exists(device_file_path):
					# 读取设备文件
					with open(device_file_path, 'r', encoding='utf-8') as df:
						device_info = json.load(df)
					
					# 获取android和miui字段
					android_versions = device_info.get("android", [])
					miui_versions = device_info.get("miui", [])
					
					# 添加到devlist.json中的设备对象
					device["android"] = android_versions
					device["miui"] = miui_versions
					
					print(f"	Updated {code} with android: {android_versions}, miui: {miui_versions}")
				else:
					print(f"	Warning: Device file for {code} not found at {device_file_path}")
	
	# 写回 devlist.json 文件，使用优化的格式以提高 Git diff 友好性
	output_data = json.dumps(devlist_data, ensure_ascii=False, indent=2, separators=(',', ': '))
	
	# 检查当前文件内容是否与要写入的内容相同
	current_content = ''
	if os.path.exists('public/MRData/data/devlist.json'):
		with open('public/MRData/data/devlist.json', 'r', encoding='utf-8') as f:
			current_content = f.read()
	
	if current_content != output_data:
		# 如果内容发生变化，则写入新内容
		with open('public/MRData/data/devlist.json', 'w', encoding='utf-8') as f:
			f.write(output_data)
		print("Updated devlist.json successfully!")
	else:
		print("No changes to devlist.json, skipping write.")
		

if __name__ == "__main__":
	update_devices_with_android_miui()