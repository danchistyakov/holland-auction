import time
import sys
import select
import random
from threading import Timer


class Lot:
    """Лот — товар, который продается на аукционе."""

    def __init__(self, name, starting_price, decrement, auction_duration, quantity):
        self.name = name  # Название товара
        self.starting_price = starting_price  # Начальная цена
        self.current_price = starting_price  # Текущая цена
        self.decrement = decrement  # Сколько уменьшается цена каждую секунду
        self.time_left = auction_duration  # Время аукциона
        self.quantity = quantity  # Количество товара
        self.sold = False  # Флаг, был ли товар продан

    def decrement_price(self):
        """Уменьшаем цену товара."""
        self.current_price -= self.decrement
        if self.current_price < 0:
            self.current_price = 0  # Цена не может быть меньше нуля

    def is_sold(self):
        """Проверяем, был ли товар продан."""
        return self.sold

    def sell(self):
        """Продаем товар, уменьшаем количество на 1."""
        if self.quantity > 0:
            self.sold = True
            self.quantity -= 1
            print(f"{self.name} был продан за {self.current_price}. Осталось {self.quantity} единиц.")
            return True
        return False


class Agent:
    """Агент — покупатель, который решает, покупать ли товар."""

    def __init__(self, name, is_random=False):
        self.name = name  # Имя покупателя
        self.is_random = is_random  # Флаг, случайный ли агент
        self.bought_lots = []  # Список купленных товаров

    def make_bid(self, lot):
        """Агент решает, купить ли товар, с ограничением по времени на ввод."""
        if lot.name in self.bought_lots:
            return False  # Этот лот уже куплен

        print(f"{self.name}, текущая цена лота {lot.name}: {lot.current_price}.")

        if self.is_random:
            # Второй агент случайным образом решает, покупать ли товар
            response = random.choice(["да", "нет"])
            print(f"{self.name} случайно выбрал: {response}")
        else:
            response = None

            def get_input():
                nonlocal response
                try:
                    response = input("Хотите купить? (да): ").strip().lower()
                except Exception:
                    response = "нет"  # В случае ошибки ввода считаем, что отказались

            # Таймер на 2 секунды
            input_thread = Timer(2.0, lambda: None)  # Таймер на 2 секунды
            input_thread.start()
            get_input()  # Ждем ввода пользователя
            input_thread.cancel()  # Останавливаем таймер

        if response == "да":
            self.bought_lots.append(lot.name)  # Помечаем товар как купленный
            print(f"{self.name} купил {lot.name} за {lot.current_price}")
            return lot.sell()  # Продаем товар
        else:
            print(f"{self.name} не ответил вовремя или отказался. Цена падает.")
            return False


class DutchAuction:
    """Голландский аукцион."""

    def __init__(self, lots, agents):
        self.lots = lots  # Список лотов
        self.agents = agents  # Список агентов

    def start(self):
        """Запускаем аукцион для всех лотов."""
        for lot in self.lots:
            print(f"\nНачинается аукцион на {lot.name}, начальная цена: {lot.starting_price}")

            while lot.time_left > 0 and not lot.is_sold():
                print(f"Текущая цена: {lot.current_price}, оставшееся время: {lot.time_left} секунд")

                for agent in self.agents:
                    if agent.make_bid(lot):  # Если агент купил товар
                        print(f"Аукцион завершен. {lot.name} был продан.")
                        break  # Останавливаем аукцион, если товар продан

                if lot.is_sold():
                    break  # Лот продан, выходим

                # Если товар не был куплен, снижаем цену и уменьшаем время
                lot.decrement_price()
                lot.time_left -= 1  # Уменьшаем оставшееся время
                time.sleep(1)  # Ждем 1 секунду

            if not lot.is_sold():
                print(f"Аукцион завершен. {lot.name} не был продан.")


# Создаем агентов
agent1 = Agent("Покупатель 1", is_random=False)  # Это агент, который будет отвечать вручную
agent2 = Agent("Покупатель 2", is_random=True)  # Это агент, который будет отвечать случайным образом

# Создаем лот для аукциона
lot1 = Lot("Картина 1", 1000, 50, 10, 1)

# Создаем аукцион с двумя агентами и одним лотом
auction = DutchAuction([lot1], [agent1, agent2])

# Запускаем аукцион
auction.start()











