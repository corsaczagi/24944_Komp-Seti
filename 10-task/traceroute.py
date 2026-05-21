#!/usr/bin/env python3
import subprocess
import csv
import sys


DOMAINS = {
    "google.com": {
        "ipv4": [
            "173.194.221.113",
            "173.194.221.138",
            "173.194.221.101",
            "173.194.221.139",
            "173.194.221.100",
            "173.194.221.102",
        ],
        "ipv6": [],
    },
    "yandex.ru": {"ipv4": ["77.88.44.55", "5.255.255.77", "77.88.55.88"], "ipv6": []},
    "github.com": {"ipv4": ["140.82.121.4"], "ipv6": []},
    "gmail.com": {
        "ipv4": ["64.233.164.19", "64.233.164.17", "64.233.164.83", "64.233.164.18"],
        "ipv6": [],
    },
    "avito.ru": {
        "ipv4": [
            "87.250.250.242",
            "87.250.250.243",
            "87.250.250.244",
            "87.250.250.245",
        ],
        "ipv6": [],
    },
    "reddit.com": {
        "ipv4": [
            "151.101.1.140",
            "151.101.65.140",
            "151.101.129.140",
            "151.101.193.140",
        ],
        "ipv6": [],
    },
}


def get_final_destination(ip):
    try:
        cmd = [
            "sudo",
            "traceroute",
            "-4",
            "-T",
            "-p",
            "80",
            "-n",
            "-q",
            "1",
            "-w",
            "1",
            ip,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        last_hop = None
        for line in result.stdout.strip().split("\n"):
            if line and line[0].isdigit():
                parts = line.split()
                hop_num = parts[0]
                hop_ip = parts[1] if len(parts) > 1 else "*"
                rtt = parts[2] if len(parts) > 2 else "*"
                last_hop = [hop_num, hop_ip, rtt]

        if last_hop and last_hop[1] == ip:
            return [last_hop[0], last_hop[1], last_hop[2]]
        else:
            return ["-", "-", "not_reached"]
    except Exception:
        return ["-", "-", "error"]


def main():
    all_results = []
    total_ips = 0
    successful = 0
    failed = 0

    for domain, ips in DOMAINS.items():
        for ip in ips["ipv4"]:
            total_ips += 1
            hop = get_final_destination(ip)

            if hop[2] not in ["not_reached", "error"]:
                successful += 1
            else:
                failed += 1

            all_results.append([domain, "IPv4", ip, hop[0], hop[1], hop[2]])

    with open("dns_traceroute_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["domain", "ip_type", "ip_address", "hop", "hop_ip", "status"])
        writer.writerows(all_results)

    print("РЕЗУЛЬТАТЫ:")
    print(f"  Успешно сохранено в файл: dns_traceroute_results.csv")
    print(f"  Всего IP-адресов: {total_ips}")
    print(f"  Успешных: {successful}")
    print(f"  Неудачных: {failed}")


if __name__ == "__main__":
    main()
