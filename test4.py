class ClassA:
    def __init__(self, initial_value=0):
        self.value = initial_value


    def print_value(self):
        print(f"ClassAの現在の値: {self.value}")

class ClassB:
    def __init__(self, class_a):
        self.class_a = class_a

    def update_value_in_a(self, new_value):
        self.class_a.value = new_value

# ClassAのインスタンスを作成
a = ClassA()

# ClassBのインスタンスを作成し、ClassAのインスタンスを渡す
b = ClassB(a)

# ClassAで値を出力
a.print_value()

# ClassBからClassAの値を更新
b.update_value_in_a(200)

# 再度ClassAで値を出力
a.print_value()

# while文でループさせる例
import time

while True:
    # ClassBからClassAの値を更新
    new_value = int(input("新しい値を入力してください: "))
    b.update_value_in_a(new_value)

    # ClassAで値を出力
    a.print_value()

    # ループを適当に遅延させる
    time.sleep(1)