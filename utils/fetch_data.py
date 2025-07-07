from elasticsearch import Elasticsearch
import urllib3

# 🔒 Disable SSL warnings (for local dev only)
urllib3.disable_warnings()

# ✅ Connect to Elasticsearch
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "kowsh@123"),  # 🔑 Replace with your actual ES password
    verify_certs=False
)

# 🔹 Step 1: Get product IDs by category
def get_product_ids_by_category(category_name):
    print("1.")
    try:
        res = es.search(
            index="products",
            body={
                "query": {
                    "term": {
                        "category.keyword": category_name
                    }
                },
                "_source": ["product_id"]
            },
            size=100
        )
        product_ids = [hit["_source"]["product_id"] for hit in res["hits"]["hits"]]
        print(f"🔍 Product IDs for category '{category_name}': {product_ids}")
        return product_ids
    except Exception as e:
        print(f"❌ Error fetching product IDs: {e}")
        return f"Error fetching product IDs: {e}"

# 🔹 Step 2: Get product details by IDs (via search)
def get_product_details_by_ids(product_ids):
    print("2. 🔍 Fetching product details by search")
    product_details = []
    try:
        for pid in product_ids:
            try:
                res = es.search(
                    index="product_details",
                    body={
                        "query": {
                            "term": {
                                "product_id.keyword": pid
                            }
                        }
                    }
                )
                hits = res["hits"]["hits"]
                if hits:
                    print(f"✅ Found details for {pid}")
                    product_details.append(hits[0]["_source"])
                else:
                    print(f"❌ No match found for {pid}")
            except Exception as inner_e:
                print(f"❌ Error for {pid}: {inner_e}")
                continue
        return product_details
    except Exception as e:
        return f"Error fetching product details: {e}"

# 🔹 Step 3: Get inventory quantity for product IDs
def get_product_inventory_by_ids(product_ids):
    print("3. 🔍 Fetching inventory via search")
    inventory = {}
    try:
        for pid in product_ids:
            try:
                res = es.search(
                    index="product_inventory",
                    body={
                        "query": {
                            "term": {
                                "product_id.keyword": pid
                            }
                        }
                    }
                )
                hits = res["hits"]["hits"]
                if hits:
                    quantity = hits[0]["_source"].get("Quantity", 0)
                    inventory[pid] = quantity
                    print(f"📦 Inventory for {pid}: {quantity}")
                else:
                    inventory[pid] = 0
                    print(f"⚠️ No inventory record for {pid}")
            except Exception as e:
                inventory[pid] = 0
                print(f"❌ Error for {pid}: {e}")
        return inventory
    except Exception as e:
        print(f"❌ Bulk error fetching inventory: {e}")
        return f"Error fetching inventory: {e}"

# 🔹 Step 4: Get price details for product IDs
def get_product_prices_by_ids(product_ids):
    print("4.")
    prices = {}
    try:
        for pid in product_ids:
            try:
                res = es.search(
                    index="product_price",
                    body={
                        "query": {
                            "term": {
                                "product_id.keyword": pid
                            }
                        }
                    }
                )
                hits = res["hits"]["hits"]
                if hits:
                    source = hits[0]["_source"]
                    prices[pid] = {
                        "price": source.get("price"),
                        "discount": source.get("discount"),
                        "after_discount_price": source.get("after_discount_price"),
                        "currency": source.get("currency", "INR")
                    }
                    print(f"💰 Price for {pid}: {prices[pid]}")
                else:
                    print(f"⚠️ No price found for {pid}")
            except Exception as e:
                prices[pid] = None
                print(f"⚠️ Price fetch failed for {pid}: {e}")
        return prices
    except Exception as e:
        print(f"❌ Error fetching product prices: {e}")
        return f"Error fetching product prices: {e}"

# 🔹 Step 5: Get product sales insights
def get_product_sales_by_ids(product_ids):
    print("5. 🔍 Fetching sales data")
    sales_data = {}
    try:
        for pid in product_ids:
            try:
                res = es.search(
                    index="product_sales",
                    body={
                        "query": {
                            "term": {
                                "product_id.keyword": pid
                            }
                        }
                    }
                )
                hits = res["hits"]["hits"]
                if hits:
                    source = hits[0]["_source"]
                    sales_data[pid] = {
                        "female_buyer": source.get("female_buyer", 0),
                        "male_buyer": source.get("male_buyer", 0),
                        "most_bought_age_group": source.get("most_bought_age_group", "N/A"),
                        "country_most_bought": source.get("country_most_bought", "N/A"),
                        "avg_rating": source.get("avg_rating", 0)
                    }
                    print(f"📊 Sales for {pid}: {sales_data[pid]}")
                else:
                    sales_data[pid] = {}
                    print(f"⚠️ No sales data found for {pid}")
            except Exception as e:
                sales_data[pid] = {}
                print(f"❌ Error fetching sales for {pid}: {e}")
        return sales_data
    except Exception as e:
        print(f"❌ Error fetching sales data: {e}")
        return f"Error fetching sales data: {e}"
# 🔹 Step 6: Get sponsorship status for product IDs
def get_product_sponsorship_by_ids(product_ids):
    print("7. 🔍 Fetching sponsorship status")
    sponsorship = {}
    try:
        for pid in product_ids:
            try:
                res = es.search(
                    index="product_sponsorship",
                    body={
                        "query": {
                            "term": {
                                "product_id.keyword": pid
                            }
                        }
                    }
                )
                hits = res["hits"]["hits"]
                if hits:
                    sponsored = hits[0]["_source"].get("sponsored", 0)
                    sponsorship[pid] = sponsored
                    print(f"🏷️ Sponsorship for {pid}: {sponsored}")
                else:
                    sponsorship[pid] = 0
                    print(f"⚠️ No sponsorship record for {pid}")
            except Exception as e:
                sponsorship[pid] = 0
                print(f"❌ Error for {pid}: {e}")
        return sponsorship
    except Exception as e:
        print(f"❌ Error fetching sponsorships: {e}")
        return f"Error fetching sponsorships: {e}"

# 🔹 Step 7: Combine everything into a single product dictionary
# 🔹 Step 7: Combine everything into a single product dictionary
def get_products(category):
    print("6.")
    try:
        print(f"\n📁 Fetching full product data for category: {category}")
        product_ids = get_product_ids_by_category(category)

        if isinstance(product_ids, str):
            return {"error": product_ids}

        if not product_ids:
            return {"error": "No products found for this category."}

        details_data = get_product_details_by_ids(product_ids)
        inventory_data = get_product_inventory_by_ids(product_ids)
        price_data = get_product_prices_by_ids(product_ids)
        sales_data = get_product_sales_by_ids(product_ids)
        sponsorship_data = get_product_sponsorship_by_ids(product_ids)  # 🔹 Added

        products = {}
        for item in details_data:
            pid = item.get("product_id")
            products[pid] = {
                "details": item,
                "inventory": inventory_data.get(pid, 0),
                "price": price_data.get(pid, {}),
                "sales": sales_data.get(pid, {}),
                "sponsorship": sponsorship_data.get(pid, 0)  # 🔹 Include sponsorship
            }
            print(f"✅ Product built: {pid}")

        return products

    except Exception as e:
        print(f"❌ Error building product data: {e}")
        return {"error": f"Error building product data: {e}"}
