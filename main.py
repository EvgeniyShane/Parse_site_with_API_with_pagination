import json
import requests

def fetch_products(category_slug, page_number):
    url = f'https://api.technodom.kz/katalog/api/v1/products/category/{category_slug}?city_id=5f5f1e3b4c8a49e692fefd70&limit=24&brands=samsung&sorting=score&price=0&page={page_number}'
    products_raw = requests.get(url).json()
    return products_raw.get("payload", [])

categories_slug = []
categories_raw = requests.get('https://api.technodom.kz/menu/api/v1/menu/breadcrumbs/categories/smartfony?brands=samsung').json()
for category in categories_raw:
    categories_slug.append(category["category_code"])

products = []
for category_slug in categories_slug:
    try:
        for page_number in range(1, 6): 
            products_raw = fetch_products(category_slug, page_number)
            if not products_raw:
                break

            for product_raw in products_raw:
                products.append({
                    "category": category_slug,
                    "page": page_number,
                    "title": product_raw["title"],
                    "price": product_raw["price"]
                })

    except Exception as e:
        print(f"Error fetching products for category {category_slug}: {str(e)}")

with open('products.json', 'w', encoding='utf-8') as outfile:
    json.dump(products, outfile, indent=2, ensure_ascii=False)