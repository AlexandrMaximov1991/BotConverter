import json
import requests
from Config import keys


class ConvertionExeption(Exception):
    pass


class ValuesConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        quote = quote.lower()
        base = base.lower()

        if quote == base:
            raise ConvertionExeption(f'Не возможно переводить одинаковую валюту {quote}!')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExeption(f'Не удалось обработать валюту {quote}!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExeption(f'Не удалось обработать валюту {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f'Не удалось обработать колличество валюты {amount}!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')

        total_base = json.loads(r.content)[keys[base]]
        return total_base * amount
