from utils.access_token import *
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

# Logging setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_headers(access_token=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": f"{FLIP_URL}",
        "priority": "u=1, i",
        "referer": "https://flipmagic.flip.shop/",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
    }
    
    if access_token:
        headers["authorization"] = f"Bearer {access_token}"
        
    return headers

def get_brands_list():
    """
    Call the brands onboarding API and return its JSON response.
    """
    access_token = get_flip_access_token()
    if not access_token:
        logger.error("Could not retrieve access token for brands list.")
        return None

    url = f"{BASE_URL}/shop/admin/brands/onboarding/list/v2"
    headers = get_headers(access_token)
    payload = {
        "page": 1,
        "limit": 50,  # Increased from 10 to 50 to fetch more brands at once
        "displayStatus": "live",
        "sort": "createdAt",
        "order": "desc",
        "provider": ["shopify"]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.error("Brands list response is not valid JSON.")
            return None
    else:
        logger.error(f"Brands list API call failed with status code: {response.status_code}")
        return None

def call_product_mapping_list(brand_id):
    """
    Call the product mapping list endpoint for the given brand ID.
    """
    access_token = get_flip_access_token()
    if not access_token:
        logger.error("Could not retrieve access token for product mapping list.")
        return None

    url = f"{BASE_URL}/shop/admin/product-mappings/v1"
    headers = get_headers(access_token)
    payload = {
        "page": 1,
        "limit": 50,
        "itemBrandId": brand_id
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.error("Product mapping list response is not valid JSON.")
            return None
    else:
        logger.error(f"Product mapping list API call failed with status code: {response.status_code}")
        return None

def get_detailed_mapping(external_id, brand_id):
    """
    Call the detailed mapping endpoint for a specific parent using its external ID and brand ID.
    """
    access_token = get_flip_access_token()
    if not access_token:
        logger.error("Could not retrieve access token for detailed mapping.")
        return None

    url = f"{BASE_URL}/shop/admin/product-mappings/{external_id}/v1"
    params = {"itemBrandId": brand_id}
    headers = get_headers(access_token)
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.error("Detailed mapping response is not valid JSON.")
            return None
    else:
        logger.error(f"Detailed mapping API call failed with status code: {response.status_code}")
        return None

def accept_mapping(item_mapping_ids):
    """
    Call the accept mapping endpoint for one or more variant itemMapping IDs.
    
    Parameters:
    item_mapping_ids (str or list): A single itemMapping ID or a list of IDs
    """
    access_token = get_flip_access_token()
    if not access_token:
        logger.error("Could not retrieve access token for accepting mapping.")
        return None

    # Convert single ID to list if needed
    if isinstance(item_mapping_ids, str):
        item_mapping_ids = [item_mapping_ids]
    
    url = f"{BASE_URL}/shop/brand/items-mapping/accept/v1"
    headers = get_headers(access_token)
    payload = {"itemIds": item_mapping_ids}
    
    logger.info(f"Accepting mapping for item(s): {item_mapping_ids}")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        try:
            result = response.json()
            logger.info(f"Accept mapping response: {json.dumps(result, indent=2)}")
            return result
        except json.JSONDecodeError:
            logger.error("Accept mapping response is not valid JSON.")
            return None
    else:
        logger.error(f"Accept mapping API call failed with status code: {response.status_code}")
        return None