#!/bin/bash

# Bu script'in bulunduğu dizine (yani project_root'a) git
# Bu, 'ModuleNotFoundError' hatasını engeller
cd "$(dirname "$0")"

echo "========================================="
echo " Flask Web Sunucusu (Dashboard) başlatılıyor..."
echo "========================================="
echo "Tarayıcınızda http://127.0.0.1:5001/ adresini açabilirsiniz."
echo "Bu pencereyi kapattığınızda sunucu durur."
echo ""

# Web sunucusunu başlat
python3 app.py

# Hata verirse veya sunucu durursa pencere hemen kapanmasın
echo ""
echo "Sunucu durduruldu."
read -p "Kapatmak için Enter'a basın..."
