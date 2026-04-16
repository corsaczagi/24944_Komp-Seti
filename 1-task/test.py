import csv
import subprocess
import re


domains = [
    "google.com",
    "yandex.ru",
    "vk.com",
    "github.com",
    "wikipedia.org",
    "amazon.com",
    "microsoft.com",
    "cloudflare.com",
    "openai.com",
    "bbc.co.uk",
]
output_file = "ping_results.csv"
ping_count = 4


def ping_domain(domain):
    print(f"пингую - {domain}")
    try:
        result = subprocess.run(
            ["ping", "-c", str(ping_count), domain],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10,
        )

        output = result.stdout

        # Ищем процент потерь
        loss_match = re.search(r"(\d+)% packet loss", output)
        packet_loss = loss_match.group(1) if loss_match else "100"

        # Ищем среднее время
        avg_match = re.search(r"min/avg/max.*?([\d.]+)/([\d.]+)/([\d.]+)", output)
        if avg_match:
            rtt_min, rtt_avg, rtt_max = avg_match.groups()
        else:
            rtt_min = rtt_avg = rtt_max = "0"

        return {
            "Домен": domain,
            "Средний RTT (мс)": rtt_avg,
            "Мин RTT (мс)": rtt_min,
            "Макс RTT (мс)": rtt_max,
            "Потеря пакетов (%)": packet_loss,
        }

    except Exception:
        print(f"{domain} не отвечает")
        return {
            "Домен": domain,
            "Средний RTT (мс)": "0",
            "Мин RTT (мс)": "0",
            "Макс RTT (мс)": "0",
            "Потеря пакетов (%)": "100",
        }


with open(output_file, "w", newline="", encoding="utf-8") as CSV_file:
    field_names = ["Домен", "Средний RTT", "Min RTT", "Max RTT", "Потеря пакетов (%)"]
    writer = csv.DictWriter(CSV_file, fieldnames=field_names)
    writer.writeheader()

    results = []
    for domain in domains:
        data = ping_domain(domain)
        writer.writerow(data)
        results.append(data)

print("результат сохранен в файл")
