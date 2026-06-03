# datetime 标准库 —— 日期与时间

> **学习目标**：掌握 `datetime` 模块的核心类（`date`、`time`、`datetime`、`timedelta`），能完成日期时间创建、格式化、解析、计算等常见任务。

---

## 1. 什么是 datetime 模块？

`datetime` 是 Python 标准库中处理日期和时间的模块。它提供了以下几个核心类：

| 类          | 说明                     | 示例                          |
| ----------- | ------------------------ | ----------------------------- |
| `date`      | 日期（年、月、日）       | `2024-06-01`                  |
| `time`      | 时间（时、分、秒、微秒） | `14:30:00`                    |
| `datetime`  | 日期 + 时间              | `2024-06-01 14:30:00`         |
| `timedelta` | 时间间隔/差值            | `3 days, 5:30:00`             |
| `timezone`  | 时区                     | `UTC+8`（北京时间）           |

```python
from datetime import date, time, datetime, timedelta, timezone
```

---

## 2. date —— 日期

### 创建日期

```python
from datetime import date

# 指定年月日创建
birthday = date(2000, 1, 15)
print(birthday)  # 2000-01-15

# 获取今天的日期
today = date.today()
print(f"今天是: {today}")

# 从时间戳创建（时间戳是自 1970-01-01 00:00:00 UTC 以来的秒数）
import time
timestamp = time.time()
d = date.fromtimestamp(timestamp)
print(f"时间戳对应日期: {d}")
```

### 获取日期的各个部分

```python
today = date.today()

print(f"年: {today.year}")       # 2024
print(f"月: {today.month}")      # 6
print(f"日: {today.day}")        # 1
print(f"星期: {today.weekday()}")  # 0=周一, 1=周二, ..., 6=周日
print(f"星期: {today.isoweekday()}")  # 1=周一, ..., 7=周日（ISO 标准）
print(f"ISO 日历: {today.isocalendar()}")  # (年, 周数, 星期几)
```

> **注意**：`weekday()` 返回 0-6（周一=0），`isoweekday()` 返回 1-7（周一=1）。ISO 标准更符合直觉。

### 日期的属性和方法

```python
d = date(2024, 6, 1)

# ISO 格式字符串
print(d.isoformat())    # '2024-06-01'

# 自定义格式
print(d.strftime("%Y年%m月%d日"))  # '2024年06月01日'

# 替换某个部分（返回新的 date 对象）
new_date = d.replace(year=2025)
print(new_date)  # 2025-06-01
```

---

## 3. time —— 时间

### 创建时间

```python
from datetime import time

# 创建时间对象
t1 = time(14, 30)          # 14:30:00
t2 = time(14, 30, 45)      # 14:30:45
t3 = time(14, 30, 45, 123456)  # 14:30:45.123456（含微秒）

print(t1)  # 14:30:00
print(t2)  # 14:30:45
print(t3)  # 14:30:45.123456
```

### 获取时间的各个部分

```python
t = time(14, 30, 45, 123456)

print(f"时: {t.hour}")         # 14
print(f"分: {t.minute}")       # 30
print(f"秒: {t.second}")       # 45
print(f"微秒: {t.microsecond}")  # 123456
```

### 格式化

```python
t = time(14, 30, 45)
print(t.isoformat())             # '14:30:45'
print(t.strftime("%I:%M %p"))    # '02:30 PM'（12 小时制）
```

---

## 4. datetime —— 日期 + 时间

这是最常用的类，包含了日期和时间的信息。

### 创建 datetime

```python
from datetime import datetime, timezone, timedelta

# 获取当前日期时间
now = datetime.now()                    # 本地时间
print(f"现在: {now}")

utc_now = datetime.now(timezone.utc)    # UTC 时间
print(f"UTC: {utc_now}")

# 指定日期时间创建
dt = datetime(2024, 6, 1, 14, 30, 0)
print(f"指定时间: {dt}")  # 2024-06-01 14:30:00

# 从字符串解析
dt = datetime.strptime("2024-06-01 14:30", "%Y-%m-%d %H:%M")
print(f"解析结果: {dt}")

# 从时间戳创建
import time as time_module
dt = datetime.fromtimestamp(time_module.time())
print(f"时间戳对应: {dt}")
```

### 获取 datetime 的各个部分

```python
dt = datetime(2024, 6, 1, 14, 30, 45, 123456)

print(f"年: {dt.year}")          # 2024
print(f"月: {dt.month}")         # 6
print(f"日: {dt.day}")           # 1
print(f"时: {dt.hour}")          # 14
print(f"分: {dt.minute}")        # 30
print(f"秒: {dt.second}")        # 45
print(f"微秒: {dt.microsecond}")  # 123456
```

### datetime 与 date 的转换

```python
dt = datetime(2024, 6, 1, 14, 30, 0)

# 提取日期部分
d = dt.date()
print(f"日期: {d}")      # 2024-06-01

# 提取时间部分
t = dt.time()
print(f"时间: {t}")      # 14:30:00
```

