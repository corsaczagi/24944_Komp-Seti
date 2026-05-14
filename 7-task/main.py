import time
import uvicorn

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from database import create_table, save_quotes_to_db, get_all_quotes, get_quotes_count


app = FastAPI(
    title="Quotes Parser API",
    description="API для парсинга цитат и сохранения в PostgreSQL",
    version="1.0.0",
)

create_table()


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


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


def parse_all_pages(start_url, max_pages=5):
    driver = setup_driver()
    all_quotes = []

    try:
        driver.get(start_url)
        print(f"[+] Начинаю парсить: {start_url}")

        for page in range(1, max_pages + 1):
            print(f"    Страница {page}...")
            quotes = parse_page(driver)
            all_quotes.extend(quotes)
            print(f"        Нашел {len(quotes)} цитат")

            try:
                next_btn = driver.find_element(By.CSS_SELECTOR, "li.next > a")
                next_btn.click()
                time.sleep(1)
            except Exception:
                print("    Достигнут конец, дальше страниц нет")
                break

    except Exception as e:
        print(f"[!] Ошибка: {e}")
        raise
    finally:
        driver.quit()

    print(f"[+] Всего собрано {len(all_quotes)} цитат")
    return all_quotes


@app.get("/")
async def root():
    return {
        "service": "Quotes Parser API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "Информация об API",
            "GET /parse?url=URL": "Запустить парсинг сайта",
            "GET /get-data": "Получить все цитаты из БД",
            "GET /stats": "Получить статистику",
            "GET /docs": "Документация API (Swagger)",
        },
        "example": "curl 'http://127.0.0.1:8000/parse?url=http://quotes.toscrape.com'",
    }


@app.get("/parse")
async def parse_endpoint(url: str = Query(..., description="URL сайта для парсинга")):
    try:
        print(f"\n[>] Поступил запрос на парсинг: {url}")

        quotes = parse_all_pages(url, max_pages=5)
        save_quotes_to_db(quotes, url)

        print(f"[+] Готово! Спарсено {len(quotes)} цитат\n")

        return {
            "status": "success",
            "message": f"Успешно спарсено {len(quotes)} цитат",
            "url": url,
            "quotes_count": len(quotes),
        }

    except Exception as e:
        print(f"[!] Ошибка: {e}\n")
        return {"status": "error", "message": f"Ошибка при парсинге: {str(e)}"}


@app.get("/get-data")
async def get_data_endpoint():
    try:
        quotes = get_all_quotes()
        print(f"[+] Отдал {len(quotes)} цитат из БД")

        return JSONResponse(
            content={"status": "success", "count": len(quotes), "data": quotes}
        )

    except Exception as e:
        print(f"[!] Ошибка при получении данных: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Ошибка при получении данных: {str(e)}",
            },
        )


@app.get("/stats")
async def get_stats():
    try:
        total_quotes = get_quotes_count()
        print(f"[+] Статистика: в БД {total_quotes} цитат")

        return {
            "status": "success",
            "statistics": {"total_quotes_in_db": total_quotes, "status": "active"},
        }

    except Exception as e:
        print(f"[!] Ошибка: {e}")
        return JSONResponse(
            status_code=500, content={"status": "error", "message": f"Ошибка: {str(e)}"}
        )


if __name__ == "__main__":
    print("\nЗапуск Quotes Parser API")
    print("Документация: http://127.0.0.1:8000/docs")
    print("Сервер на http://127.0.0.1:8000\n")

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
