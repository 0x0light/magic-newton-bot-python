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

async def run_account(cookie, account_index):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
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

            lets_roll_clicked = await page.evaluate("""
                () => {
                    let btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes("Let's roll"));
                    if (btn) { btn.click(); return true; }
                    return false;
                }
            """)
            if lets_roll_clicked:
                print(Fore.BLUE + f"[Account {account_index}] {get_current_time()} - Rolling the dice...")
                await delay(5)

                throw_dice_clicked = await page.evaluate("""
                    () => {
                        let btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Throw Dice'));
                        if (btn) { btn.click(); return true; }
                        return false;
                    }
                """)
                if throw_dice_clicked:
                    print(Fore.MAGENTA + f"[Account {account_index}] {get_current_time()} - Waiting for dice animation...")
                    await delay(10)

                    for i in range(1, 6):
                        press_clicked = await page.evaluate("""
                            () => {
                                let btn = Array.from(document.querySelectorAll('p.gGRRlH.WrOCw.AEdnq.gTXAMX.gsjAMe'))
                                    .find(b => b.innerText.includes('Press'));
                                if (btn) { btn.click(); return true; }
                                return false;
                            }
                        """)
                        if press_clicked:
                            print(Fore.YELLOW + f"[Account {account_index}] {get_current_time()} - Press button clicked ({i}/5)")
                            await delay(7)
                        else:
                            print(Fore.RED + f"[Account {account_index}] {get_current_time()} - 'Press' button not found.")
                            break
                        await delay(10)

                    print(Fore.MAGENTA + f"[Account {account_index}] {get_current_time()} - Waiting before click Bank...")
                    await delay(10)

                    try:
                        await page.click("button:nth-child(3) > div > p")
                        print(Fore.GREEN + f"[Account {account_index}] {get_current_time()} - Bank button clicked...")
                        await delay(10)

                        dice_roll_result = await page.eval_on_selector(
                            "h2.gRUWXt.dnQMzm.ljNVlj.kzjCbV.dqpYKm.RVUSp.fzpbtJ.bYPzoC", "el => el.innerText")
                        print(Fore.CYAN + f"[Account {account_index}] {get_current_time()} - Dice Roll Result: {dice_roll_result} points")

                        user_credits = await page.eval_on_selector("#creditBalance", "el => el.innerText")
                        print(Fore.GREEN + f"[Account {account_index}] {get_current_time()} - Final Balance after dice roll: {user_credits}")

                        print(Fore.YELLOW + f"[Account {account_index}] {get_current_time()} - Daily roll completed successfully!")

                    except:
                        print(Fore.RED + f"[Account {account_index}] {get_current_time()} - 'Bank' button not found.")

            await browser.close()
    except Exception as e:
        print(Fore.RED + f"[Account {account_index}] {get_current_time()} - An error occurred: {e}")

async def main():
    with open("E:\\Code\\magic-newton-bot\\data.txt", "r") as f:
        cookies = [
            {"name": "__Secure-next-auth.session-token", "value": line.strip(), "domain": ".magicnewton.com", "path": "/", "secure": True, "httpOnly": True}
            for line in f if line.strip()
        ]
    while True:
        print(Fore.CYAN + f"[Starting] {get_current_time()} - Starting your account...")
        for i, cookie in enumerate(cookies, 1):
            await run_account(cookie, i)
        extra_delay = random_extra_delay()
        print(Fore.MAGENTA + f"[Finished] {get_current_time()} - Bot will run again in 24 hours + {extra_delay // 60} minutes...")
        await delay(DEFAULT_SLEEP_TIME + extra_delay)

if __name__ == "__main__":
    asyncio.run(main())
