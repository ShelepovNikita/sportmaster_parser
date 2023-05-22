"""Главный модуль скрипта, отвечающий за его запуск."""
from typing import Generator, Any

from requests import post

from converter import to_json, to_xml, to_excel, to_csv
from constants import COOKIES, HEADERS


def requset_to_site() -> Generator[dict[str, Any], None, None]:
    """Возвращает генератор, который генерирует
    словари с данными о кроссовках."""
    products_count = 1
    page = 0
    while products_count != 0:
        cookies = COOKIES
        headers = HEADERS
        json_data = {
            'url': '/catalog/muzhskaya_obuv/krossovki',
            'page': page + 1,
        }
        response = post('https://www.sportmaster.ru/web-api/v1/catalog/',
                        cookies=cookies, headers=headers,
                        json=json_data).json()

        products_count = len(response.get('products'))
        print(page)
        page += 1

        for sneakers_raw in response.get('products'):
            yield get_sneakers(sneakers_raw)


def get_sneakers(sneakers_raw: dict[str, Any]) -> dict[str, Any]:
    """Возвращает словарь с данными о текущих кросовках."""
    sneakers = dict()
    sneakers['Id'] = sneakers_raw.get('productId')
    sneakers['Рейтинг'] = float(sneakers_raw.get('rating'))
    sneakers['Цена'] = int(sneakers_raw.get('price').get('retail'))
    sneakers['Старая цена'] = int(sneakers_raw.get('price').get('catalog'))
    return sneakers


def main() -> None:
    """Главная функция модуля, запускающая работу скрипта."""
    column_names = ['Id',
                    'Рейтинг',
                    'Цена',
                    'Старая цена']

    sneakers = list(requset_to_site())

    to_excel(sneakers, column_names, file_name="sneakers")
    to_json(sneakers, file_name="sneakers")
    to_xml(
        sneakers,
        parameters=column_names,
        root='Кроссовки',
        item_name='Кроссовки',
        file_name="sneakers"
    )
    to_csv(sneakers, column_names, file_name="sneakers")


if __name__ == '__main__':
    main()
