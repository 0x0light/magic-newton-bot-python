import asyncio
import time
import random
from datetime import datetime
from header import display_header
from playwright.async_api import async_playwright
from colorama import Fore, Style, init

display_header()
init(autoreset=True)  

MAGICNEWTON_URL = "https://www.magicnewton.com/portal/rewards"
DEFAULT_SLEEP_TIME = 24 * 60 * 60  

def random_extra_delay():
    return random.randint(5, 10) * 60 

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def delay(seconds):
    await asyncio.sleep(seconds)

async def run_account(cookie, proxy, account_index):
    try:
        async with async_playwright() as p:
            proxy_options = None
            if proxy:
                parts = proxy.split(":")
                if len(parts) == 4:
                    ip, port, user, password = parts
                    proxy_options = {
                        "server": f"http://{ip}:{port}",
                        "username": user,
                        "password": password
                    }
                else:
                    print(Fore.RED + f"[Account {account_index}] Proxy format invalid: {proxy}")

            browser = await p.chromium.launch(
                headless=True,
                proxy=proxy_options
            )
            context = await browser.new_context()
            page = await context.new_page()
            await context.add_cookies([cookie])
            await page.goto(MAGICNEWTON_URL, wait_until="networkidle")

            user_address = await page.eval_on_selector("p.gGRRlH.WrOCw.AEdnq.hGQgmY.jdmPpC", "el => el.innerText") or "Unknown"
            print(Fore.CYAN + f"[Account {account_index}] {get_current_time()} - Your account: {user_address}")

            user_credits = await page.eval_on_selector("#creditBalance", "el => el.innerText") or "Unknown"
            print(Fore.GREEN + f"[Account {account_index}] {get_current_time()} - Total your points: {user_credits}")

            roll_now_clicked = await page.evaluate("""
                () => {
                    let btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Roll now'));
                    if (btn) { btn.click(); return true; }
                    return false;
                }
            """)
            if roll_now_clicked:
                print(Fore.YELLOW + f"[Account {account_index}] {get_current_time()} - Starting daily roll...")
                await delay(5)

            await browser.close()
    except Exception as e:
        print(Fore.RED + f"[Account {account_index}] {get_current_time()} - Error: {e}")

async def main():
    with open("E:\\Code\\magic-newton-bot\\data.txt", "r") as f:
        cookies = [
            {"name": "__Secure-next-auth.session-token", "value": line.strip(), "domain": ".magicnewton.com", "path": "/", "secure": True, "httpOnly": True}
            for line in f if line.strip()
        ]

    with open("E:\\Code\\magic-newton-bot\\proxy.txt", "r") as f:
        proxies = [line.strip() for line in f if line.strip()]

    if len(proxies) < len(cookies):
        proxies += [None] * (len(cookies) - len(proxies))

    print(Fore.CYAN + f"[Starting] {get_current_time()} - Running accounts with proxies...")

    tasks = [run_account(cookies[i], proxies[i], i + 1) for i in range(len(cookies))]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
