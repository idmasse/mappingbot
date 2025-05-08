import json
import logging
import requests
from api.auth_api import get_headers, get_flip_access_token
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
PRODUCT_MAPPINGS_PATH = '/shop/admin/product-mappings/v1'
PRODUCT_MAPPING_VARIANTS_PATH = '/shop/admin/product-mappings/{product_id}/variants/v1'
ACCEPT_MAPPING_PATH = '/shop/brand/items-mapping/accept/v1'
LIMIT = 50

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

def get_product_mappings(item_brand_id, brand_name, token):
    all_mappings = []
    page = 1

    while True:
        url = f"{BASE_URL}{PRODUCT_MAPPINGS_PATH}"
        headers = get_headers(token)
        payload = {"page": page, "limit": LIMIT, "itemBrandId": item_brand_id}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            try:
                data = response.json().get("data", [])
            except json.JSONDecodeError:
                logger.error(f"Product mappings response is not valid JSON for {brand_name} ({item_brand_id})")
                break
        else:
            logger.error(f"Product mappings API call failed for {brand_name} ({item_brand_id}) on page {page} with status code: {response.status_code}")
            break

        if not data:
            logger.info(f"No more product mappings data on {page} for {brand_name} ({item_brand_id})")
            break

        all_mappings.extend(data)
        logger.info(f"Fetched {len(data)} product mappings from {page} for {brand_name} ({item_brand_id})")

        # If the number of items is less than the limit its probably last page.
        if len(data) < LIMIT:
            break

        page += 1

    return all_mappings

def get_product_variants(product_id, token):
    all_variants = []
    page = 1

    while True:
        url = f"{BASE_URL}{PRODUCT_MAPPING_VARIANTS_PATH}".format(product_id=product_id)
        headers = get_headers(token)
        payload = {"page": page, "limit": LIMIT}
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code in (200, 201):
            try:
                data = response.json().get("data", [])
            except json.JSONDecodeError:
                logger.error(f"product variants response is not valid JSON for product id: {product_id} on page {page}")
                break
        else:
            logger.error(f"product variants API call failed for product id {product_id} on page {page} with status code: {response.status_code}")
            break

        if not data:
            logger.info(f"no more variants data on page {page} for product id: {product_id}")
            break

        all_variants.extend(data)
        logger.info(f"fetched {len(data)} variants from page {page} for product id: {product_id}")

        if len(data) < LIMIT:
            break

        page += 1

    return all_variants

# /shop/brand/items-mapping/accept/v1
def accept_item_mappings(item_ids, token, retry=True):
    url = f"{BASE_URL}{ACCEPT_MAPPING_PATH}"
    headers = get_headers(token)
    payload = {"itemIds": item_ids}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code in (200, 201):
        return response.json()

    elif response.status_code == 401 and retry:
        logger.error("received 401 response - attempting to refresh access token and retry")
        new_token = get_flip_access_token()
        if new_token and new_token != token:
            #retry the request once with the new token
            return accept_item_mappings(item_ids, new_token, retry=False)
    else:
        logger.error(f"accept mapping API call failed with status code: {response.status_code}")
    return None