#!/bin/bash

# AbuseIPDB API dokümantasyonunda 100 skora sahip olduğu bilinen IP
BAD_IP="89.222.119.23"
# config.py'de şüpheli olarak işaretli portlardan biri
SUSPICIOUS_PORT=23

echo "[TEST] Bilinen Kötü IP'ye ($BAD_IP) Şüpheli Port ($SUSPICIOUS_PORT) testi gönderiliyor..."
echo "Sniffer terminalini ve Dashboard'u kontrol et!"

# -v (verbose) -z (zero-I/O mode, sadece SYN gönderir) -w 1 (1 saniye timeout)
# Bu komut, nc'nin tam bir bağlantı kurmadan sadece SYN paketi atmasını sağlar.
nc -v -z -w 1 $BAD_IP $SUSPICIOUS_PORT

echo "[TEST] Tamamlandı."
