import requests
import json
from keys import keys


class APIException(Exception):
    pass


class ValuteConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        cur = json.loads(r.content)

        if quote_ticker != 'RUR':
            if base_ticker == 'RUR':
                total_base = round(
                    (cur['Valute'][quote_ticker]['Value'] / cur['Valute'][quote_ticker]['Nominal']) * amount, 4)
            else:
                total_base = round(((cur['Valute'][quote_ticker]['Value'] / cur['Valute'][quote_ticker]['Nominal']) / (
                        cur['Valute'][base_ticker]['Value'] / cur['Valute'][base_ticker]['Nominal'])) * amount, 4)
        else:
            total_base = round(
                (1 / (cur['Valute'][base_ticker]['Value'] / cur['Valute'][base_ticker]['Nominal'])) * amount, 4)

        return total_base
