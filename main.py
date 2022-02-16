from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

chrome_driver_path = Service(os.environ.get("CHROMEDRIVER_PATH"))  # Path to chromedriver
driver = webdriver.Chrome(service=chrome_driver_path, options=webdriver.ChromeOptions())

cookie_clicker_url = "https://orteil.dashnet.org/experiments/cookie"
driver.get(cookie_clicker_url)

cookie = driver.find_element(By.ID, "cookie")

timeout = time.time() + 3.5  # Time delay between purchases
stop_time = time.time() + 60  # End time

is_on = True
while is_on:
    cookie.click()

    # ----- Make a purchase after time delay ----- #

    if time.time() > timeout:

        # ----- Return the amount of money and list of upgrades ----- #

        money = int(driver.find_element(By.ID, "money").text)
        upgrades = driver.find_elements(By.CSS_SELECTOR, "#store div")

        highest_price = 0
        choice = {
            "id": "",
            "price": 0
        }

        # ----- Check each upgrade for availability ----- #

        for i in range(len(upgrades)):
            try:
                price = int("".join(upgrades[i].text.split("\n")[0].split(" ")[-1].split(",")))

                # ----- Check if there is enough money for the upgrade ----- #
                # -----  and if the price is more than the highest previous price ----- #

                if money >= price >= highest_price:
                    choice["id"] = upgrades[i].get_property("id")
                    choice["price"] = price
                    highest_price = price
            except:
                pass

        # ----- Find the best element by id and purchase it ----- #

        best_upg = driver.find_element(By.ID, f"{choice['id']}")
        best_upg.click()

        # ----- Reset the time delay ----- #

        timeout = time.time() + 5

    # ----- If the time ends - stop the loop and return the number of 'cookies per second' ----- #

    if time.time() > stop_time:
        is_on = False
        cps = driver.find_element(By.ID, "cps").text.split(" ")[-1]
        print(f"Cookies per second: {cps}.")
