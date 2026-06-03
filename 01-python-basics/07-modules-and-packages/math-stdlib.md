# math 标准库 —— 数学运算

> **学习目标**：掌握 `math` 模块中常用的数学函数和常量，能处理取整、幂运算、三角函数等常见数学计算。

---

## 1. 什么是 math 模块？

`math` 模块提供了对 C 标准库中数学函数的访问，适合处理**浮点数**的数学运算。如果你需要做科学计算（矩阵、线性代数等），可以使用第三方库 `numpy`；但如果只是日常的数学计算，`math` 就足够了。

```python
import math
```

---

## 2. 数学常量

`math` 模块内置了几个常用的数学常量：

```python
print(math.pi)       # 3.141592653589793  —— 圆周率 π
print(math.e)        # 2.718281828459045  —— 自然常数 e
print(math.tau)      # 6.283185307179586  —— 2π（ Tau）
print(math.inf)      # inf                —— 正无穷大
print(-math.inf)     # -inf               —— 负无穷大
print(math.nan)      # nan                —— 非数字（Not a Number）
```

### 常量说明

| 常量        | 值                     | 说明                   |
| ----------- | ---------------------- | ---------------------- |
| `math.pi`   | 3.141592653589793      | 圆周率                 |
| `math.e`    | 2.718281828459045      | 自然对数的底           |
| `math.tau`  | 6.283185307179586      | 2π，等于 `2 * math.pi` |
| `math.inf`  | 正无穷                 | 大于任何有限浮点数     |
| `math.nan`  | NaN                    | 任何和 NaN 的比较都为 False |

### 特殊值判断

```python
# 判断是否为无穷大
print(math.isinf(math.inf))     # True
print(math.isinf(100))          # False

# 判断是否为 NaN
print(math.isnan(math.nan))     # True
print(math.isnan(0))            # False
```

> **为什么不用 `==` 判断 NaN？** 因为 `math.nan == math.nan` 返回 `False`！NaN 是唯一一个不等于自身的值。

---

## 3. 取整函数

### `math.ceil(x)` —— 向上取整

返回大于等于 x 的最小整数。

```python
print(math.ceil(3.2))    # 4
print(math.ceil(3.0))    # 3（已经是整数，不变）
print(math.ceil(-3.2))   # -3（注意：-3 > -3.2，向上是更大的方向）
```

### `math.floor(x)` —— 向下取整

返回小于等于 x 的最大整数。

```python
print(math.floor(3.8))    # 3
print(math.floor(3.0))    # 3
print(math.floor(-3.8))   # -4（注意：-4 < -3.8，向下是更小的方向）
```

### `math.trunc(x)` —— 截断（向零取整）

直接丢弃小数部分，只保留整数部分。

```python
print(math.trunc(3.8))    # 3
print(math.trunc(-3.8))   # -3（向零方向截断，不是向下）
```

### 三种取整方式对比

| 值     | `ceil` (向上) | `floor` (向下) | `trunc` (向零) |
| ------ | ------------- | -------------- | -------------- |
| `3.7`  | 4             | 3              | 3              |
| `-3.7` | -3            | -4             | -3             |
| `3.0`  | 3             | 3              | 3              |

### 与内置 `round()` 的区别

```python
# round() 是四舍五入，不是 math 模块的函数
print(round(3.5))    # 4
print(round(2.5))    # 2（银行家舍入：四舍六入五成双）
print(round(3.14159, 2))  # 3.14（保留 2 位小数）
```

> **提示**：需要四舍五入用内置 `round()`，需要向上/向下取整用 `math.ceil()` / `math.floor()`。

---

## 4. 绝对值与符号

### `math.fabs(x)` —— 浮点数绝对值

返回 x 的绝对值（浮点数）。

```python
print(math.fabs(-5))      # 5.0
print(math.fabs(3.14))    # 3.14
```

> 与内置 `abs()` 的区别：`math.fabs()` 始终返回浮点数，`abs()` 对整数返回整数。

### `math.copysign(x, y)` —— 复制符号

返回一个值，大小为 `x`，符号与 `y` 相同。

```python
print(math.copysign(5, -1))     # -5.0
print(math.copysign(-3, 2))     # 3.0
print(math.copysign(4, -0.0))   # -4.0（负零的符号也被复制）
```

---

## 5. 幂运算与对数

### `math.sqrt(x)` —— 平方根

```python
print(math.sqrt(16))      # 4.0
print(math.sqrt(2))       # 1.4142135623730951
print(math.sqrt(0))       # 0.0
```

> **注意**：`math.sqrt(-1)` 会抛出 `ValueError`。如果需要复数结果，使用 `cmath.sqrt(-1)`。

### `math.pow(x, y)` —— 幂运算

返回 `x ** y` 的浮点数结果。

```python
print(math.pow(2, 10))    # 1024.0
print(math.pow(9, 0.5))   # 3.0（等价于 sqrt）
```

