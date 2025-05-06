import json
import logging
import requests
from dotenv import load_dotenv
from utils.flip_auth import get_flip_access_token, get_headers
import os

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
BRANDS_LIST_PATH = '/shop/admin/brands/onboarding/list/v2'

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_shopify_connected_brands():
    token = get_flip_access_token()
    if not token:
        logger.error("Could not retrieve access token for brands list.")
        return None

    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers(token)
    payload = {
        "page": 1,
        "limit": 50,
        "displayStatus": "live", # live brands only
        "sort": "createdAt",
        "order": "desc",
        "provider": ["shopify"] # connector is shopify
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.error("shopify brands list response is not valid JSON.")
            return None
    else:
        logger.error(f"shopify brands list API call failed with status code: {response.status_code}")
        return None
    
def get_italist_brands():
    token = get_flip_access_token()
    if not token:
        logger.error("Could not retrieve access token for Italist brands list.")
        return None

    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers(token)
    payload = {
        "page": 1,
        "limit": 50,
        "displayStatus": "live", # live brands only
        "sort": "createdAt",
        "order": "desc",
        "platform": ["italist"] # connected platform === italist
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.error("Italist brands list response is not valid JSON.")
            return None
    else:
        logger.error(f"Italist brands list API call failed with status code: {response.status_code}")
        return None
    
def get_culture_kings_brands():
    token = get_flip_access_token()
    if not token:
        logger.error("Could not retrieve access token for Italist brands list.")
        return None

    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers(token)
    payload = {
        "page": 1,
        "limit": 50,
        "displayStatus": "live", # live brands only
        "sort": "createdAt",
        "order": "desc",
        "platform": ["cultureKings"] # connected platform
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.error("brands list response is not valid JSON.")
            return None
    else:
        logger.error(f"brands list API call failed with status code: {response.status_code}")
        return None
    
def get_princess_polly():
    token = get_flip_access_token()
    if not token:
        logger.error("Could not retrieve access token for Italist brands list.")
        return None

    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers(token)
    payload = {
        "page":1,
        "limit":50,
        "name":"Princess Polly", # princess polly only
        "sort":"createdAt",
        "order":"desc"
        }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.error("response is not valid JSON.")
            return None
    else:
        logger.error(f"API call failed with status code: {response.status_code}")
        return None

def get_refinery_no_1():
    token = get_flip_access_token()
    if not token:
        logger.error("Could not retrieve access token for Italist brands list.")
        return None

    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers(token)
    payload = {
        "page":1,
        "limit":50,
        "name":"Refinery Number One", # refinery number one only
        "sort":"createdAt",
        "order":"desc"
        }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.error("response is not valid JSON.")
            return None
    else:
        logger.error(f"API call failed with status code: {response.status_code}")
        return None
    
def get_rustic_marlin():
    token = get_flip_access_token()
    if not token:
        logger.error("Could not retrieve access token for Italist brands list.")
        return None

    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers(token)
    payload = {
        "page":1,
        "limit":50,
        "name":"Rustic Marlin", # rustic marlin only
        "sort":"createdAt",
        "order":"desc"
        }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.error("response is not valid JSON.")
            return None
    else:
        logger.error(f"API call failed with status code: {response.status_code}")
        return None