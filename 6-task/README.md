# Задание 6: Проксирование

## Конфиг nginx
Файл `nginx.conf` содержит настройки проксирования порта 80 на порт 8080.

## Запуск
```bash
docker start postgres_db quotes_app
sudo cp nginx.conf /etc/nginx/sites-available/default
sudo systemctl restart nginx
curl "http://127.0.0.1/parse?url=http://quotes.toscrape.com"
```