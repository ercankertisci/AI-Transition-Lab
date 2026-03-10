# 💱 Canlı Döviz Kuru Uygulaması

Python ile yazılmış, canlı döviz kurlarını terminalde şık bir tablo ile gösteren uygulama.

## Özellikler

- 🔐 API anahtarını `.env` dosyasından güvenli okuma
- 💱 Kullanıcının seçtiği para birimlerini karşılaştırma
- 🎨 Renkli ve şık terminal tablosu (Rich kütüphanesi)
- ⚠️ Profesyonel hata yönetimi (internet, API, zaman aşımı)
- 🆓 API anahtarı olmadan Frankfurter API ile çalışabilir

## Kurulum

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# .env dosyasını oluştur (opsiyonel)
copy .env.example .env
# .env içine EXCHANGERATE_API_KEY=your_key ekleyin
```

## API Anahtarı (Opsiyonel)

**ExchangeRate-API** kullanmak için:
1. [exchangerate-api.com](https://www.exchangerate-api.com/) adresinden ücretsiz kayıt olun
2. API anahtarınızı alın
3. `.env` dosyasına `EXCHANGERATE_API_KEY=anahtarınız` ekleyin

API anahtarı yoksa uygulama **Frankfurter API** ile çalışır (ECB verileri).

## Kullanım

```bash
python main.py
```

Uygulama sırasıyla:
1. Temel para birimini sorar (örn: USD)
2. Karşılaştırılacak para birimlerini sorar (örn: EUR, TRY, GBP)
3. Kurları çekip renkli tabloda gösterir

## Örnek Çıktı

```
╭─────────────────────────────────────────────╮
│  💱 Canlı Döviz Kurları (1 USD = ?)         │
├─────────────┬─────────────────┬─────────────┤
│ Para Birimi │ İsim            │ Kur         │
├─────────────┼─────────────────┼─────────────┤
│ EUR         │ Euro            │ 0.9234      │
│ TRY         │ Türk Lirası     │ 32.4512     │
│ GBP         │ İngiliz Sterlini│ 0.7912      │
╰─────────────┴─────────────────┴─────────────╯
```

## Hata Durumları

- **İnternet yok**: Açıklayıcı hata mesajı
- **API anahtarı geçersiz**: .env kontrolü önerisi
- **Zaman aşımı**: Kullanıcı dostu bilgilendirme
- **İstek limiti**: 429 durumunda bilgilendirme
