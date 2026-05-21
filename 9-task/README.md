#  Настройка IPv6 и сравнение пакетов IPv4/IPv6

## Требования к окружению
- **ОС**: Ubuntu 20.04/22.04/24.04
- **Docker**: установлен и запущен
- **Права**: пользователь в группе `docker`

### Включение IPv6 в Docker (если не настроен):
```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<EOF
{
  "ipv6": true,
  "fixed-cidr-v6": "2001:db8:1::/64"
}
EOF
sudo systemctl restart docker
```
### Запуск:
``` bash
chmod +x docker_compare.sh
./docker_compare.sh
```

### Вывод
``` bash
Создаём контейнеры
32cd82feafee6e124f74d9406f2c00e7aafaa69262735752321bbfea3653e435
e40752bbc071c4e24533c9a9bdb9d34461a8bd4cf08bf09a0255982b55103647
Установка ping...
1 package can be upgraded. Run 'apt list --upgradable' to see it.
The following additional packages will be installed:
  libcap2-bin libpam-cap
The following NEW packages will be installed:
  iputils-ping libcap2-bin libpam-cap
0 upgraded, 3 newly installed, 0 to remove and 1 not upgraded.
Need to get 77.0 kB of archives.
After this operation, 280 kB of additional disk space will be used.
Selecting previously unselected package libcap2-bin.
(Reading database ... 4393 files and directories currently installed.)
Preparing to unpack .../libcap2-bin_1%3a2.44-1ubuntu0.22.04.3_amd64.deb ...
Unpacking libcap2-bin (1:2.44-1ubuntu0.22.04.3) ...
Selecting previously unselected package iputils-ping.
Preparing to unpack .../iputils-ping_3%3a20211215-1ubuntu0.1_amd64.deb ...
Unpacking iputils-ping (3:20211215-1ubuntu0.1) ...
Selecting previously unselected package libpam-cap:amd64.
Preparing to unpack .../libpam-cap_1%3a2.44-1ubuntu0.22.04.3_amd64.deb ...
Unpacking libpam-cap:amd64 (1:2.44-1ubuntu0.22.04.3) ...
Setting up libcap2-bin (1:2.44-1ubuntu0.22.04.3) ...
Setting up libpam-cap:amd64 (1:2.44-1ubuntu0.22.04.3) ...
debconf: unable to initialize frontend: Dialog
debconf: (TERM is not set, so the dialog frontend is not usable.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (Can't locate Term/ReadLine.pm in @INC (you may need to install the Term::ReadLine module) (@INC contains: /etc/perl /usr/local/lib/x86_64-linux-gnu/perl/5.34.0 /usr/local/share/perl/5.34.0 /usr/lib/x86_64-linux-gnu/perl5/5.34 /usr/share/perl5 /usr/lib/x86_64-linux-gnu/perl-base /usr/lib/x86_64-linux-gnu/perl/5.34 /usr/share/perl/5.34 /usr/local/lib/site_perl) at /usr/share/perl5/Debconf/FrontEnd/Readline.pm line 7.)
debconf: falling back to frontend: Teletype
Setting up iputils-ping (3:20211215-1ubuntu0.1) ...
1 package can be upgraded. Run 'apt list --upgradable' to see it.
The following additional packages will be installed:
  dbus libapparmor1 libcap2-bin libdbus-1-3 libexpat1 libpam-cap libpcap0.8
Suggested packages:
  default-dbus-session-bus | dbus-session-bus apparmor
The following NEW packages will be installed:
  dbus iputils-ping libapparmor1 libcap2-bin libdbus-1-3 libexpat1 libpam-cap
  libpcap0.8 tcpdump
0 upgraded, 9 newly installed, 0 to remove and 1 not upgraded.
Need to get 1202 kB of archives.
After this operation, 3735 kB of additional disk space will be used.
Selecting previously unselected package libapparmor1:amd64.
(Reading database ... 4393 files and directories currently installed.)
Preparing to unpack .../0-libapparmor1_3.0.4-2ubuntu2.5_amd64.deb ...
Unpacking libapparmor1:amd64 (3.0.4-2ubuntu2.5) ...
Selecting previously unselected package libdbus-1-3:amd64.
Preparing to unpack .../1-libdbus-1-3_1.12.20-2ubuntu4.1_amd64.deb ...
Unpacking libdbus-1-3:amd64 (1.12.20-2ubuntu4.1) ...
Selecting previously unselected package libexpat1:amd64.
Preparing to unpack .../2-libexpat1_2.4.7-1ubuntu0.7_amd64.deb ...
Unpacking libexpat1:amd64 (2.4.7-1ubuntu0.7) ...
Selecting previously unselected package dbus.
Preparing to unpack .../3-dbus_1.12.20-2ubuntu4.1_amd64.deb ...
Unpacking dbus (1.12.20-2ubuntu4.1) ...
Selecting previously unselected package libcap2-bin.
Preparing to unpack .../4-libcap2-bin_1%3a2.44-1ubuntu0.22.04.3_amd64.deb ...
Unpacking libcap2-bin (1:2.44-1ubuntu0.22.04.3) ...
Selecting previously unselected package iputils-ping.
Preparing to unpack .../5-iputils-ping_3%3a20211215-1ubuntu0.1_amd64.deb ...
Unpacking iputils-ping (3:20211215-1ubuntu0.1) ...
Selecting previously unselected package libpam-cap:amd64.
Preparing to unpack .../6-libpam-cap_1%3a2.44-1ubuntu0.22.04.3_amd64.deb ...
Unpacking libpam-cap:amd64 (1:2.44-1ubuntu0.22.04.3) ...
Selecting previously unselected package libpcap0.8:amd64.
Preparing to unpack .../7-libpcap0.8_1.10.1-4ubuntu1.22.04.1_amd64.deb ...
Unpacking libpcap0.8:amd64 (1.10.1-4ubuntu1.22.04.1) ...
Selecting previously unselected package tcpdump.
Preparing to unpack .../8-tcpdump_4.99.1-3ubuntu0.2_amd64.deb ...
Unpacking tcpdump (4.99.1-3ubuntu0.2) ...
Setting up libexpat1:amd64 (2.4.7-1ubuntu0.7) ...
Setting up libapparmor1:amd64 (3.0.4-2ubuntu2.5) ...
Setting up libcap2-bin (1:2.44-1ubuntu0.22.04.3) ...
Setting up libdbus-1-3:amd64 (1.12.20-2ubuntu4.1) ...
Setting up dbus (1.12.20-2ubuntu4.1) ...
Setting up libpam-cap:amd64 (1:2.44-1ubuntu0.22.04.3) ...
debconf: unable to initialize frontend: Dialog
debconf: (TERM is not set, so the dialog frontend is not usable.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (Can't locate Term/ReadLine.pm in @INC (you may need to install the Term::ReadLine module) (@INC contains: /etc/perl /usr/local/lib/x86_64-linux-gnu/perl/5.34.0 /usr/local/share/perl/5.34.0 /usr/lib/x86_64-linux-gnu/perl5/5.34 /usr/share/perl5 /usr/lib/x86_64-linux-gnu/perl-base /usr/lib/x86_64-linux-gnu/perl/5.34 /usr/share/perl/5.34 /usr/local/lib/site_perl) at /usr/share/perl5/Debconf/FrontEnd/Readline.pm line 7.)
debconf: falling back to frontend: Teletype
Setting up iputils-ping (3:20211215-1ubuntu0.1) ...
Setting up libpcap0.8:amd64 (1.10.1-4ubuntu1.22.04.1) ...
Setting up tcpdump (4.99.1-3ubuntu0.2) ...
Processing triggers for libc-bin (2.35-0ubuntu3.13) ...

-------- Получение IP адресов --------
IPv4 адрес test2: 172.17.0.3
IPv6 адрес test2: 2001:db8:1::3

-------- IPv4 Пинг ----------
PING 172.17.0.3 (172.17.0.3) 56(84) bytes of data.
64 bytes from 172.17.0.3: icmp_seq=1 ttl=64 time=0.103 ms
64 bytes from 172.17.0.3: icmp_seq=2 ttl=64 time=0.160 ms

--- 172.17.0.3 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1048ms
rtt min/avg/max/mdev = 0.103/0.131/0.160/0.028 ms

---------- IPv6 Пинг -----------
PING 2001:db8:1::3(2001:db8:1::3) 56 data bytes
64 bytes from 2001:db8:1::3: icmp_seq=1 ttl=64 time=0.113 ms
64 bytes from 2001:db8:1::3: icmp_seq=2 ttl=64 time=0.143 ms

--- 2001:db8:1::3 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1041ms
rtt min/avg/max/mdev = 0.113/0.128/0.143/0.015 ms

tcpdump: listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
08:35:58.939559 IP6 (hlim 255, next-header ICMPv6 (58) payload length: 32) fe80::5cbb:82ff:fe0c:6570 > fe80::40e0:78ff:fe3b:99ea: [icmp6 sum ok] ICMP6, neighbor solicitation, length 32, who has fe80::40e0:78ff:fe3b:99ea
          source link-address option (1), length 8 (1): 5e:bb:82:0c:65:70

Завершено
```

### Сравнение IPv6 и IPv4

| Параметр | IPv4 | IPv6 |
|----------|------|------|
| **IP-адрес контейнера** | 172.17.0.3 | 2001:db8:1::3 |
| **Формат адреса** | Десятичный | Шестнадцатеричный |
| **Поле TTL/Hop Limit** | `ttl=64` | `hlim=255` |
| **Размер заголовка** | 28 байт | 40 байт |
| **Контрольная сумма** | Есть | **Отсутствует** |
| **Определение соседей** | ARP | NDP (ICMPv6) |