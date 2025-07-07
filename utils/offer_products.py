from utils.fetch_data import (
    get_product_details_by_ids,
    get_product_inventory_by_ids,
    get_product_prices_by_ids,
    get_product_sales_by_ids,
    get_product_sponsorship_by_ids
)
from elasticsearch import Elasticsearch
import urllib3

# Disable SSL warnings (for dev)
urllib3.disable_warnings()

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "kowsh@123"),
    verify_certs=False
)

def get_offered_products():
    print("🔍 Searching for products with discount...")

    try:
        # Step 1: Get product_ids from product_price index with discount > 0
        res = es.search(
            index="product_price",
            body={
                "query": {
                    "range": {
                        "discount": {
                            "gt": 0
                        }
                    }
                },
                "_source": ["product_id"]
            },
            size=100
        )

        product_ids = [hit["_source"]["product_id"] for hit in res["hits"]["hits"]]
        print(f"🎯 Products on offer: {product_ids}")

        if not product_ids:
            return {"error": "No discounted products found."}

        # Step 2: Fetch all details using helper functions
        details_data = get_product_details_by_ids(product_ids)
        inventory_data = get_product_inventory_by_ids(product_ids)
        price_data = get_product_prices_by_ids(product_ids)
        sales_data = get_product_sales_by_ids(product_ids)
        sponsorship_data = get_product_sponsorship_by_ids(product_ids)

        # Step 3: Merge into final product dictionary
        products = {}
        for item in details_data:
            pid = item.get("product_id")
            products[pid] = {
                "details": item,
                "inventory": inventory_data.get(pid, 0),
                "price": price_data.get(pid, {}),
                "sales": sales_data.get(pid, {}),
                "sponsorship": sponsorship_data.get(pid, 0)
            }

        return products

    except Exception as e:
        print(f"❌ Error getting offered products: {e}")
        return {"error": f"Error fetching offers: {e}"}
