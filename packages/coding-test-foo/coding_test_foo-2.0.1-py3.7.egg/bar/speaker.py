from datetime import datetime


def hello_world():
    print("hello world")


def say(words):
    print("you just said: " + words)


def smile():
    print("hiahiahia")


def now():
    print(datetime.now())


def multiplication_table():
    for i in range(1, 10):
        for j in range(1, i + 1):
            print("%d * %d = %2d" % (i, j, i * j), end="\t")
        print("")
