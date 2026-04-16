import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


URL = "http://quotes.toscrape.com"
CSV_FILE = "quotes.csv"
MAX_PAGES = 5


def setup_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def parse_page(driver):
    quotes_data = []
    quotes = driver.find_elements(By.CSS_SELECTOR, "div.quote")

    for quote in quotes:
        text = quote.find_element(By.CSS_SELECTOR, "span.text").text
        author = quote.find_element(By.CSS_SELECTOR, "small.author").text
        tags = [tag.text for tag in quote.find_elements(By.CSS_SELECTOR, "a.tag")]

        quotes_data.append(
            {
                "quote": text,
                "author": author,
                "tags": ", ".join(tags),
                "tags_count": len(tags),
            }
        )

    return quotes_data


def save_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["quote", "author", "tags", "tags_count"])
        writer.writeheader()
        writer.writerows(data)


def main():
    driver = setup_driver()
    all_quotes = []

    try:
        driver.get(URL)

        for page in range(1, MAX_PAGES + 1):
            print(f"Страница {page}...")
            quotes = parse_page(driver)
            all_quotes.extend(quotes)

            try:
                next_btn = driver.find_element(By.CSS_SELECTOR, "li.next > a")
                next_btn.click()
                time.sleep(1)
            except Exception:
                break

        save_to_csv(all_quotes, CSV_FILE)
        print(f"Сохранено {len(all_quotes)} цитат в {CSV_FILE}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
