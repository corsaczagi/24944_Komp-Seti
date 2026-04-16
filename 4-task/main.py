import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from typing import List, Optional


DATABASE_URL = "postgresql://quote_user:quotes123@localhost:5432/quotes_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True)
    quote = Column(Text, nullable=False)
    author = Column(String(255), nullable=False)
    tags = Column(Text)
    tags_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


class QuoteResponse(BaseModel):
    id: int
    quote: str
    author: str
    tags: str
    tags_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class ParseResponse(BaseModel):
    status: str
    message: str
    quotes_count: int


def parse_quotes(url: str, max_pages: int) -> list:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    quotes_data = []
    try:
        driver.get(url)
        for _ in range(max_pages):
            for q in driver.find_elements(By.CSS_SELECTOR, "div.quote"):
                tags = [t.text for t in q.find_elements(By.CSS_SELECTOR, "a.tag")]
                quotes_data.append(
                    {
                        "quote": q.find_element(By.CSS_SELECTOR, "span.text").text,
                        "author": q.find_element(By.CSS_SELECTOR, "small.author").text,
                        "tags": ", ".join(tags),
                        "tags_count": len(tags),
                    }
                )
            try:
                driver.find_element(By.CSS_SELECTOR, "li.next > a").click()
                time.sleep(1)
            except:
                break
    finally:
        driver.quit()
    return quotes_data


def save_quotes(quotes: list):
    db = SessionLocal()
    for q in quotes:
        if not db.query(Quote).filter(Quote.quote == q["quote"]).first():
            db.add(Quote(**q))
    db.commit()
    db.close()


app = FastAPI()


@app.post("/parse")
async def parse(url: str = Query(...), max_pages: int = Query(5)) -> ParseResponse:
    if not url.startswith(("http://", "https://")):
        raise HTTPException(400, "URL должен начинаться с http:// или https://")
    quotes = parse_quotes(url, max_pages)
    if quotes:
        save_quotes(quotes)
    return ParseResponse(
        status="success",
        message=f"Сохранено {len(quotes)} цитат",
        quotes_count=len(quotes),
    )


@app.get("/quotes")
async def get_quotes(
    limit: int = 50, offset: int = 0, author: Optional[str] = None
) -> List[QuoteResponse]:
    db = SessionLocal()
    q = db.query(Quote)
    if author:
        q = q.filter(Quote.author.ilike(f"%{author}%"))
    result = q.order_by(Quote.created_at.desc()).offset(offset).limit(limit).all()
    db.close()
    return result


@app.get("/quotes/{id}")
async def get_quote(id: int) -> QuoteResponse:
    db = SessionLocal()
    quote = db.query(Quote).filter(Quote.id == id).first()
    db.close()
    if not quote:
        raise HTTPException(404, "Цитата не найдена")
    return quote


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
