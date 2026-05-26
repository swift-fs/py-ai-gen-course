def do_sum(*args):
    return sum(args)


def do_divide(a, b):
    if b == 0:
        raise ValueError("除数不能为0")
    return a / b


def do_float_sum(a, b):
    return a + b
