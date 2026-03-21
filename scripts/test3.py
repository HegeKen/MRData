import json
import os
import sys
from typing import Dict, Optional, Any
from datetime import datetime
import common

# -------------------------- 配置项 --------------------------
DATE_FIELD_NAME = "release"        # 新增日期字段的键名

# 数据库配置（建议生产环境使用环境变量）
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",           # 建议：os.environ.get("DB_USER", "user")
    "password": "",   # 建议：os.environ.get("DB_PASS", "password")
    "database": "miroms",
    "charset": "utf8mb4"
}
# -----------------------------------------------------------

# 尝试导入pymysql
try:
    import pymysql
    from pymysql.cursors import DictCursor
except ImportError:
    print("错误：需要安装 PyMySQL")
    print("请运行: pip install pymysql")
    sys.exit(1)


def load_json_file(file_path: str) -> Dict:
    """加载JSON文件并返回解析后的字典"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"未找到文件: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"文件 {file_path} JSON解析错误: {str(e)}")


def save_json_file(file_path: str, data: Dict):
    """
    将修改后的数据覆盖保存到JSON文件
    
    关键修复：
    - 使用 indent="\\t" 保持与原agate.json一致的制表符缩进
    - 使用 ensure_ascii=False 保留中文
    - 自动创建输出目录
    """
    try:
        # 确保输出目录存在
        output_dir = os.path.dirname(file_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            # 关键：使用制表符缩进（\\t）与原文件格式保持一致
            json.dump(data, f, indent="", ensure_ascii=False)
        
        print(f"✓ JSON文件已成功保存到: {file_path}")
        
    except PermissionError:
        raise RuntimeError(f"保存失败：没有权限写入文件 {file_path}")
    except Exception as e:
        raise RuntimeError(f"保存JSON文件失败: {str(e)}")


def get_rom_date_from_db(branch_code: str, miui_version: str) -> Optional[str]:
    """
    从MySQL数据库查询ROM发布日期
    
    安全修复：
    - 使用参数化查询（%s占位符）防止SQL注入 [^19^]
    - 使用上下文管理器确保连接正确关闭
    - 使用DictCursor方便取值
    - 统一日期格式为 YYYY-MM-DD
    """
    conn = None
    try:
        # 建立数据库连接
        conn = pymysql.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            charset=DB_CONFIG["charset"],
            cursorclass=DictCursor  # 使用字典游标
        )
        
        with conn.cursor() as cursor:
            # 安全：使用参数化查询，避免SQL注入 [^23^]
            SQL = "SELECT beta_date FROM roms WHERE code = %s AND version = %s"
            cursor.execute(SQL, (branch_code, miui_version))
            result = cursor.fetchone()
            
            if result and result.get("beta_date"):
                date_val = result["beta_date"]
                
                # 统一转换为 YYYY-MM-DD 格式
                if isinstance(date_val, datetime):
                    return date_val.strftime("%Y-%m-%d")
                elif isinstance(date_val, str):
                    # 尝试解析常见日期格式
                    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%d-%m-%Y"]:
                        try:
                            return datetime.strptime(date_val, fmt).strftime("%Y-%m-%d")
                        except ValueError:
                            continue
                    return date_val  # 无法解析则返回原值
                else:
                    return str(date_val)
            
            return None
            
    except pymysql.Error as e:
        print(f"数据库查询错误 [{branch_code}/{miui_version}]: {e}")
        return None
    except Exception as e:
        print(f"未知错误 [{branch_code}/{miui_version}]: {e}")
        return None
    finally:
        # 确保连接关闭（关键修复）
        if conn:
            try:
                conn.close()
            except:
                pass


def main(JSON_FILE_PATH,OUTPUT_FILE_PATH):
    """主函数：处理ROM数据并保存"""
    print("=" * 60)
    print("MIUI ROM JSON 日期更新工具")
    print("=" * 60)
    
    # 1. 加载JSON
    print(f"\\n[1/4] 加载JSON文件: {JSON_FILE_PATH}")
    try:
        rom_data = load_json_file(JSON_FILE_PATH)
        print(f"      ✓ 加载成功")
    except Exception as e:
        print(f"      ✗ 加载失败: {e}")
        sys.exit(1)
    
    # 统计信息
    branches = rom_data.get("branches", [])
    total_roms = sum(len(b.get("links", [])) for b in branches)
    print(f"      发现 {len(branches)} 个分支，共 {total_roms} 个ROM版本")
    
    # 2. 处理数据
    print(f"\\n[2/4] 查询数据库并更新日期...")
    print(f"      数据库: {DB_CONFIG['database']}@{DB_CONFIG['host']}")
    print("-" * 60)
    
    stats = {"success": 0, "failed": 0, "skipped": 0}
    
    for idx, branch in enumerate(branches, 1):
        branch_code = branch.get("code")
        if not branch_code:
            print(f"[{idx}/{len(branches)}] 警告：跳过无code的分支")
            stats["skipped"] += 1
            continue
        
        links = branch.get("links", [])
        branch_name = branch.get("zh-cn", branch_code)
        
        print(f"[{idx}/{len(branches)}] {branch_code} ({branch_name}): {len(links)} 个版本")
        
        for rom in links:
            miui_version = rom.get("miui")
            if not miui_version:
                stats["skipped"] += 1
                continue
            
            # 查询日期
            rom_date = get_rom_date_from_db(branch_code, miui_version)
            
            # 写入日期字段
            if rom_date:
                rom[DATE_FIELD_NAME] = rom_date
                stats["success"] += 1
            else:
                rom[DATE_FIELD_NAME] = None
                stats["failed"] += 1
    
    # 3. 统计
    print("-" * 60)
    print(f"\\n[3/4] 处理统计:")
    print(f"      成功获取日期: {stats['success']} 个")
    print(f"      未找到日期:   {stats['failed']} 个")
    print(f"      跳过项目:     {stats['skipped']} 个")
    
    # 4. 保存（关键：覆盖保存）
    print(f"\\n[4/4] 保存结果到: {OUTPUT_FILE_PATH}")
    try:
        save_json_file(OUTPUT_FILE_PATH, rom_data)
        print(f"\\n✓ 全部完成！")
    except Exception as e:
        print(f"\\n✗ 保存失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
  for device in ["klein"]:
    JSON_FILE_PATH = f"public/MRData/data/devices/{device}.json"      # 输入JSON文件路径
    OUTPUT_FILE_PATH = f"public/MRData/data/devices/{device}.json"  # 输出文件路径（覆盖保存）
    try:
        main(JSON_FILE_PATH, OUTPUT_FILE_PATH)
    except KeyboardInterrupt:
        print("\\n\\n用户中断执行")
        sys.exit(1)
    except Exception as e:
        print(f"\\n脚本执行失败：{str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)