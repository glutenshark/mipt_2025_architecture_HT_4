from .base_usd_converter import BaseUsdConverter

class UniversalUsdConverter(BaseUsdConverter):
    """
    Универсальный класс, наследуемся от BaseUsdConverter
    и указываем нужную валюту через параметр target_currency.
    """

    def __init__(self, target_currency: str, max_retries=3, retry_delay=1):
        super().__init__(max_retries, retry_delay)
        self.target_currency = target_currency

    def convert(self, amount: float) -> float:
        """
        Вызывает базовый метод convert_from_usd, 
        передавая нужную валюту (self.target_currency).
        """
        return self.convert_from_usd(amount, self.target_currency)
