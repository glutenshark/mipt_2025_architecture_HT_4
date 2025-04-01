# main.py
from converters.universal_usd_converter import UniversalUsdConverter

def main():
    amount = 100
    print("Testing UniversalUsdConverter...")

    # Пример RUB
    rub_converter = UniversalUsdConverter("RUB")
    rub_value = rub_converter.convert(amount)
    print(f"{amount} USD in RUB = {rub_value}")

    # Пример EUR
    eur_converter = UniversalUsdConverter("EUR")
    eur_value = eur_converter.convert(amount)
    print(f"{amount} USD in EUR = {eur_value}")

if __name__ == "__main__":
    main()
