import threading
from time import sleep
from random import randint


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        for i in range(100):
            mon = randint(50, 500)
            self.balance += mon
            sleep(0.001)
            print(f"Пополнение: {mon}. Баланс: {self.balance}")
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()

    def take(self):
        for i in range(100):
            mon = randint(50, 500)
            print(f'Запрос на {mon}')
            sleep(0.001)
            if mon <= self.balance:
                self.balance -= mon
                sleep(0.001)
                print(f"Снятие: {mon}. Баланс: {self.balance}")
                if self.lock.locked():
                    self.lock.release()
            else:
                print("Запрос отклонён, недостаточно средств")
                if not self.lock.locked():
                    self.lock.acquire()


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
