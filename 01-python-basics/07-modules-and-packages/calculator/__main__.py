import sys

from calculator import add, power, subtract

if len(sys.argv) < 4:
    print("用法: python -m calculator <操作> <a> <b>")
    print("操作: add / subtract / power")
    sys.exit(1)

operation = sys.argv[1]
a, b = int(sys.argv[2]), int(sys.argv[3])

if operation == "add":
    print(f"{a} + {b} = {add(a, b)}")
elif operation == "subtract":
    print(f"{a} - {b} = {subtract(a, b)}")
elif operation == "power":
    print(f"{a} ^ {b} = {power(a, b)}")
else:
    print(f"未知操作: {operation}")
