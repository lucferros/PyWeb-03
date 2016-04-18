import operator, functools


def do_math(func_name, *args):
    numbers = map(int, *args)
    result = {
        "add": functools.reduce(operator.add, numbers),
        "subtract": functools.reduce(operator.sub, numbers),
        "multiply": functools.reduce(operator.mul, numbers),
        "divide": functools.reduce(operator.div, numbers),
    }
    answer = result[func_name]
    return str(answer)


def main():
    numbers = ['5', '6', '8', '2']
    func_name = 'subtract'
    func = do_math(func_name, numbers)
    print(func)

if __name__ == "__main__":
    main()