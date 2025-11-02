from datetime import datetime
import psycopg2  # 1. DEĞİŞİKLİK: 'sqlite3' yerine 'psycopg2' import edildi
from config.config import LOG_FILE, POSTGRES_DB  # 2. DEĞİŞİKLİK: 'POSTGRES_DB' import edildi

# 3. DEĞİŞİKLİK: 'DB_PATH' satırı silindi (artık config'den geliyor)

def append_dns_log(domain: str):
    # Bu fonksiyon veritabanına dokunmadığı için DEĞİŞİKLİK YOK
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} {domain}\n")

# Basit postgresql insert örneği
# (HAFTA 4 GÜNCELLEMESİ)
def insert_event(
    src, 
    dst, 
    dport, 
    proto, 
    details="", 
    abuse_score=0,      # YENİ (Hafta 4)
    is_known_bad=False, # YENİ (Hafta 4)
    conn=None
):
    """
    Olayları PostgreSQL'e kaydeder.
    (Hafta 4: Tehdit istihbaratı sütunları eklendi)
    """
    close_conn = False
    cur = None  # 9. DEĞİŞİKLİK: 'cur' değişkenini 'finally' bloğu için dışarıda tanımla
    
    try:
        if conn is None:
            # 4. DEĞİŞİKLİK: Bağlantı metodu Postgres'e göre güncellendi
            # config.py'daki POSTGRES_DB sözlüğünü kullanır
            conn = psycopg2.connect(**POSTGRES_DB)
            close_conn = True
        
        # 5. DEĞİŞİKLİK: 'conn.execute('PRAGMA...WAL')' satırı silindi
        # (Bu, SQLite'a özel bir komuttu)
        
        cur = conn.cursor()
        
        # 6. DEĞİŞİKLİK (Hafta 4 GÜNCELLEMESİ): 
        # abuse_score ve is_known_bad sütunları eklendi
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
        
        # 7. DEĞİŞİKLİK (Hafta 4 GÜNCELLEMESİ): 
        # Yeni sütunlar INSERT'e eklendi
        cur.execute('''
            INSERT INTO events (
                timestamp, source_ip, dest_ip, dest_port, protocol, details, 
                abuse_score, is_known_bad
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ''', (
            datetime.utcnow().isoformat(), src, dst, dport, proto, details,
            abuse_score, is_known_bad  # YENİ (Hafta 4)
        ))
        
        conn.commit()
        
    except psycopg2.Error as e:
        # 8. DEĞİŞİKLİK: Hata yönetimi eklendi (Bağlantı/Yazma hatası olursa)
        print(f"[LOGGER HATA] PostgreSQL'e yazılamadı: {e}")
        if conn:
            conn.rollback() # Hata olursa işlemi geri al
            
    finally:
        # 9. DEĞİŞİKLİK: Bağlantıyı ve cursor'ı kapatmak için 'finally' bloğu eklendi
        # Bu, bağlantıların açık kalmasını engeller
        if cur:
            cur.close()
        if close_conn and conn:
            conn.close()