> 与 `**` 运算符的区别：`math.pow()` 始终返回浮点数，而 `2 ** 10` 返回整数 `1024`。

### `math.log(x, base)` —— 对数

```python
# 自然对数（以 e 为底）
print(math.log(math.e))      # 1.0
print(math.log(10))          # 2.302585092994046

# 以 2 为底
print(math.log(1024, 2))     # 10.0

# 以 10 为底（推荐用 log10 更精确）
print(math.log(1000, 10))    # 2.9999999999999996（有精度误差）
```

### `math.log10(x)` —— 常用对数（以 10 为底）

比 `math.log(x, 10)` 更精确。

```python
print(math.log10(1000))    # 3.0
print(math.log10(100))     # 2.0
```

### `math.log2(x)` —— 以 2 为底的对数

比 `math.log(x, 2)` 更精确。

```python
print(math.log2(1024))    # 10.0
print(math.log2(256))     # 8.0
```

---

## 6. 三角函数

`math` 模块提供了完整的三角函数，但**参数和返回值都是弧度，不是角度**。

### 角度与弧度的转换

```python
# 角度转弧度
print(math.radians(180))    # 3.141592653589793（等于 π）
print(math.radians(90))     # 1.5707963267948966（等于 π/2）

# 弧度转角度
print(math.degrees(math.pi))      # 180.0
print(math.degrees(math.pi / 2))  # 90.0
```

### 基本三角函数

```python
angle = math.radians(30)  # 30 度转弧度

print(math.sin(angle))    # 0.49999999999999994（约 0.5）
print(math.cos(angle))    # 0.8660254037844387
print(math.tan(angle))    # 0.5773502691896257

# 特殊角度
print(math.sin(math.radians(90)))   # 1.0
print(math.cos(math.radians(180)))  # -1.0
```

### 反三角函数

```python
# 反正弦（返回弧度）
angle_rad = math.asin(0.5)
print(math.degrees(angle_rad))  # 30.000000000000004（约 30 度）

# 反余弦
angle_rad = math.acos(0.5)
print(math.degrees(angle_rad))  # 60.0

# 反正切
angle_rad = math.atan(1)
print(math.degrees(angle_rad))  # 45.0
```

### `math.atan2(y, x)` —— 两参数反正切

考虑了 x 和 y 的符号，能正确判断象限。在游戏开发和图形计算中常用。

```python
# 点 (1, 1) 的角度
angle = math.atan2(1, 1)
print(math.degrees(angle))  # 45.0

# 点 (-1, 1) 的角度（第二象限）
angle = math.atan2(1, -1)
print(math.degrees(angle))  # 135.0
```

---

## 7. 其他实用函数

### `math.hypot(*coordinates)` —— 欧几里得距离

计算原点到给定坐标的距离，即 $\sqrt{x^2 + y^2}$。

```python
# 2D 距离
print(math.hypot(3, 4))      # 5.0（勾股定理：3² + 4² = 5²）

# 3D 距离
print(math.hypot(1, 2, 2))   # 3.0

# 两点之间的距离
x1, y1 = 1, 2
x2, y2 = 4, 6
distance = math.hypot(x2 - x1, y2 - y1)
print(f"两点距离: {distance}")  # 5.0
```

### `math.gcd(a, b)` —— 最大公约数

```python
print(math.gcd(12, 8))     # 4
print(math.gcd(17, 13))    # 1（互质）
```

> Python 3.9+ 支持多个参数：`math.gcd(12, 8, 20)` 返回 `4`。

### `math.lcm(a, b)` —— 最小公倍数（Python 3.9+）

```python
print(math.lcm(4, 6))      # 12
print(math.lcm(3, 5, 7))   # 105
```

### `math.fsum(iterable)` —— 精确求和

比内置 `sum()` 更精确，避免浮点数累积误差。

```python
# 内置 sum() 有精度误差
numbers = [0.1] * 10
print(sum(numbers))          # 0.9999999999999999（不是 1.0！）
print(math.fsum(numbers))    # 1.0（精确结果）
```

### `math.prod(iterable, start=1)` —— 连乘（Python 3.8+）

```python
print(math.prod([1, 2, 3, 4, 5]))  # 120（5 的阶乘）
print(math.prod([2, 3, 4]))        # 24
```

### `math.perm(n, k)` —— 排列数（Python 3.8+）

从 n 个元素中选 k 个排列，即 $A(n,k) = n! / (n-k)!$。

```python
# 从 5 个中选 3 个排列
print(math.perm(5, 3))    # 60
```

### `math.comb(n, k)` —— 组合数（Python 3.8+）

从 n 个元素中选 k 个组合，即 $C(n,k) = n! / (k!(n-k)!)$。

```python
# 从 5 个中选 3 个组合
print(math.comb(5, 3))    # 10

# 彩票：从 49 个号码中选 6 个
print(math.comb(49, 6))   # 13983816
```

### `math.factorial(n)` —— 阶乘

