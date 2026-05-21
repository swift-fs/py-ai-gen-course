# 第 8 章配套代码：文件 I/O
# 运行方式：python file_io.py

import json
import csv
from pathlib import Path

# ============================
# 1. 基本读写
# ============================
print("=== 基本文件读写 ===")
file_path = Path("test_output.txt")

# 写入
file_path.write_text("第一行\n第二行\n第三行\n", encoding="utf-8")
print(f"写入完成: {file_path}")

# 读取全部
content = file_path.read_text(encoding="utf-8")
print(f"读取全部:\n{content}")

# 逐行读取
print("逐行读取:")
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        print(f"  {line.strip()}")

# 追加
with open(file_path, "a", encoding="utf-8") as f:
    f.write("第四行（追加）\n")
print(f"追加后: {file_path.read_text(encoding='utf-8')}")

# ============================
# 2. pathlib 文件操作
# ============================
print("\n=== pathlib ===")
print(f"文件名: {file_path.name}")
print(f"后缀: {file_path.suffix}")
print(f"是否存在: {file_path.exists()}")
print(f"大小: {file_path.stat().st_size} 字节")

# ============================
# 3. JSON 文件
# ============================
print("\n=== JSON ===")
students = [
    {"name": "小明", "age": 18, "scores": [95, 88]},
    {"name": "小红", "age": 17, "scores": [92, 96]},
]

json_path = Path("test_students.json")
json_path.write_text(
    json.dumps(students, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

loaded = json.loads(json_path.read_text(encoding="utf-8"))
for s in loaded:
    print(f"  {s['name']}: {s['scores']}")

# ============================
# 4. CSV 文件
# ============================
print("\n=== CSV ===")
csv_path = Path("test_grades.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["姓名", "数学", "语文"])
    writer.writerow(["小明", 88, 92])
    writer.writerow(["小红", 95, 85])

with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['姓名']}: 数学{row['数学']}, 语文{row['语文']}")

# ============================
# 5. 清理测试文件
# ============================
file_path.unlink(missing_ok=True)
json_path.unlink(missing_ok=True)
csv_path.unlink(missing_ok=True)
print("\n测试文件已清理")
