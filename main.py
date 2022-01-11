import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_driver_path = "/home/janf/Development/chromedriver"
ser = Service(chrome_driver_path)
driver = webdriver.Chrome(service=ser)


driver.get("http://orteil.dashnet.org/experiments/cookie/")
# Get cookie to click on.
cookie = driver.find_element(By.ID, "cookie")

# Get upgrade item ids.
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60*5 # 5minutes

price = 0

while True:
    cookie.click()
    if time.time() > timeout:
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        prices = []
        for price in all_prices:
            if price.text != "":
                prices.append(int(price.text.split("-")[1].strip().replace(",", "")))

        print(prices)

        upgrade_prices = {}
        for i in range(len(prices)):
            upgrade_prices[prices[i]] = item_ids[i]

        print(upgrade_prices)

        cookies_count = int(driver.find_element(By.ID, "money").text.replace(",", ""))
        affordable_upgrades = {}
        for price, upgrade in upgrade_prices.items():
            if price <= cookies_count:
                affordable_upgrades[price] = upgrade

        print(affordable_upgrades)

        max_affordable_price = max(affordable_upgrades)

        driver.find_element(By.ID, affordable_upgrades[max_affordable_price]).click()
        timeout = time.time() + 5

        if time.time() > five_min:
            cookie_per_s = driver.find_element(By.ID, "cps").text
            print(cookie_per_s)
            break

