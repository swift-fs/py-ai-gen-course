import asyncio
import time


async def asy_hi(name: str, delay: int):
    print(f"  {name} 开始")
    await asyncio.sleep(delay)
    print(f"  {name} 结束（等了{delay}秒）")
    return f"{name}完成"


async def fetch_data(name: str, delay: int):
    print(f"  {name} 开始请求...")
    await asyncio.sleep(delay)
    print(f"  {name} 完成")
    return f"{name}的数据"


async def main():
    # 并发执行
    # start_time = time.time()
    # try:
    #     results = await asyncio.gather(
    #         asy_hi("小明", 3),
    #         asyncio.wait_for(fetch_data("API-1", 5), timeout=4),
    #     )
    # except asyncio.TimeoutError:
    #     print("  超时")
    #     return
    # print(f"  结果: {results}")
    # end_time = time.time()
    # print(f"  总耗时: {end_time - start_time:.2f}秒")

    task1 = asyncio.create_task(asy_hi("小明", 3))
    task2 = asyncio.create_task(fetch_data("API-1", 5))
    start_time = time.time()
    print("任务已提交，等待结果...")
    await task1
    await task2
    end_time = time.time()
    print(f"  总耗时: {end_time - start_time:.2f}秒")

    print(f"  结果: {task1.result()}")
    print(f"  结果: {task2.result()}")


asyncio.run(main())
