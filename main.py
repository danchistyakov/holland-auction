import time
import sys
import select
import platform


class DutchAuction:
    def __init__(self, lots):
        self.lots = lots

    def get_input_with_timeout(self, timeout):
        system_platform = platform.system()
        if system_platform == "Windows":
            import msvcrt
            start_time = time.time()
            input_str = ""
            while time.time() - start_time < timeout:
                if msvcrt.kbhit():
                    char = msvcrt.getwch()
                    if char == "\r":  # Enter
                        print()
                        return input_str.strip()
                    elif char == "\b":  # Backspace
                        input_str = input_str[:-1]
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                    else:
                        input_str += char
                        sys.stdout.write(char)
                        sys.stdout.flush()
            print()
            return None
        else:
            sys.stdout.write("Введите 'Да' для покупки")
            sys.stdout.flush()
            ready, _, _ = select.select([sys.stdin], [], [], timeout)
            if ready:
                return sys.stdin.readline().strip()
            return None

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
                response = self.get_input_with_timeout(2)
                if response == "Да":
                    print(f"Товар продан за {current_price}!")
                    break
            else:
                print("Аукцион завершен. Покупателей не найдено.")


# Пример использования
if __name__ == "__main__":
    lots = [
        (1000, 500, 50, 2),
        (2000, 1000, 100, 2)
    ]
    auction = DutchAuction(lots)
    auction.start()
