"""
retreat.py
从数据库读取 type=MIUI 的 ROM 记录，比对本地 JSON 文件，
验证分支匹配后，不存在则使用 add_rom_to_json 添加。
"""
import sys
import common


# SELECT 列顺序: device, code, android, version, tag, fastboot, ctelecom, cunicom, cmobile, recovery
# checkpoint 列索引 → filetype
CHECKPOINTS = [
    (5, "fastboot"),   # fastboot
    (6, "fastboot"),   # ctelecom
    (7, "fastboot"),   # cunicom
    (8, "fastboot"),   # cmobile
    (9, "recovery"),   # recovery
]


def find_matching_branch(devdata, code, tag):
    """直接用数据库中的 tag 值匹配分支

    匹配条件：branch.code == code 且 branch.branch == tag
    Returns:
        匹配的 branch dict，或 None（未找到匹配分支）
    """
    if devdata is None:
        return None
    for branch in devdata.get("branches", []):
        if branch.get("code") == code and branch.get("tag") == tag:
            return branch
    return None


def rom_exists_in_branch(branch, version, filetype, filename):
    """检查 ROM 版本是否已存在于该分支的 links 中"""
    if branch is None:
        return False
    key = "recovery" if filetype == "recovery" else "fastboot"
    for link in branch.get("links", []):
        if link.get("miui") == version and link.get(key) == filename:
            return True
    return False


def get_miui_roms_from_db():
    """从数据库读取 type 为 MIUI 的所有 ROM 记录"""
    sql = (
        "SELECT device, code, android, version, tag, "
        "fastboot, ctelecom, cunicom, cmobile, recovery "
        "FROM roms WHERE type = 'MIUI'"
    )
    return common.db_job(sql)


def main():
    print("=" * 60)
    print("ROM 同步：数据库(type=MIUI) → 本地 JSON")
    print("=" * 60)

    rows = get_miui_roms_from_db()
    if not rows:
        print("数据库中未找到 type=MIUI 的记录")
        return

    print(f"从数据库读取到 {len(rows)} 条记录")
    print("-" * 60)

    stats = {"checked": 0, "added": 0, "skipped": 0, "no_branch": 0, "failed": 0}
    current_device = None
    devdata = None

    for row in rows:
        device = row[0]
        code = row[1]
        android = str(row[2]) if row[2] is not None else ""
        version = row[3]
        tag = row[4] if row[4] is not None else ""

        # 按设备缓存 JSON，减少重复读取
        if device != current_device:
            current_device = device
            devdata = common.read_json_file(device)
            if devdata is None:
                print(f"[跳过] 无法读取 {device}.json")

        for col_idx, filetype in CHECKPOINTS:
            filename = row[col_idx]
            if not filename:
                continue

            stats["checked"] += 1

            if devdata is None:
                stats["failed"] += 1
                continue

            # 验证所属分支是否匹配
            branch = find_matching_branch(devdata, code, tag)
            if branch is None:
                print(f"[分支不匹配] {device} {code} tag={tag} {version} {filename}")
                stats["no_branch"] += 1
                continue

            # 检查 ROM 是否已存在
            if rom_exists_in_branch(branch, version, filetype, filename):
                stats["skipped"] += 1
                continue

            # 不存在，调用 add_rom_to_json 添加
            try:
                devdata = common.add_rom_to_json(
                    device, code, android, version,
                    filetype, filename, devdata=devdata,
                )
                stats["added"] += 1
            except Exception as e:
                print(f"添加失败: {device} {code} {version} {filetype} {filename}: {e}")
                stats["failed"] += 1

    print("-" * 60)
    print(f"处理统计:")
    print(f"  检查总数: {stats['checked']}")
    print(f"  已存在跳过: {stats['skipped']}")
    print(f"  新增/更新: {stats['added']}")
    print(f"  分支不匹配: {stats['no_branch']}")
    print(f"  失败: {stats['failed']}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断执行")
        sys.exit(1)
