#!/bin/bash

# Bu script'in bulunduğu dizine (yani project_root'a) git
cd "$(dirname "$0")"

# Proje kök dizininin tam yolunu bir değişkene kaydet
PROJECT_ROOT=$(pwd)

echo "========================================="
echo "👁️ Ağ Sniffer'ı (Paket Yakalayıcı) başlatılıyor..."
echo "========================================="
echo "Ağ trafiğini dinlemek için Yönetici (sudo) şifreniz istenecek."
echo "Proje Yolu: $PROJECT_ROOT"
echo ""

# Python 3'ün tam yolunu bul
PYTHON_PATH=$(which python3)

# --- YENİ (Düzeltilmiş Komut V2) ---
# 'export' komutu 'osascript' tarafından yok sayıldı.
# Yeni Yöntem: PYTHONPATH'i doğrudan komutun başına ekle.
# Bu, 'sudo' altında bile Python'un 'core' modülünü bulmasını garanti eder.
COMMAND_TO_RUN="PYTHONPATH='$PROJECT_ROOT' $PYTHON_PATH -m core.sniffer"

# macOS'ta bir komutu 'sudo' ile çalıştırmak için AppleScript kullan
osascript -e "do shell script \"$COMMAND_TO_RUN\" with administrator privileges"

# Eğer kullanıcı şifreyi iptal ederse veya hata olursa
if [ $? -ne 0 ]; then
    echo ""
    echo "[HATA] Sniffer başlatılamadı. Şifre yanlış girildi, 'İptal'e basıldı veya bir Python hatası oluştu."
    echo "Python Hatası (eğer varsa) yukarıda görünmelidir."
    read -p "Kapatmak için Enter'a basın..."
fi
