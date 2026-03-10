# -*- coding: utf-8 -*-
"""
Canli Doviz Kuru Uygulamasi
API'den doviz kurlarini ceker ve terminalde tablo olarak gosterir.
"""

import os
import sys
from typing import Optional

# Windows konsolunda UTF-8 ve emoji destegi
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

try:
    import requests
    from dotenv import load_dotenv
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
except ImportError:
    print("[!] Eksik paket tespit edildi. Lutfen su komutu calistirin:")
    print("   pip install -r requirements.txt")
    sys.exit(1)

# .env dosyasını yükle
load_dotenv()

console = Console()

# API konfigürasyonu
EXCHANGERATE_API_URL = "https://v6.exchangerate-api.com/v6/{key}/latest/{base}"
FRANKFURTER_API_URL = "https://api.frankfurter.app/latest"

# Populer para birimleri
COMMON_CURRENCIES = {
    "USD": "Amerikan Dolari",
    "EUR": "Euro",
    "GBP": "Ingiliz Sterlini",
    "TRY": "Turk Lirasi",
    "JPY": "Japon Yeni",
    "CHF": "Isvicre Frangi",
    "CAD": "Kanada Dolari",
    "AUD": "Avustralya Dolari",
    "CNY": "Cin Yuani",
    "RUB": "Rus Rublesi",
}


def get_api_key() -> Optional[str]:
    """API anahtarını .env dosyasından güvenli şekilde okur."""
    return os.getenv("EXCHANGERATE_API_KEY") or os.getenv("API_KEY")


def fetch_rates_exchangerate(base: str, api_key: str) -> dict:
    """ExchangeRate-API ile kurları çeker."""
    url = EXCHANGERATE_API_URL.format(key=api_key, base=base)
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("result") != "success":
        raise ValueError(data.get("error-type", "Bilinmeyen API hatasi"))

    return data.get("conversion_rates", {})


def fetch_rates_frankfurter(base: str, symbols: list[str]) -> dict:
    """Frankfurter API ile kurları çeker (ücretsiz, API anahtarı gerekmez)."""
    params = {"from": base, "to": ",".join(symbols)}
    response = requests.get(FRANKFURTER_API_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("rates", {})


def fetch_exchange_rates(base: str, target_currencies: list[str]) -> tuple[dict, str]:
    """
    Döviz kurlarını API'den çeker.
    ExchangeRate-API (API key varsa) veya Frankfurter (API key yoksa) kullanır.
    Returns: (rates_dict, base_currency)
    """
    api_key = get_api_key()

    if api_key:
        try:
            all_rates = fetch_rates_exchangerate(base, api_key)
            rates = {curr: all_rates.get(curr) for curr in target_currencies if all_rates.get(curr)}
            return rates, base
        except requests.RequestException as e:
            console.print(f"\n[bold red]ExchangeRate-API baglanti hatasi.[/bold red]")
            console.print(f"Frankfurter API ile deneniyor...")
            # Fallback to Frankfurter
            pass

    # Frankfurter (ücretsiz, anahtar gerektirmez)
    try:
        rates = fetch_rates_frankfurter(base, target_currencies)
        return rates, base
    except requests.RequestException as e:
        raise ConnectionError(
            "Internet baglantisi kurulamadi veya API erisilemiyor. "
            "Baglantinizi kontrol edip tekrar deneyin."
        ) from e


def get_currency_input(prompt: str, allow_multiple: bool = False) -> list[str]:
    """Kullanıcıdan para birimi girişi alır."""
    console.print(f"\n[cyan]{prompt}[/cyan]")
    console.print("Ornek: USD, EUR, TRY | Virgul ile birden fazla: USD,EUR,TRY")
    console.print("Mevcut kodlar: " + ", ".join(COMMON_CURRENCIES.keys()))

    while True:
        user_input = console.input("\n[bold]Giris: [/bold]").strip().upper()
        if not user_input:
            console.print("[yellow]Lutfen en az bir para birimi girin.[/yellow]")
            continue

        currencies = [c.strip() for c in user_input.replace("，", ",").split(",") if c.strip()]
        if not currencies:
            console.print("[yellow]Gecerli bir para birimi kodu girin.[/yellow]")
            continue

        return currencies


def display_results(base: str, rates: dict):
    """Sonuçları Rich tablo ile gösterir."""
    if not rates:
        console.print("[bold red]Gosterilecek kur bilgisi bulunamadi.[/bold red]")
        return

    table = Table(
        title=f"Canli Doviz Kurlari (1 {base} = ?)",
        show_header=True,
        header_style="bold magenta",
        border_style="blue",
    )
    table.add_column("Para Birimi", style="cyan", justify="center")
    table.add_column("Isim", style="dim")
    table.add_column("Kur", justify="right", style="bold green")

    for curr, rate in sorted(rates.items()):
        name = COMMON_CURRENCIES.get(curr, "-")
        table.add_row(curr, name, f"{rate:,.4f}")

    console.print()
    console.print(Panel(table, border_style="blue"))
    console.print()


def run():
    """Ana uygulama akışı."""
    console.print(Panel.fit(
        "[bold cyan]DOVIZ KURU UYGULAMASI[/bold cyan]\n"
        "Guncel doviz kurlarini aninda goruntuleyin.",
        border_style="cyan",
    ))

    try:
        # Temel para birimi
        base_currencies = get_currency_input("Karsilastirma icin temel para birimini girin (orn: USD):")
        base = base_currencies[0]

        # Karşılaştırılacak para birimleri
        target_prompt = f"{base} kuruyla karsilastirmak istediginiz para birimlerini girin:"
        targets = get_currency_input(target_prompt, allow_multiple=True)

        if base in targets:
            targets = [t for t in targets if t != base]

        if not targets:
            console.print("[yellow]Karsilastirma icin en az bir farkli para birimi gerekli.[/yellow]")
            return

        # Kurları çek
        console.print("\n[dim]Kurlar aliniyor...[/dim]")
        rates, _ = fetch_exchange_rates(base, targets)

        display_results(base, rates)

    except requests.ConnectionError:
        console.print("\n[bold red][X] Internet Baglanti Hatasi[/bold red]")
        console.print(
            "Internet baglantinizi kontrol edin ve tekrar deneyin. "
            "API sunucularina erisilemiyor."
        )
        sys.exit(1)

    except requests.Timeout:
        console.print("\n[bold red][X] Zaman Asimi[/bold red]")
        console.print("API sunucusu yanit vermedi. Lutfen daha sonra tekrar deneyin.")
        sys.exit(1)

    except requests.HTTPError as e:
        console.print(f"\n[bold red][X] API HTTP Hatasi ({e.response.status_code})[/bold red]")
        if e.response.status_code == 401:
            console.print("API anahtariniz gecersiz. .env dosyasindaki EXCHANGERATE_API_KEY degerini kontrol edin.")
            console.print("Not: API anahtari olmadan Frankfurter API kullanilir (sinirli para birimleri).")
        elif e.response.status_code == 429:
            console.print("API istek limiti asildi. Lutfen daha sonra tekrar deneyin.")
        else:
            console.print(f"Sunucu hatasi: {e}")
        sys.exit(1)

    except (ConnectionError, ValueError) as e:
        console.print(f"\n[bold red][X] Hata[/bold red]")
        console.print(str(e))
        sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Cikis yapildi.[/yellow]")
        sys.exit(0)


if __name__ == "__main__":
    run()