```python
print(math.factorial(5))    # 120（5! = 5 × 4 × 3 × 2 × 1）
print(math.factorial(0))    # 1（0! = 1）
```

---

## 8. 实用示例

### 示例 1：计算圆的面积和周长

```python
import math

radius = 5.0
area = math.pi * radius ** 2
circumference = 2 * math.pi * radius

print(f"半径: {radius}")
print(f"面积: {area:.2f}")
print(f"周长: {circumference:.2f}")
```

### 示例 2：两点间距离

```python
import math

def distance_between(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

d = distance_between(0, 0, 3, 4)
print(f"距离: {d}")  # 5.0
```

### 示例 3：温度转换（华氏 → 摄氏）并取整

```python
import math

fahrenheit = 98.6
celsius = (fahrenheit - 32) * 5 / 9
print(f"华氏 {fahrenheit}°F = 摄氏 {celsius:.1f}°C")
print(f"向上取整: {math.ceil(celsius)}°C")
print(f"向下取整: {math.floor(celsius)}°C")
```

### 示例 4：计算排列组合

```python
import math

# 班级 30 人，选 3 人当班干部（有顺序）
positions = math.perm(30, 3)
print(f"排列方式: {positions} 种")

# 班级 30 人，选 3 人参加活动（无顺序）
teams = math.comb(30, 3)
print(f"组合方式: {teams} 种")
```

### 示例 5：使用对数计算大数的位数

```python
import math

big_number = 2 ** 1000
# 不直接算，用对数求位数
digits = math.floor(math.log10(big_number)) + 1
print(f"2^1000 有 {digits} 位")  # 302
```

---

## 9. 常用函数速查表

| 函数                        | 说明                   | 示例                   |
| --------------------------- | ---------------------- | ---------------------- |
| `math.pi`                   | 圆周率 π               | `3.141592653589793`    |
| `math.e`                    | 自然常数 e             | `2.718281828459045`    |
| `math.ceil(x)`              | 向上取整               | `ceil(3.2)` → `4`      |
| `math.floor(x)`             | 向下取整               | `floor(3.8)` → `3`     |
| `math.trunc(x)`             | 截断小数               | `trunc(-3.7)` → `-3`   |
| `math.fabs(x)`              | 浮点绝对值             | `fabs(-5)` → `5.0`     |
| `math.sqrt(x)`              | 平方根                 | `sqrt(16)` → `4.0`     |
| `math.pow(x, y)`            | 幂运算（返回浮点）     | `pow(2, 10)` → `1024.0` |
| `math.log(x)`               | 自然对数               | `log(e)` → `1.0`       |
| `math.log10(x)`             | 常用对数               | `log10(100)` → `2.0`   |
| `math.sin(x)`               | 正弦（弧度）           | `sin(pi/2)` → `1.0`    |
| `math.cos(x)`               | 余弦（弧度）           | `cos(pi)` → `-1.0`     |
| `math.radians(deg)`         | 角度 → 弧度            | `radians(180)` → `pi`  |
| `math.degrees(rad)`         | 弧度 → 角度            | `degrees(pi)` → `180`  |
| `math.hypot(x, y)`          | 欧几里得距离           | `hypot(3, 4)` → `5.0`  |
| `math.gcd(a, b)`            | 最大公约数             | `gcd(12, 8)` → `4`     |
| `math.lcm(a, b)`            | 最小公倍数（3.9+）     | `lcm(4, 6)` → `12`     |
| `math.factorial(n)`         | 阶乘                   | `factorial(5)` → `120` |
| `math.comb(n, k)`           | 组合数（3.8+）         | `comb(5, 3)` → `10`    |
| `math.perm(n, k)`           | 排列数（3.8+）         | `perm(5, 3)` → `60`    |
| `math.fsum(iterable)`       | 精确求和               | `fsum([0.1]*10)` → `1.0` |
| `math.prod(iterable)`       | 连乘（3.8+）           | `prod([1,2,3])` → `6`  |

---

## 10. 常见问题

### Q：`math.sqrt(-1)` 报错怎么办？

`math` 不支持负数的平方根。如果需要复数运算，使用 `cmath` 模块：

```python
import cmath
print(cmath.sqrt(-1))  # 1j
```

### Q：`math` 和 `numpy` 有什么区别？

| 特性     | `math`              | `numpy`                  |
| -------- | ------------------- | ------------------------ |
| 类型     | 标准库              | 第三方库（需安装）       |
| 输入     | 单个数值            | 支持数组批量运算         |
| 速度     | 单个值更快          | 批量运算更快             |
| 适用场景 | 简单数学计算        | 科学计算、数据分析       |

### Q：怎么算百分比的向上取整？

```python
import math

completed = 7
total = 33
percent = math.ceil(completed / total * 100)
print(f"进度: {percent}%")  # 向上取整显示 22%
```

---

## 返回

[← 返回模块与包](./README.md)