---

## 5. timedelta —— 时间间隔

`timedelta` 表示两个日期或时间之间的**差值**（时间间隔）。

### 创建 timedelta

```python
from datetime import timedelta

# 3 天
delta1 = timedelta(days=3)
print(delta1)  # 3 days, 0:00:00

# 2 小时 30 分钟
delta2 = timedelta(hours=2, minutes=30)
print(delta2)  # 2:30:00

# 1 周
delta3 = timedelta(weeks=1)
print(delta3)  # 7 days, 0:00:00

# 组合
delta4 = timedelta(days=5, hours=3, minutes=30, seconds=15)
print(delta4)  # 5 days, 3:30:15
```

### timedelta 支持的参数

| 参数          | 说明   |
| ------------- | ------ |
| `days`        | 天     |
| `seconds`     | 秒     |
| `microseconds`| 微秒   |
| `milliseconds`| 毫秒   |
| `minutes`     | 分钟   |
| `hours`       | 小时   |
| `weeks`       | 周     |

### 日期时间运算

```python
from datetime import datetime, timedelta

now = datetime(2024, 6, 1, 12, 0, 0)

# 加上时间间隔
tomorrow = now + timedelta(days=1)
print(f"明天: {tomorrow}")

next_week = now + timedelta(weeks=1)
print(f"下周: {next_week}")

# 减去时间间隔
yesterday = now - timedelta(days=1)
print(f"昨天: {yesterday}")

# 两个日期相减得到 timedelta
birthday = datetime(2024, 12, 25)
diff = birthday - now
print(f"距离生日: {diff}")        # 207 days, 12:00:00
print(f"还有 {diff.days} 天")    # 207
```

### timedelta 的属性

```python
delta = timedelta(days=5, hours=3, minutes=30)

print(f"总天数: {delta.days}")            # 5
print(f"总秒数: {delta.total_seconds()}") # 469800.0（5天3小时30分钟）
print(f"仅秒部分: {delta.seconds}")        # 12600（3小时30分钟的秒数，不含天的部分）
```

> **注意**：`delta.seconds` 只是不满一天部分的秒数（0-86399），不是总秒数！要用 `total_seconds()` 获取总秒数。

---

## 6. 格式化与解析

### `strftime()` —— 日期时间 → 字符串

```python
from datetime import datetime

now = datetime.now()

# 常用格式
print(now.strftime("%Y-%m-%d"))           # '2024-06-01'
print(now.strftime("%Y/%m/%d %H:%M"))     # '2024/06/01 14:30'
print(now.strftime("%Y年%m月%d日 %H时%M分"))  # '2024年06月01日 14时30分'
print(now.strftime("%A, %B %d, %Y"))      # 'Saturday, June 01, 2024'
```

### `strptime()` —— 字符串 → 日期时间

```python
from datetime import datetime

# 解析常见格式
dt1 = datetime.strptime("2024-06-01", "%Y-%m-%d")
print(dt1)  # 2024-06-01 00:00:00

dt2 = datetime.strptime("01/06/2024 14:30", "%d/%m/%Y %H:%M")
print(dt2)  # 2024-06-01 14:30:00

dt3 = datetime.strptime("June 1, 2024", "%B %d, %Y")
print(dt3)  # 2024-06-01 00:00:00
```

> **关键**：`strptime` 的格式字符串必须和输入字符串的格式**完全匹配**，否则会报 `ValueError`。

### 格式化代码速查表

| 代码 | 说明                   | 示例                |
| ---- | ---------------------- | ------------------- |
| `%Y` | 四位数年份             | `2024`              |
| `%y` | 两位数年份             | `24`                |
| `%m` | 月份（补零）           | `01` ~ `12`         |
| `%d` | 日（补零）             | `01` ~ `31`         |
| `%H` | 24 小时制小时          | `00` ~ `23`         |
| `%I` | 12 小时制小时          | `01` ~ `12`         |
| `%M` | 分钟                   | `00` ~ `59`         |
| `%S` | 秒                     | `00` ~ `59`         |
| `%f` | 微秒（6 位）           | `000000` ~ `999999` |
| `%A` | 星期全名               | `Monday`            |
| `%a` | 星期缩写               | `Mon`               |
| `%B` | 月份全名               | `June`              |
| `%b` | 月份缩写               | `Jun`               |
| `%p` | AM / PM                | `AM` / `PM`         |
| `%w` | 星期数字（0=周日）     | `0` ~ `6`           |
| `%j` | 一年中的第几天         | `001` ~ `366`       |
| `%W` | 一年中的第几周（周一起） | `00` ~ `53`       |
| `%Z` | 时区名称               | `CST`               |
| `%%` | 百分号本身             | `%`                 |

---

## 7. 时区处理

### 基本时区操作

