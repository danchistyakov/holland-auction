import time
import sys
import select
import platform


class DutchAuction:
    def __init__(self, auction_lots, auction_interval):
        self.lots = auction_lots
        self.interval = auction_interval

    def get_input_with_timeout(self, prompt, timeout):
        system_platform = platform.system()
        if system_platform == "Windows":
            return self._get_input_windows(prompt, timeout)
        else:
            return self._get_input_unix(prompt, timeout)

    @staticmethod
    def _get_input_windows(prompt, timeout):
        import msvcrt
        start_time = time.time()
        input_str = ""
        sys.stdout.write(prompt)
        sys.stdout.flush()
        while time.time() - start_time < timeout:
            if msvcrt.kbhit():
                char = msvcrt.getwch()
                if char == "\r":  # Enter
                    print()
                    return input_str.strip()
                elif char == "\b":  # Backspace
                    input_str = input_str[:-1]
                    sys.stdout.write("\b \b")
                else:
                    input_str += char
                    sys.stdout.write(char)
                sys.stdout.flush()
        print()
        return None

    @staticmethod
    def _get_input_unix(prompt, timeout):
        sys.stdout.write(prompt)
        sys.stdout.flush()
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if ready:
            return sys.stdin.readline().strip()
        return None

    def start_auction_for_lot(self, lot):
        start_price, min_price, decrement = lot
        current_price = start_price
        print(f"Аукцион начался! Лот: {lot}, начальная цена: {current_price}")

        while current_price >= min_price:
            print(f"Текущая цена: {current_price}")
            print("Купить за эту цену? (ответ только 'Да')")
            response = input()
            if response
            response = self.get_input_with_timeout("Введите 'Да' для покупки: ", self.interval)
            if response == "Да":
                print(f"Товар продан за {current_price}!")
                return

            current_price -= decrement
            current_price = max(current_price, min_price)

        print("Аукцион завершен. Покупателей не найдено.")

    def start(self):
        for lot in self.lots:
            self.start_auction_for_lot(lot)


if __name__ == "__main__":
    lots = [
        (1000, 500, 50),
        (2000, 1000, 100)
    ]
    interval = 5
    auction = DutchAuction(lots, interval)
    auction.start()