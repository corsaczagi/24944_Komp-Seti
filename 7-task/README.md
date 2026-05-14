# Задание 7: Гео-блокировка российских IP

## Файлы в папке
- `nginx.conf` — конфиг nginx с geoip и блокировкой RU
- `blocked.html` — страница-заглушка
- `main.py`, `database.py`, `Dockerfile`, `requirements.txt` — само приложение

## Как работает блокировка
- nginx проверяет страну по IP через GeoIP
- Если IP из России (`RU`) → возвращает `403` и страницу `blocked.html`
- Для отладки добавлена локальная проверка (`127.0.0.1`), чтобы видеть заглушку на своём компьютере

## Установка GeoIP (один раз)
```bash
sudo apt update && sudo apt install geoip-database -y