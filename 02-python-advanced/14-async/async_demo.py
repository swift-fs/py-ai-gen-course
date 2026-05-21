# 第 14 章配套代码：异步编程
# 运行方式：python async_demo.py

import asyncio
import time

# ============================
# 1. 基本异步函数
# ============================
async def say_hello(name, delay):
    print(f"  {name} 开始")
    await asyncio.sleep(delay)
    print(f"  {name} 结束（等了{delay}秒）")
    return f"{name}完成"

async def demo_basic():
    print("=== 基本异步 ===")
    result = await say_hello("小明", 0.1)
    print(f"  结果: {result}")

# ============================
# 2. 并发执行
# ============================
async def fetch_data(name, delay):
    print(f"  {name} 开始请求...")
    await asyncio.sleep(delay)
    print(f"  {name} 完成")
    return f"{name}的数据"

async def demo_concurrent():
    print("\n=== 并发执行 ===")
    start = time.time()
    results = await asyncio.gather(
        fetch_data("API-1", 0.2),
        fetch_data("API-2", 0.1),
        fetch_data("API-3", 0.3),
    )
    elapsed = time.time() - start
    print(f"  结果: {results}")
    print(f"  总耗时: {elapsed:.2f}秒（接近0.3秒，不是0.6秒）")

# ============================
# 3. 超时控制
# ============================
async def demo_timeout():
    print("\n=== 超时控制 ===")
    async def slow():
        await asyncio.sleep(10)
        return "完成"
    try:
        result = await asyncio.wait_for(slow(), timeout=0.1)
    except asyncio.TimeoutError:
        print("  操作超时")

# ============================
# 4. 创建任务
# ============================
async def demo_tasks():
    print("\n=== 创建任务 ===")
    task1 = asyncio.create_task(fetch_data("A", 0.2))
    task2 = asyncio.create_task(fetch_data("B", 0.1))
    print("  任务已提交")
    r1 = await task1
    r2 = await task2
    print(f"  结果: {r1}, {r2}")

# ============================
# 主函数
# ============================
async def main():
    await demo_basic()
    await demo_concurrent()
    await demo_timeout()
    await demo_tasks()

asyncio.run(main())
