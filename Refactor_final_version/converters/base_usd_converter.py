import requests
import logging
import time

class BaseUsdConverter:
    """
    Базовый класс конвертации USD в другие валюты, который:
      - Содержит кэш и логику получения курсов (fetch_rates).
      - Умеет логировать и обрабатывать ошибки.
      - Универсальный метод convert_from_usd(amount, currency).
      - Записывает статистику в stats.txt.
    """

    API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

    def __init__(self, max_retries=3, retry_delay=1):
        """
        :param max_retries: Максимум попыток запроса к API
        :param retry_delay: Пауза (сек) между повторными попытками
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._rates_cache = None

        # Логгер для вывода в консоль
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def _fetch_rates(self):
        """
        Загружает курсы из API, если _rates_cache ещё пуст.
        При неудаче делает несколько повторов (max_retries).
        Если провалили все попытки, оставляет _rates_cache = {}.
        """
        if self._rates_cache is not None:
            return  # Уже загружали

        for attempt in range(self.max_retries):
            try:
                response = requests.get(self.API_URL, timeout=5)
                response.raise_for_status()
                data = response.json()

                self._rates_cache = data.get("rates", {})
                self.logger.info("Rates fetched successfully.")
                return
            except (requests.exceptions.RequestException, KeyError, ValueError) as e:
                self.logger.error(f"Error fetching rates (attempt {attempt+1}): {e}")
                time.sleep(self.retry_delay)

        # Все попытки оказались неудачными
        self.logger.error("Failed to fetch rates after all retries.")
        self._rates_cache = {}

    def convert_from_usd(self, amount: float, currency: str) -> float:
        """
        Универсальный метод: переводит amount USD в currency.
         1) Если нет кэша, вызывает _fetch_rates().
         2) Если курсы пусты или нет нужной валюты, возвращает 0 и пишет в лог (FAIL).
         3) Иначе умножает amount на курс и записывает успешную статистику (OK).
        """
        if self._rates_cache is None:
            self._fetch_rates()

        if not self._rates_cache or currency not in self._rates_cache:
            self.logger.warning(f"No rate for {currency}, returning 0.")
            self._record_stats(amount, currency, 0.0, success=False)
            return 0.0

        rate = self._rates_cache[currency]
        result = amount * rate

        self._record_stats(amount, currency, result, success=True)
        return result

    def _record_stats(self, amount, currency, result, success=True):
        """
        Записывает каждый вызов конвертации в stats.txt.
        """
        status = "OK" if success else "FAIL"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        line = f"{timestamp} - Convert {amount} USD to {currency} => {result} ({status})\n"

        with open("stats.txt", "a", encoding="utf-8") as f:
            f.write(line)
