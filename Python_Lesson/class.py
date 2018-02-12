"""
objectはいらないがコードスタイル的に書いたほうがいい
コンストラクタ：__init__で初期化、インスタンスが出来た瞬間に実行される
デストラクタ：__del__, インスタンスがなくなるとき呼び出される
クラス全体で使いたい変数はself.paramとしてオブジェクト変数にする
クラス変数はすべてのオブジェクトで共有される
"""


class Person(object):
    def __init__(self, name):
        self.name = name
        print(self.name)

    def say_something(self):
        print('Im {}'.format(self.name))
        self.run(10)

    def run(self, num):
            print('run'*num)

    def __del__(self):
        print('Bye')


person = Person("Mike")
person.say_something()

del person

"""
継承
みんなで使う関数をまとめられる
上書きできる,superで親クラスを呼び出せる
@propertyで読み込み専用にできる、関数ではなくクラス変数として扱われる
@param.setterで特定の条件を満たしたときのみ書き換えられるようにする
"""

"""
抽象クラス
@abstractmethodがついたクラスは必ず継承する
多用しないほうが良い
"""
import abc


class Person(metaclass=ABCMeta):
    def __init__(self, age=1):
        self.age = age

    @abc.abstractclassmethod
    def drive(self):
        pass


class Baby(Person):
    def __init__(self, age=1):
        if age < 18:
            super().__init__(age)
        else:
            raise ValueError

    def drive(self):
        raise Exception('No drive')


class Adult(Person):
    def __init__(self, age=18):
        if age >= 18:
            super().__init__(age)
        else:
            raise ValueError

    def drive(self):




baby=Baby()
adult=Adult()


class Car(object):
    def __init__(self, model = None):
        self.model = model

    def run(self):
        print('run')

    def ride(self, person):
        person.drive()


car = Car()
car.ride(adult)
car.ride(baby)


class ToyotaCar(Car):
    def run(self):
        print('fast')


class TeslaCar(Car):
    def __init__(self, model = 'Model s',
                 enable_auto_run=False,
                 password="123"):
        #self.model = model
        super().init(model)
        #self.enable_auto_run = enable_auto_run
        """
        アンダースコアが二個だとアクセスできなくなる、ただしクラス内
        からはアクセスできる    
        """
        self._enable_auto_run = enable_auto_run
        self.password = password

    @property
    def enable_auto_run(self):
        return self._enable_auto_run

    @enable_auto_run.setter
    def enable_auto_run(self, is_enable):
        if self.password == "456":
            self.enable_auto_run = is_enable
        else:
            raise ValueError


"""
多重継承
関数名が被ったら左が優先
使わないほうが良い
"""

class Person(object):
    def talk(self):
        print('talk')

    def run(self):
        print('person run')


class Car(object):
    def run(self):
        print('run')


class PersonCar(Person, Car):
    def fly(self):
        print('fly')

"""
()をつけないとオブジェクトは生成されない(__init__が実行されない)
オブジェクトをつけなくてもクラス変数にはアクセスできる
@classmethodでクラスメソッドにできる、オブジェクトを生成しなくても呼び出せる
@staticmethodでs他ティックメソッドにできる、クラスの外に置いてもいいが
関連性がある場合はスタティックメソッドとして中に置いたほうがわかりやすい
"""
class Person(object):
    kind = 'human'

    def __init__(self):
        self.age = 100

    @classmethod
    def what_is_your_kind(cls):
        return cls.kind

    @staticmethod
    def about(year):
        print('about human {}'.format(year))

a = Person()
b = Person

"""
特殊メソッド
__init__ コンストラクタ
__str__ オブジェクトを文字列として扱おうとしたときに呼ばれる
__len__  len(object)で呼び出される
__aadd__ オブジェクトの足し算
__eq__ オブジェクトの比較
"""
class Word(object):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return'Word!!!!'

    def __len__(self):
        return len(self.text)

    def __add__(self, other):
        self.text.lower() + other.text.lower()

    def __eq__(self, other):
        return self.text.lower()  == other.text.lower()

w=Word('test')
print(len(w))

w2=Word('#########')
print(w + w2)
print(w == w2)
