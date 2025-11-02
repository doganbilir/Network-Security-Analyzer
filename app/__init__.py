from flask import Flask

# Flask uygulamasını (motoru) oluştur
# 'app' adını veriyoruz, çünkü run_web.py bu isimle arayacak
app = Flask(__name__)

# ÖNEMLİ:
# Uygulamayı oluşturduktan sonra, bu uygulamayı kullanacak olan
# rota (routes) dosyamızı import ediyoruz.
# Python'un döngüsel import (circular import) hatası vermemesi
# için bu import'un 'app' tanımlandıktan SONRA yapılması gerekir.
from app import routes