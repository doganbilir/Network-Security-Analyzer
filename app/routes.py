# app/__init__.py dosyasında oluşturduğumuz 'app' nesnesini import et
from app import app
import traceback
# HTML sayfalarını göstermek için Flask'ın render_template aracını import et
from flask import render_template, request

# --- KÖPRÜ ---
# Projenin kök dizinindeki 'core' klasöründen,
# senin yazdığın 'db_utils.py' dosyasını 'db' adıyla import et.
import core.db_utils as db
# -------------

@app.route('/')
def index():
    """
    Ana sayfa (Dashboard) rotası.
    """
    try:
        # --- Zaman Aralığı Filtresi ---
        try:
            hours = request.args.get('hours', default=24, type=int)
        except ValueError:
            hours = 24
        # -------------------------------------

        # 1. VERİTABANINDAN VERİ ÇEK
        
        top_ports_data = db.get_top_ports(last_hours=hours, limit=5)
        recent_dns = db.get_recent_dns_queries(last_hours=hours, limit=10)
        recent_leaks = db.get_http_leaks(last_hours=hours, limit=10)
        recent_suspicious = db.get_suspicious_ports(last_hours=hours, limit=10)
        
        # --- YENİ (Grafik Geliştirmesi) ---
        # db_utils'dan gelen top_ports verisini (örn: [(80, 50), (23, 20)])
        # Chart.js'in anlayacağı 2 ayrı listeye böl:
        
        chart_labels = []
        chart_data = []
        if top_ports_data: # Veri varsa işle
            chart_labels = [f"Port {port}" for port, count in top_ports_data]
            chart_data = [count for port, count in top_ports_data]
        # -------------------------------------

        # 2. ÇEKTİĞİN BU VERİLERİ BİR HTML SAYFASINA GÖNDER
        return render_template(
            'index.html',
            # 'stats_top_ports'u artık kullanmayacağız, ama silmek sorun yaratmaz
            stats_top_ports=top_ports_data, 
            
            events_dns=recent_dns,
            events_leaks=recent_leaks,
            events_suspicious=recent_suspicious,
            active_hours=hours,
            
            # --- YENİ (Grafik Geliştirmesi) ---
            # Yeni, işlenmiş verileri HTML'e gönder:
            chart_labels=chart_labels,
            chart_data=chart_data
            # -------------------------------------
        )

    except Exception as e:
        # ... (Hata HTML'i değişmedi) ...
        print("[FLASK HATA] Veritabanı sorgusu başarısız:", flush=True)
        traceback.print_exc()
        return f"<h1>Dashboard yüklenemedi.</h1><pre>{str(e)}</pre>"