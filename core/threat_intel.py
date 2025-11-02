# core/threat_intel.py
# YENİ DOSYA (Hafta 4 - Tehdit İstihbaratı)

import requests
import time
from config.config import ABUSEIPDB_API_KEY # config'den API anahtarını al

# --- Akıllı Önbellek (Cache) ---
# Bu sözlük, API limitlerimizi koruyacak.
# Format: {'1.2.3.4': {'score': 90, 'timestamp': 1678886400}}
IP_CACHE = {}
CACHE_DURATION_SECONDS = 3600 # 1 saat (3600 saniye)
# --------------------------------

def _check_api(ip: str):
    """
    AbuseIPDB API'sine IP adresini sorgular.
    Bu fonksiyon SADECE önbellekte olmayan IP'ler için çağrılır.
    """
    print(f"[THREAT INTEL] API'ye soruluyor: {ip}", flush=True)
    
    try:
        response = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
            params={
                'ipAddress': ip,
                'verbose': False
            },
            headers={
                'Accept': 'application/json',
                'Key': ABUSEIPDB_API_KEY # config'den gelen anahtar
            }
        )
        
        response.raise_for_status() # 4xx veya 5xx hata kodu varsa hata fırlat
        data = response.json()
        
        # API'den gelen skoru al (eğer IP hiç raporlanmamışsa 'data' boş gelebilir)
        score = data.get('data', {}).get('abuseConfidenceScore', 0)
        
        return score

    except requests.exceptions.RequestException as e:
        print(f"[HATA][THREAT INTEL] AbuseIPDB API sorgusu başarısız: {e}", flush=True)
        # API hatası olursa, sistemi yavaşlatmamak için 0 (güvenli) dön
        return 0
    except Exception as e:
        print(f"[HATA][THREAT INTEL] API yanıtı işlenirken hata: {e}", flush=True)
        return 0


def get_ip_reputation(ip: str):
    """
    Bir IP'nin "saldırı skorunu" döner.
    API limitlerini korumak için akıllı önbellek (cache) kullanır.
    
    Returns:
        (int): 0-100 arası skor
        (bool): Skora göre "kötü" olup olmadığı
    """
    
    # 1. Adım: IP önbellekte var mı?
    current_time = time.time()
    if ip in IP_CACHE:
        cache_entry = IP_CACHE[ip]
        
        # 2. Adım: Kayıt taze mi? (örn: 1 saatten yeni mi?)
        if (current_time - cache_entry['timestamp']) < CACHE_DURATION_SECONDS:
            # print(f"[THREAT INTEL] Önbellekten bulundu (Taze): {ip}", flush=True) # (Debug için)
            score = cache_entry['score']
            is_bad = score > 80 # Örnek eşik: 80'den yüksekse "kötü" say
            return score, is_bad

    # 3. Adım: Önbellekte yoksa veya kayıt eskiyse, API'ye sor
    # (Not: localhost, broadcast veya özel ağ IP'lerini sorgulamayalım)
    if ip.startswith('127.') or ip.startswith('192.168.') or ip.startswith('10.') or ip == '255.255.255.255':
        return 0, False # Bu IP'ler için API'ye gitme, 0 dön

    # API'ye sor
    score = _check_api(ip)
    
    # 4. Adım: Sonucu önbelleğe kaydet
    IP_CACHE[ip] = {
        'score': score,
        'timestamp': current_time # Yeni damga
    }
    
    is_bad = score > 80 # Eşik
    return score, is_bad