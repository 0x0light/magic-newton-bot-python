import os
import time
from colorama import Fore, Style, init

# Khởi tạo colorama để hỗ trợ in màu trên Windows
init(autoreset=True)

def display_header():
    os.system('cls' if os.name == 'nt' else 'clear')  # Xóa màn hình terminal trước khi hiển thị
    print(Fore.CYAN + "=" * 40)
    print(Fore.CYAN + "     Magicnewton Daily Roll Bot      ")
    print(Fore.CYAN + "         Created by OhariFN    ")
    print(Fore.CYAN + "        https://t.me/OhariFN   ")
    print(Fore.CYAN + "=" * 40)
    print()

def delay(ms):
    time.sleep(ms / 1000)

if __name__ == "__main__":
    display_header()
