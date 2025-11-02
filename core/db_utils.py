import psycopg2  # 1. DEĞİŞİKLİK: 'sqlite3' yerine 'psycopg2' import edildi
import psycopg2.extras # 5. DEĞİŞİKLİK: Veriyi sözlük (dict) olarak çekmek için
from datetime import datetime, timedelta
from config.config import POSTGRES_DB  # 2. DEĞİŞİKLİK: 'POSTGRES_DB' import edildi

# 3. DEĞİŞİKLİK: 'DB_PATH' satırı silindi (artık config'den geliyor)


# (HAFTA 4 GÜNCELLEMESİ)
def get_connection():
    """
    PostgreSQL bağlantısı alır ve 'events' tablosunu (yoksa) garanti eder.
    (Hafta 4: Tehdit istihbaratı sütunları eklendi)
    """
    try:
        # 4. DEĞİŞİKLİK: Bağlantı metodu Postgres'e göre güncellendi
        conn = psycopg2.connect(**POSTGRES_DB)
        
        # 'logger.py' ile aynı mantık: OKUYUCU da tablo yoksa oluşturabilmeli.
        with conn.cursor() as cur:
            # (HAFTA 4 GÜNCELLEMESİ): abuse_score ve is_known_bad sütunları eklendi
            cur.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id SERIAL PRIMARY KEY,
                    timestamp TEXT,
                    source_ip TEXT,
                    dest_ip TEXT,
                    dest_port INTEGER,
                    protocol TEXT,
                    details TEXT,
                    abuse_score INTEGER DEFAULT 0,
                    is_known_bad BOOLEAN DEFAULT FALSE
                )
            ''')
        conn.commit() # CREATE TABLE işlemini onayla
        
        return conn
        
    except psycopg2.Error as e:
        print(f"[DB_UTILS HATA] PostgreSQL bağlantısı kurulamadı: {e}")
        # Hata olursa Flask'ın patlaması için hatayı yükselt
        raise e

    

# --- 2. Hafta Sorguları (Güncellendi) ---

def get_top_ports(last_hours=1, limit=5):
    """
    Son X saatte en çok hangi portlara bağlantı olmuş?
    """
    since = datetime.utcnow() - timedelta(hours=last_hours)
    
    query = """
        SELECT dest_port, COUNT(*) as count
        FROM events
        WHERE timestamp >= %s
        GROUP BY dest_port
        ORDER BY count DESC
        LIMIT %s
    """
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (since.isoformat(), limit))
            return cur.fetchall()


def get_activities_by_ip(ip):
    """
    Belirli bir IP'den gelen tüm aktiviteler.
    Returns: list of dict
    """
    query = "SELECT * FROM events WHERE source_ip = %s ORDER BY timestamp DESC"
    
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (ip,))
            return cur.fetchall()


# (HAFTA 4 GÜNCELLEMESİ)
def get_recent_dns_queries(last_hours=1, limit=10):
    """
    Son X saatteki DNS sorguları.
    (Hafta 4: Yeni skor sütunları eklendi)
    """
    since = datetime.utcnow() - timedelta(hours=last_hours)
    
    # YENİ: Sorguya 'abuse_score' ve 'is_known_bad' eklendi
    query = """
        SELECT timestamp, source_ip, dest_ip, details, abuse_score, is_known_bad
        FROM events
        WHERE protocol = 'DNS' AND timestamp >= %s
        ORDER BY timestamp DESC
        LIMIT %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (since.isoformat(), limit))
            return cur.fetchall()


# (HAFTA 4 GÜNCELLEMESİ)
def get_http_leaks(last_hours=1, limit=10):
    """
    Son X saatte HTTP üzerinden şifresiz veri sızmaları.
    (Hafta 4: Yeni skor sütunları eklendi)
    """
    since = datetime.utcnow() - timedelta(hours=last_hours)
    
    # YENİ: Sorguya 'abuse_score' ve 'is_known_bad' eklendi
    query = """
        SELECT timestamp, source_ip, dest_ip, details, abuse_score, is_known_bad
        FROM events
        WHERE protocol = 'HTTP' AND details LIKE 'Leak:%%' AND timestamp >= %s
        ORDER BY timestamp DESC
        LIMIT %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (since.isoformat(), limit))
            return cur.fetchall()

# --- YENİ (Dashboard Geliştirmesi) ---

def get_suspicious_ports(last_hours=1, limit=10):
    """
    Son X saatteki "Şüpheli Port" (Kırmızı Alarm) olaylarını getirir.
    """
    since = datetime.utcnow() - timedelta(hours=last_hours)
    
    # 'analyzer.py' tarafından kaydedilen 'Suspicious port syn' olaylarını arıyoruz
    # ve 'dest_port' bilgisini de alıyoruz.
    query = """
        SELECT timestamp, source_ip, dest_ip, dest_port, details, abuse_score, is_known_bad
        FROM events
        WHERE protocol = 'TCP' AND details = 'Suspicious port syn' AND timestamp >= %s
        ORDER BY timestamp DESC
        LIMIT %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (since.isoformat(), limit))
            return cur.fetchall()