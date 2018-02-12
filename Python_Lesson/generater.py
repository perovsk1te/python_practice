"""
ジェネレーター
要素を一個ずつ作り出す
一気に処理しない、小分けに実行できる
"""


def greeting():
    yield 'Good,morning'
    yield 'Good,afternoon'
    yield  'Good,night'


def counter(num=10):
    for i in range(num):
        yield 'run'


g = greeting()
c = counter()


print(next(g))
print(next(c))
print(next(c))
print(next(c))
print(next(g))
print(next(c))
print(next(c))
print(next(c))
print(next(g))
print(next(c))
print(next(c))
print(next(c))
print(next(c))


