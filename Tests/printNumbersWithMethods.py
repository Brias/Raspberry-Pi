num = 0


def print_even(n):
    if(n % 2) == 0:
        print(n)


def setup():
    global num
    num = 10


def loop():
    while True:
        global num
        print_even(num)
        num += 1


setup()
loop()