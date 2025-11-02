# core/analyzer.py
from scapy.all import IP, IPv6, TCP, UDP, Raw
from scapy.layers.dns import DNS, DNSQR
import config.config as cfg            # config dosyan proje kökünde: config/config.py
from core import logger, alert
import traceback

# YENİ (Hafta 4) - Tehdit istihbarat modülümüzü import et
from core import threat_intel

def get_ip_src(packet):
    if IP in packet:
        return packet[IP].src, packet[IP].dst
    elif IPv6 in packet:
        return packet[IPv6].src, packet[IPv6].dst
    return (None, None)

def _is_syn(packet):
    """SYN bitini daha güvenilir tespit et."""
    try:
        flags = packet[TCP].flags
        # flags farklı tipte gelebilir, bu nedenle hem bit maskesi hem string kontrolü ekliyoruz
        try:
            # scapy FlagsField -> int() dönüşümüyle bit maskesi kontrolü
            return (int(flags) & 0x02) != 0
        except Exception:
            return 'S' in str(flags)
    except Exception:
        return False

def process_packet(packet):
    """
    Her paketi işler:
      - DNS sorgularını logla
      - (Hafta 4): Şüpheli IP'leri API ile kontrol et ve zenginleştirilmiş logla
      - HTTP (port 80) üzerindeki RAW payload içinde anahtar kelime arayıp logla
    """

    # --- DNS ---
    # (Bu bloğu değiştirmedik, DNS sorgularını olduğu gibi logluyoruz)
    if DNSQR in packet:
        try:
            src_ip, dst_ip = get_ip_src(packet)
            domain = packet[DNSQR].qname.decode('utf-8', errors='ignore')
            print(f"[DNS Sorgusu] -> {domain}", flush=True)
            logger.append_dns_log(domain)
            # DNS olayları için API sorgusu yapmıyoruz (isteğe bağlı eklenebilir)
            logger.insert_event(src_ip, dst_ip, 53, "DNS", domain)
        except Exception:
            print("[DEBUG][analyzer][DNS] exception:", traceback.format_exc(), flush=True)
        return

    # --- TCP bazlı analizler ---
    if TCP in packet:
        try:
            src_ip, dst_ip = get_ip_src(packet)
            dport = packet[TCP].dport

            # debug: hangi TCP paketlerinin geldiğini gör
            print(f"[DEBUG] TCP paket: {src_ip} -> {dst_ip} :{dport} flags={packet[TCP].flags}", flush=True)

            # Şüpheli port (SYN kontrolü)
            if dport in cfg.SUSPICIOUS_PORTS and _is_syn(packet):
                
                # --- YENİ (Hafta 4) ---
                # Olayı loglamadan önce IP'nin sicilini kontrol et
                # Bu fonksiyon cache mekanizmalı, API limitimizi koruyacak
                print(f"[THREAT INTEL] Şüpheli port {dport} için {src_ip} sorgulanıyor...", flush=True)
                score, is_bad = threat_intel.get_ip_reputation(src_ip)
                # ---------------------

                # Uyarıyı ver (Bu fonksiyonu bir sonraki adımda skoru alacak şekilde güncelleyebiliriz)
                alert.print_suspicious_port(src_ip, dport)
                
                # --- GÜNCELLEME (Hafta 4) ---
                # Loglama fonksiyonuna yeni skor/durum bilgisini de gönder
                logger.insert_event(
                    src_ip, dst_ip, dport, "TCP", "Suspicious port syn",
                    abuse_score=score,
                    is_known_bad=is_bad
                )
                return

            # HTTP Avcısı: port 80 ve Raw payload varsa
            if dport == 80 and Raw in packet:
                try:
                    payload = packet[Raw].load.lower()
                except Exception:
                    payload = b""
                print(f"[DEBUG] HTTP raw length: {len(payload)}", flush=True)

                for kw in cfg.KEYWORDS_TO_HUNT:
                    if kw in payload:
                        
                        # --- YENİ (Hafta 4) ---
                        # Olayı loglamadan önce IP'nin sicilini kontrol et
                        print(f"[THREAT INTEL] HTTP sızıntısı için {src_ip} sorgulanıyor...", flush=True)
                        score, is_bad = threat_intel.get_ip_reputation(src_ip)
                        # ---------------------
                        
                        # Uyarıyı ver
                        alert.print_http_leak(src_ip, dst_ip, kw, payload)
                        
                        # --- GÜNCELLEME (Hafta 4) ---
                        # Loglama fonksiyonuna yeni skor/durum bilgisini de gönder
                        logger.insert_event(
                            src_ip, dst_ip, dport, "HTTP", f"Leak: {kw.decode(errors='ignore')}",
                            abuse_score=score,
                            is_known_bad=is_bad
                        )
                        break

        except Exception:
            # Hata yutmak yerine logla ki neden uyarı gelmediğini görelim
            print("[DEBUG][analyzer][TCP] exception:", traceback.format_exc(), flush=True)