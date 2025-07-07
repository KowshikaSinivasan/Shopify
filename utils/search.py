from elasticsearch import Elasticsearch
import urllib3
from utils.fetch_data import (
    get_product_details_by_ids,
    get_product_inventory_by_ids,
    get_product_prices_by_ids,
    get_product_sales_by_ids,
    get_product_sponsorship_by_ids
)

# ✅ Disable SSL warnings (for local development only)
urllib3.disable_warnings()

# ✅ Connect to Elasticsearch
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "kowsh@123"),
    verify_certs=False
)

def search_and_get_products(keyword):
    """
    Search for products in Elasticsearch using a keyword,
    then fetch and return enriched product data.
    """
    keyword = keyword.lower()
    matched_ids = set()

    try:
        # ---------- 1. Search in product_details index ----------
        query_details = {
            "query": {
                "bool": {
                    "should": [
                        {"match_phrase": {"name": keyword}},
                        {"match_phrase": {"description": keyword}}
                    ]
                }
            },
            "_source": ["product_id"]
        }

        res1 = es.search(index="product_details", body=query_details, size=100)
        for hit in res1["hits"]["hits"]:
            pid = hit["_source"].get("product_id")
            if pid:
                matched_ids.add(pid)

        # ---------- 2. Search in products index ----------
        query_products = {
            "query": {
                "bool": {
                    "should": [
                        {"match_phrase": {"name": keyword}},
                        {"match_phrase": {"description": keyword}},
                        {"match_phrase": {"category": keyword}},
                        {"match_phrase": {"subcategory": keyword}}
                    ]
                }
            },
            "_source": ["product_id"]
        }

        res2 = es.search(index="products", body=query_products, size=100)
        for hit in res2["hits"]["hits"]:
            pid = hit["_source"].get("product_id")
            if pid:
                matched_ids.add(pid)

        product_ids = list(matched_ids)
        print(f"🔍 Matched product_ids for '{keyword}': {product_ids}")

        if not product_ids:
            return {"error": f"No products found for keyword: {keyword}"}

        # ---------- 3. Fetch data using helper functions ----------
        details_data = get_product_details_by_ids(product_ids)
        inventory_data = get_product_inventory_by_ids(product_ids)
        price_data = get_product_prices_by_ids(product_ids)
        sales_data = get_product_sales_by_ids(product_ids)
        sponsorship_data = get_product_sponsorship_by_ids(product_ids)

        # ---------- 4. Merge data into unified product dictionary ----------
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
        print(f"❌ Error in search_and_get_products: {e}")
        return {"error": f"Search failed: {e}"}
