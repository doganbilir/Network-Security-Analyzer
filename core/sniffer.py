# core/sniffer.py

from scapy.all import sniff
from config.config import LOG_FILE, SUSPICIOUS_PORTS, KEYWORDS_TO_HUNT, BPF_FILTER
from core.analyzer import process_packet

def start_sniff():
    print("Sniffer başlatılıyor...")
    sniff(prn=process_packet, store=0, filter=BPF_FILTER)

if __name__ == "__main__":
    try:
        start_sniff()
    except PermissionError:
        print("[HATA] root/sudo gereklidir.")
    except KeyboardInterrupt:
        print("[BİLGİ] Sniffer durduruldu.")
