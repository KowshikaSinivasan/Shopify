# 🛒 Shopify - Intelligent E-commerce Search API System

**Shopify** is a backend-focused project aimed at building and experimenting with **various e-commerce search APIs** using **Elasticsearch**. These APIs cover real-world features like category-based search, offer filtering.

While the core focus is API design and search relevance logic, a lightweight **Streamlit UI** is used to visualize and interact with the APIs easily.

---

## 🎯 Project Aim

These APIs simulate real e-commerce behaviors like:
- Smart search by keyword, category, or offers
- Dynamic ranking using boosting, burying, and weighted scoring
- Sorting and filtering with Elasticsearch queries


---

## 🚀 Features

- 🔍 **Search APIs**
  - Category-based search
  - Offer-based product discovery
  - Full-text keyword search with weighted relevance

- 🧠 **Advanced Ranking**
  - **Boosting**: Give priority to specific product fields or terms
  - **Burying**: Demote certain results from dominating top ranks
  - **Weighted Edges**: Score products using parameters like rating, price, and popularity

- 📊 **Sort & Display**
  - Sort products by rating, price, etc.
  

---

## 🧱 Tech Stack

| Layer        | Technology      |
|--------------|-----------------|
| Frontend     | Streamlit       |
| Backend API  | Elasticsearch   |
| Dataset      | CSV + Preprocessed Fields |
| Others       | Python, Pandas, Custom ES Queries |

---

## 📁 Folder Structure

```plaintext
.
├── app.py                      # Main Streamlit launcher
├── pages/                      # All UI logic for different sections
│   ├── login.py                # Login screen
│   ├── offer_page.py           # Offer products page
│   ├── searchpage.py           # General search UI
│   ├── user_profile.py         # User profile page
│   ├── Category_search.py      # Search by category
│   └── homepage.py             # Homepage/landing screen
├── utils/                      # Backend logic and helpers
│   ├── auth.py                 # Handles authentication
│   ├── fetch_data.py           # Loads and processes dataset
│   ├── offer_products.py       # Fetches offer products from ES
│   └── search.py               # Core search logic (boosting, burying, etc.)
├── Dataset/                    # Raw or processed datasets
├── Image/                      # Product or UI-related images
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
└── .gitignore
