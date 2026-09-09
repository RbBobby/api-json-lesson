"""
Учебный проект: запросы к API и разбор JSON.

Документация API:
https://automationexercise.com/api_list

Запуск:
    python3 -m pip install -r requirements.txt
    python3 main.py
"""

import requests

BASE_URL = "https://automationexercise.com/api"


def get_json(url, method="GET", data=None):
    
    """Отправляет запрос и возвращает ответ как словарь Python."""
    if method == "GET":
        response = requests.get(url, params=data, timeout=20)
    elif method == "POST":
        response = requests.post(url, data=data, timeout=20)
    else:
        response = requests.request(method, url, data=data, timeout=20)

    # HTTP-код (200, 405 и т.д.)P
    print(f"HTTP статус: {response.status_code}")

    # У этого сайта JSON часто приходит как текст — парсим явно
    return response.json()


def lesson_1_all_products():
    print("\n" + "=" * 60)
    print("Урок 1. GET — список всех товаров")
    print("=" * 60)

    url = f"{BASE_URL}/productsList"

    data = get_json(url)

    # Переменные из JSON
    response_code = data.get("responseCode")
    products = data.get("products", [])

    print(f"Код из JSON: {response_code}")
    print(f"Всего товаров: {len(products)}")

    if response_code != 200:
        print("Список товаров не получен")
        return []

    # Цикл по списку словарей
    print("\nПервые 5 товаров:")
    for product in products[:5]:
        product_id = product["id"]
        name = product["name"]
        price = product["price"]
        brand = product["brand"]
        print(f"  #{product_id}: {name} | {price} | {brand}")

    return products


def lesson_2_filter_products(products):
    print("\n" + "=" * 60)
    print("Урок 2. if + for — фильтр и счётчики")
    print("=" * 60)

    women_count = 0
    men_count = 0
    kids_count = 0
    expensive = []

    for product in products:
        name = product["name"]
        price_text = product["price"]  # например "Rs. 500"
        user_type = product["category"]["usertype"]["usertype"]

        # Цена приходит строкой — достаём число
        price_number = int(price_text.replace("Rs.", "").strip())

        if user_type == "Women":
            women_count += 1
        elif user_type == "Men":
            men_count += 1
        elif user_type == "Kids":
            kids_count += 1

        if price_number >= 1500:
            expensive.append(name)

    print(f"Женские: {women_count}")
    print(f"Мужские: {men_count}")
    print(f"Детские: {kids_count}")
    print(f"Товары от 1500 Rs.: {len(expensive)}")

    for name in expensive:
        print(f"  - {name}")


def lesson_3_unique_brands(products):
    print("\n" + "=" * 60)
    print("Урок 3. Словарь-счётчик брендов")
    print("=" * 60)

    brand_counts = {}

    for product in products:
        brand = product["brand"]

        if brand in brand_counts:
            brand_counts[brand] += 1
        else:
            brand_counts[brand] = 1

    print("Сколько товаров у каждого бренда:")
    for brand, count in brand_counts.items():
        print(f"  {brand}: {count}")


def lesson_4_brands_api():
    print("\n" + "=" * 60)
    print("Урок 4. GET — список брендов")
    print("=" * 60)

    url = f"{BASE_URL}/brandsList"
    data = get_json(url)
    brands = data.get("brands", [])

    print(f"Записей в списке: {len(brands)}")

    unique_names = []
    for item in brands:
        name = item["brand"]
        if name not in unique_names:
            unique_names.append(name)

    print("Уникальные бренды:")
    for name in unique_names:
        print(f"  - {name}")


def lesson_5_search():
    print("\n" + "=" * 60)
    print("Урок 5. POST — поиск товаров")
    print("=" * 60)

    search_word = "top"
    url = f"{BASE_URL}/searchProduct"
    data = get_json(url, method="POST", data={"search_product": search_word})

    response_code = data.get("responseCode")
    products = data.get("products", [])

    print(f"Ищем: {search_word}")
    print(f"Код из JSON: {response_code}")
    print(f"Найдено: {len(products)}")

    if response_code == 200 and products:
        for product in products[:8]:
            print(f"  - {product['name']} ({product['price']})")
    else:
        print("Ничего не найдено")


def lesson_6_errors():
    print("\n" + "=" * 60)
    print("Урок 6. Ошибки API: if по responseCode")
    print("=" * 60)

    # Поиск без обязательного параметра → 400
    print("\n1) POST searchProduct без параметра")
    data = get_json(f"{BASE_URL}/searchProduct", method="POST")
    code = data.get("responseCode")
    message = data.get("message", "")

    if code == 400:
        print(f"Ожидаемая ошибка: {message}")
    else:
        print(f"Неожиданный код: {code}")

    # POST на productsList не поддерживается → 405
    print("\n2) POST на productsList (метод не поддерживается)")
    data = get_json(f"{BASE_URL}/productsList", method="POST")
    code = data.get("responseCode")
    message = data.get("message", "")

    if code == 405:
        print(f"Ожидаемая ошибка: {message}")
    else:
        print(f"Неожиданный код: {code}")


def main():
    print("Учебный разбор JSON с automationexercise.com")

    products = lesson_1_all_products()

    if products:
        lesson_2_filter_products(products)
        lesson_3_unique_brands(products)
    else:
        print("Пропускаем уроки 2–3: нет списка товаров")

    lesson_4_brands_api()
    lesson_5_search()
    lesson_6_errors()

    print("\nГотово.")


if __name__ == "__main__":
    main()
