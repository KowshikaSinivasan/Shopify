# utils/auth.py
from elasticsearch import Elasticsearch
import urllib3
import streamlit as st

# Disable SSL warnings (for local dev)
urllib3.disable_warnings()

# ES connection
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "kowsh@123"),
    verify_certs=False
)

# Authenticate user
def authenticate_user(user_id, password):
    try:
        response = es.search(
            index="user_password",
            body={
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"user_id.keyword": user_id}},
                            {"term": {"password": int(password)}}
                        ]
                    }
                }
            }
        )
        return response["hits"]["total"]["value"] > 0
    except Exception as e:
        st.error(f"Error connecting to Elasticsearch: {e}")
        return False

# Fetch user info
def user_info(user_id):
    try:
        res = es.search(
            index="users",
            body={
                "query": {
                    "term": {"user_id.keyword": user_id}
                }
            }
        )
        if res["hits"]["total"]["value"] > 0:
            user_data = res["hits"]["hits"][0]["_source"]
            st.session_state["user_id"] = user_data.get("user_id", "")
            st.session_state["user_name"] = user_data.get("name", "")
            st.session_state["user_phone"] = user_data.get("phone", "")
            st.session_state["user_email"] = user_data.get("email", "")
            st.session_state["age"] = user_data.get("age", "")
            st.session_state["country"] = user_data.get("country", "")
            st.session_state["region"] = user_data.get("region", "")
            st.session_state["gender"] = user_data.get("gender", "")
        else:
            st.warning("⚠️ No user details found.")
    except Exception as e:
        st.error(f"Error fetching user info: {e}")
