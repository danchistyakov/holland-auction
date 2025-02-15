import time
import sys
import select


class DutchAuction:
    def __init__(self, lots):
        self.lots = lots

    def start(self):
        for lot in self.lots:
            start_price, min_price, decrement, interval = lot
            current_price = start_price
            print(f"Аукцион начался! Лот: {lot}, начальная цена: {current_price}")

            while current_price > min_price:
                time.sleep(interval)
                current_price -= decrement
                current_price = max(current_price, min_price)
                print(f"Новая цена: {current_price}")

                print("Купить за эту цену? (ответ только 'Да')")
                sys.stdout.flush()

                ready, _, _ = select.select([sys.stdin], [], [], 2)
                if ready:
                    response = sys.stdin.readline().strip()
                    if response == "Да":
                        print(f"Товар продан за {current_price}!")
                        break
            else:
                print("Аукцион завершен. Покупателей не найдено.")

if __name__ == "__main__":
    lots = [
        (1000, 500, 50, 2),
        (2000, 1000, 100, 2)
    ]
    auction = DutchAuction(lots)
    auction.start()
