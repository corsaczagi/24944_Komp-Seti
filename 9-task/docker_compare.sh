#!/bin/bash

echo "Создаём контейнеры"
docker run -dit --name test1 ubuntu:22.04 sleep infinity
docker run -dit --name test2 ubuntu:22.04 sleep infinity

echo "Установка ping..."
docker exec test1 apt update -qq 2>/dev/null
docker exec test1 apt install -y -qq iputils-ping 2>/dev/null
docker exec test2 apt update -qq 2>/dev/null
docker exec test2 apt install -y -qq iputils-ping tcpdump 2>/dev/null
echo ""

echo "-------- Получение IP адресов --------"
IP4_2=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' test2)
IP6_2=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.GlobalIPv6Address}}{{end}}' test2)

echo "IPv4 адрес test2: $IP4_2"
echo "IPv6 адрес test2: $IP6_2"
echo ""

# IPv4 тест
if [ -n "$IP4_2" ]; then
    echo "-------- IPv4 Пинг ----------"
    docker exec test1 ping -c 2 $IP4_2
else
    echo "IPv4 НЕ НАЙДЕН"
fi

# IPv6 тест
if [ -n "$IP6_2" ] && [ "$IP6_2" != "null" ]; then
    echo ""
    echo "---------- IPv6 Пинг -----------"
    docker exec test1 ping -6 -c 2 $IP6_2
    echo ""
    docker exec test2 tcpdump -i eth0 -c 1 -v ip6 2>&1 | grep -E "(IP6|hlim|length)" | head -5
else
    echo "IPv6 НЕ НАЙДЕН"
fi

# Очистка
docker rm -f test1 test2 >/dev/null
echo ""
echo "Завершено"