# 第 14 章：异步编程

> **学习目标**：理解同步与异步的区别，掌握 async/await 语法，学会用 asyncio 处理并发任务。

---

## 1. 同步 vs 异步

**同步**：一行一行执行，上一行完成才执行下一行。如果某行要等 2 秒，整个程序就卡 2 秒。

**异步**：遇到等待操作时，先去做别的事情，等好了再回来继续。

适合异步的场景：网络请求、文件读写、数据库查询——大量"等待"的操作。

---

## 2. async/await 基本语法

```python
import asyncio

async def say_hello(name, delay):
    """异步函数（协程）"""
    print(f"{name} 开始")
    await asyncio.sleep(delay)    # 非阻塞等待
    print(f"{name} 结束（等了{delay}秒）")

# 运行异步函数
asyncio.run(say_hello("小明", 1))
```

- `async def` 定义异步函数（也叫协程）
- `await` 等待异步操作完成
- `asyncio.run()` 运行异步程序

---

## 3. 并发执行多个任务

```python
import asyncio
import time

async def fetch_data(name, delay):
    print(f"  {name} 开始请求...")
    await asyncio.sleep(delay)    # 模拟网络请求
    print(f"  {name} 完成")
    return f"{name}的数据"

async def main():
    start = time.time()

    # 并发执行（同时开始，总时间 = 最慢的那个）
    results = await asyncio.gather(
        fetch_data("API-1", 2),
        fetch_data("API-2", 1),
        fetch_data("API-3", 3),
    )

    elapsed = time.time() - start
    print(f"结果: {results}")
    print(f"总耗时: {elapsed:.1f}秒")    # 约3秒（不是6秒！）

asyncio.run(main())
```

### gather vs 顺序执行

```python
# ❌ 顺序执行：总共 2+1+3 = 6 秒
r1 = await fetch_data("API-1", 2)
r2 = await fetch_data("API-2", 1)
r3 = await fetch_data("API-3", 3)

# ✅ 并发执行：总共 max(2,1,3) = 3 秒
results = await asyncio.gather(
    fetch_data("API-1", 2),
    fetch_data("API-2", 1),
    fetch_data("API-3", 3),
)
```

---

## 4. 超时控制

```python
async def slow_operation():
    await asyncio.sleep(10)
    return "完成"

async def main():
    try:
        # 最多等 3 秒
        result = await asyncio.wait_for(slow_operation(), timeout=3)
    except asyncio.TimeoutError:
        print("操作超时")

asyncio.run(main())
```

---

## 5. 创建任务

```python
async def main():
    # create_task 立即开始执行（不用等）
    task1 = asyncio.create_task(fetch_data("A", 2))
    task2 = asyncio.create_task(fetch_data("B", 1))

    # 可以在这里做其他事情
    print("任务已提交，等待结果...")

    # 需要结果时再 await
    r1 = await task1
    r2 = await task2
    print(f"结果: {r1}, {r2}")

asyncio.run(main())
```

---

## 6. 实际应用场景

### 异步 HTTP 请求

```python
# 需要安装：uv add aiohttp
import aiohttp
import asyncio

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response.status

async def main():
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
    ]
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)

# asyncio.run(main())
```

---

## 本章小结

| 概念 | 说明 |
|------|------|
| `async def` | 定义异步函数 |
| `await` | 等待异步操作 |
| `asyncio.run()` | 运行异步程序 |
| `asyncio.gather()` | 并发执行多个协程 |
| `asyncio.create_task()` | 创建后台任务 |
| `asyncio.wait_for()` | 超时控制 |

---

## 下一步

进入 [第 15 章：标准库深入](../15-stdlib-deep-dive/README.md)。
