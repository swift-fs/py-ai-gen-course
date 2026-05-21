# 第 17 章配套代码：测试
# 运行方式：python calculator.py（手动验证）
#           uv run pytest test_calculator.py -v（pytest 测试）

def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

if __name__ == "__main__":
    print("=== 手动验证 ===")
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    print("  add 测试通过")

    assert divide(10, 2) == 5.0
    print("  divide 测试通过")

    try:
        divide(10, 0)
        print("  ❌ 应该抛出异常")
    except ValueError:
        print("  除零异常测试通过")

    print("\n所有测试通过！")
