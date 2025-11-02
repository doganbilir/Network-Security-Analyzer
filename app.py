# Bu script, OKUYUCU (webapp) uygulamasını başlatır.
# Terminal 2'de normal kullanıcı olarak çalıştırılır: python3 run_web.py

# 'app' klasörümüzün içinden 'app' adlı
# Flask uygulamasını import et
from app import app

if __name__ == "__main__":
    print("Flask web sunucusu http://127.0.0.1:5001/ adresinde başlatılıyor...")
    
    # debug=True: Kodu kaydettiğinde sunucunun otomatik yeniden başlamasını sağlar.
    # port=5001: 5000 varsayılan porttur, çakışmasın diye farklı port seçtik.
    # host="0.0.0.0": Sunucunun sadece localhost'tan değil, 
    #                ağdaki diğer cihazlardan da (örn: telefonun) erişilebilir olmasını sağlar.
    app.run(debug=True, port=5001, host="0.0.0.0")
