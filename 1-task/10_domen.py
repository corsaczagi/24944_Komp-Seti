import subprocess
import csv
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
    "bbc.co.uk"
]

PING_COUNT = 5
OUTPUT_FILE = "ping_results.csv"

def ping_domain(domain):
    try:
        result = subprocess.run(
            ["ping", "-c", str(PING_COUNT), domain],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        output = result.stdout

        # packet loss
        loss_match = re.search(r"(\d+)% packet loss", output)
        packet_loss = loss_match.group(1) if loss_match else "100"

        # RTT stats
        rtt_match = re.search(
            r"min/avg/max/(?:mdev|stddev) = ([\d.]+)/([\d.]+)/([\d.]+)",
            output
        )

        if rtt_match:
            rtt_min, rtt_avg, rtt_max = rtt_match.groups()
        else:
            rtt_min = rtt_avg = rtt_max = ""

        return {
            "domain": domain,
            "RTT_avg_ms": rtt_avg,
            "RTT_min_ms": rtt_min,
            "RTT_max_ms": rtt_max,
            "packet_loss_pct": packet_loss
        }

    except Exception:
        return {
            "domain": domain,
            "RTT_avg_ms": "",
            "RTT_min_ms": "",
            "RTT_max_ms": "",
            "packet_loss_pct": "100"
        }


with open(OUTPUT_FILE, "w", newline="") as csvfile:
    fieldnames = [
        "domain",
        "RTT_avg_ms",
        "RTT_min_ms",
        "RTT_max_ms",
        "packet_loss_pct"
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for domain in domains:
        data = ping_domain(domain)
        writer.writerow(data)
        print(f"Pinged {domain}")

print(f"\nResults saved to {OUTPUT_FILE}")