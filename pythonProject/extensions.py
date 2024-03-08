import requests
import json
from config import keys
class ConvertionException(Exception):
    pass

class Convertor:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно конвертировать одинаковые валюты {base}.')

        try:
            q_tick = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не обнаружена валюта {quote}')

        try:
            b_tick = keys[base]
        except KeyError:
            raise ConvertionException(f'Не обнаружена валюта {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать кол-во {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={q_tick}&tsyms={b_tick}')
        total_base = json.loads(r.content)[keys[base]]
        result = total_base * amount

        return result