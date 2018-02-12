"""
クロージャー
実行されていない関数を返す
任意のタイミングで関数の実行できる
"""


def outer(pi):

    def inner(rad):
        return pi*rad**2

    return inner


"""
outerの引数を受け取ったinner関数を返す
任意のタイミングでinner引数を渡して実行
"""

f1 = outer(3.14)
f2 = outer(3)
print(f1(10), f2(10))