```python
from datetime import datetime, timezone, timedelta

# UTC 时间
utc_now = datetime.now(timezone.utc)
print(f"UTC 时间: {utc_now}")

# 创建东八区（北京时间）
beijing_tz = timezone(timedelta(hours=8))
beijing_now = datetime.now(beijing_tz)
print(f"北京时间: {beijing_now}")

# 创建其他时区
tokyo_tz = timezone(timedelta(hours=9))
tokyo_now = datetime.now(tokyo_tz)
print(f"东京时间: {tokyo_now}")

# 转换时区
utc_to_beijing = utc_now.astimezone(beijing_tz)
print(f"UTC 转北京: {utc_to_beijing}")
```

### 时区感知 vs 朴素 datetime

```python
from datetime import datetime, timezone

# 朴素 datetime（没有时区信息）
naive = datetime(2024, 6, 1, 14, 30)
print(f"朴素: {naive.tzinfo}")  # None

# 时区感知 datetime（有时区信息）
aware = datetime(2024, 6, 1, 14, 30, tzinfo=timezone.utc)
print(f"感知: {aware.tzinfo}")  # UTC

# 给朴素 datetime 添加时区
from_naive = naive.replace(tzinfo=timezone.utc)
print(f"添加后: {from_naive}")
```

> **建议**：处理跨时区的业务时，始终使用时区感知的 datetime，避免出现难以排查的时间偏差问题。

---

## 8. 实用示例

### 示例 1：计算年龄

```python
from datetime import date

def calculate_age(birthday):
    today = date.today()
    # 先按年份减，如果今年生日还没到则再减 1
    age = today.year - birthday.year
    if (today.month, today.day) < (birthday.month, birthday.day):
        age -= 1
    return age

birthday = date(2000, 3, 15)
print(f"年龄: {calculate_age(birthday)} 岁")
```

### 示例 2：倒计时

```python
from datetime import datetime

target = datetime(2025, 1, 1, 0, 0, 0)
now = datetime.now()
diff = target - now

print(f"距离 2025 年元旦:")
print(f"  {diff.days} 天 {diff.seconds // 3600} 小时 {(diff.seconds % 3600) // 60} 分钟")
```

### 示例 3：生成日期范围

```python
from datetime import date, timedelta

def date_range(start_date, end_date):
    dates = []
    current = start_date
    while current <= end_date:
        dates.append(current)
        current += timedelta(days=1)
    return dates

start = date(2024, 6, 1)
end = date(2024, 6, 7)

for single_date in date_range(start, end):
    print(single_date.strftime("%Y-%m-%d (%A)"))
```

### 示例 4：日志时间戳格式化

```python
from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

log("程序启动")
log("正在加载数据...")
log("加载完成")
```

### 示例 5：判断是否为工作日

```python
from datetime import date

def is_workday(target_date):
    # weekday() 返回 0-6，0=周一，5=周六，6=周日
    return target_date.weekday() < 5

today = date.today()
if is_workday(today):
    print(f"{today} 是工作日")
else:
    print(f"{today} 是周末")
```

### 示例 6：解析用户输入的日期

```python
from datetime import datetime

def parse_user_date(date_string):
    formats = [
        "%Y-%m-%d",       # 2024-06-01
        "%Y/%m/%d",       # 2024/06/01
        "%d-%m-%Y",       # 01-06-2024
        "%Y年%m月%d日",   # 2024年06月01日
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue

    print(f"无法解析日期: {date_string}")
    return None

print(parse_user_date("2024-06-01"))
print(parse_user_date("2024年06月01日"))
```

---

## 9. 常见问题

### Q：`datetime.now()` 和 `datetime.today()` 有什么区别？

- `datetime.now()` 可以传入时区参数，返回指定时区的当前时间
- `datetime.today()` 等价于 `datetime.now()` 但不支持时区参数
- 实际使用中推荐 `datetime.now()`

### Q：怎么获取上个月的最后一天？

```python
from datetime import date, timedelta

today = date.today()
# 本月第一天
first_of_this_month = today.replace(day=1)
# 本月第一天减 1 天 = 上月最后一天
last_of_prev_month = first_of_this_month - timedelta(days=1)
print(f"上月最后一天: {last_of_prev_month}")
```

### Q：`strftime` 中文字符报错怎么办？

在 Windows 上有时会遇到编码问题。确保你的 Python 文件使用 UTF-8 编码保存：

```python
# 在文件开头确保编码
# -*- coding: utf-8 -*-

from datetime import datetime
print(datetime.now().strftime("%Y年%m月%d日"))
```

### Q：需要更强大的日期处理怎么办？

对于复杂的日期需求（如"下个月的第二个周二"、"自然语言解析日期"等），推荐第三方库：

- **`dateutil`**：强大的日期解析和计算
- **`arrow`**：更人性化的日期时间库
- **`pendulum`**：类似 moment.js 的 Python 日期库

---

## 返回

[← 返回模块与包](./README.md)
