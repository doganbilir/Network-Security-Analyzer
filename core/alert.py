# core/alert.py (Temizlenmiş Sürüm)

try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    print("[UYARI] 'plyer' kütüphanesi bulunamadı. Masaüstü bildirimleri devre dışı.")
    PLYER_AVAILABLE = False
except Exception as e:
    # pyobjus gibi bir alt bağımlılık hatasını yakala
    print(f"[UYARI] Plyer yüklenirken bir hata oluştu (detay: {e}). Masaüstü bildirimleri devre dışı.")
    PLYER_AVAILABLE = False

from config.config import RENK_KIRMIZI, RENK_SARI, RENK_RESET

def _send_desktop_notification(title, message):
    """
    Güvenli bir şekilde masaüstü bildirimi gönderen yardımcı fonksiyon.
    """
    if not PLYER_AVAILABLE:
        return # plyer yüklenememişse hiçbir şey yapma

    try:
        notification.notify(
            title=title,
            message=message,
            app_name='Ağ Güvenlik Monitörü',
            timeout=10
        )
    except Exception as e:
        # Bildirim gönderme anında bir hata olursa (örn: sunucu ortamı)
        # sniffer'ın çökmesini engelle.
        print(f"{RENK_KIRMIZI}[BİLDİRİM HATASI] Masaüstü bildirimi gönderilemedi: {e}{RENK_RESET}", flush=True)


def print_suspicious_port(src_ip, dst_port):
    # Konsol uyarısı
    print(f"\n{RENK_KIRMIZI}##################################################")
    print("[UYARI] ŞÜPHELİ PORT BAĞLANTISI TESPİT EDİLDİ!")
    print(f"  -> Kaynak: {src_ip}")
    print(f"  -> Hedef Port: {dst_port}")
    print(f"##################################################{RENK_RESET}\n")

    # Masaüstü uyarısı
    title = "🚨 ŞÜPHELİ PORT UYARISI"
    message = f"Kaynak IP: {src_ip}\nHedef Port: {dst_port}"
    _send_desktop_notification(title, message)

def print_http_leak(src_ip, dst_ip, keyword, snippet):
    # Konsol uyarısı
    print(f"\n{RENK_SARI}##################################################")
    print("[HTTP AVCISI] GÜVENSİZ GİRİŞ BİLGİSİ YAKALANDI!")
    print(f"  -> '{keyword.decode()}' anahtar kelimesi Port 80 üzerinden gönderildi.")
    print(f"  -> {src_ip}  --->  {dst_ip}")
    print(f"  -> Örnek: {snippet[:100]}...")
    print(f"##################################################{RENK_RESET}\n")

    # Masaüstü uyarısı
    title = "🔒 HTTP VERİ SIZINTISI"
    message = f"'{keyword.decode()}' kelimesi {src_ip} -> {dst_ip} arasında yakalandı."
    _send_desktop_notification(title, message)
