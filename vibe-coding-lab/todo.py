"""
Basit terminal tabanlı Yapılacaklar Listesi (To-Do List) uygulaması.
Görev ekleme, silme, listeleme ve hafızada saklama özellikleri.
"""

import os

# Metin dosyası her zaman script'in bulunduğu klasörde oluşturulur
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOSYA_YOLU = os.path.join(SCRIPT_DIR, "gorevler.txt")


def gorevleri_yukle():
    """Kaydedilmiş görevleri metin dosyasından yükler."""
    if os.path.exists(DOSYA_YOLU):
        try:
            with open(DOSYA_YOLU, "r", encoding="utf-8") as f:
                return [satir.strip() for satir in f.readlines() if satir.strip()]
        except IOError:
            return []
    return []


def gorevleri_kaydet(gorevler):
    """Görevleri metin dosyasına kaydeder (her satır bir görev)."""
    with open(DOSYA_YOLU, "w", encoding="utf-8") as f:
        f.write("\n".join(gorevler))


def listele(gorevler, bekle=True):
    """Görevleri listeler. bekle=False ise (sil fonksiyonundan) Enter beklemez."""
    if not gorevler:
        print("\n  Listede henüz görev yok.", flush=True)
    else:
        print("\n  ═══ YAPILACAKLAR LİSTESİ ═══\n", flush=True)
        for i, gorev in enumerate(gorevler, 1):
            print(f"  {i}. {gorev}", flush=True)
    if bekle:
        input("\n  [Menüye dönmek için Enter'a basın]")


def ekle(gorevler):
    """Yeni görev ekler."""
    gorev = input("\n  Yeni görev: ").strip()
    if gorev:
        gorevler.append(gorev)
        gorevleri_kaydet(gorevler)
        print(f"\n  ✓ '{gorev}' eklendi.")
    else:
        print("\n  Görev boş olamaz.")


def sil(gorevler):
    """Görev siler."""
    listele(gorevler, bekle=False)
    if not gorevler:
        return
    try:
        no = int(input("\n  Silinecek görev numarası: "))
        if 1 <= no <= len(gorevler):
            silinen = gorevler.pop(no - 1)
            gorevleri_kaydet(gorevler)
            print(f"\n  ✓ '{silinen}' silindi.")
        else:
            print("\n  Geçersiz numara.")
    except ValueError:
        print("\n  Lütfen sayı girin.")


def main():
    gorevler = gorevleri_yukle()
    
    while True:
        print("\n" + "─" * 35)
        print("  YAPILACAKLAR LİSTESİ")
        print("─" * 35)
        print("  1. Görevleri listele")
        print("  2. Görev ekle")
        print("  3. Görev sil")
        print("  4. Çıkış")
        print("─" * 35)
        
        try:
            secim = int(input("\n  Seçiminiz (1-4): ").strip())
        except ValueError:
            print("\n  Lütfen 1-4 arası bir sayı girin.")
            continue
        
        if secim == 1:
            listele(gorevler)
        elif secim == 2:
            ekle(gorevler)
        elif secim == 3:
            sil(gorevler)
        elif secim == 4:
            print("\n  Görüşmek üzere!\n")
            break
        else:
            print("\n  Geçersiz seçim. 1-4 arası bir sayı girin.")


if __name__ == "__main__":
    main()
