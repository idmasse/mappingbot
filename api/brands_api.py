import json
import logging
import requests
from api.auth_api import get_headers
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
BRANDS_LIST_PATH = '/shop/admin/brands/onboarding/list/v2'

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

### GET BY CONNECTOR ###

def get_shopify_connected_brands():
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
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
    
### GET BY CONNECTED PLATFORM ###
    
def get_italist_brands():
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
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
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
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
    
### GET BY BRAND NAME ###
    
def get_princess_polly():
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
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
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
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
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
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
    
def get_uniikpillows():
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
    payload = {
        "page":1,
        "limit":50,
        "name":"UniikPillows",
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

def get_doghugscat():
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
    payload = {
        "page":1,
        "limit":50,
        "name":"Dog Hugs Cat",
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

def get_lapopart():
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
    payload = {
        "page":1,
        "limit":50,
        "name":"Los Angeles Pop Art",
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
    
def get_liberal_repellent():
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
    payload = {
        "page":1,
        "limit":50,
        "name":"Liberal Repellent",
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
    
def get_belt_rhinestone():
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
    payload = {
        "page":1,
        "limit":50,
        "name":"Belt Rhinestone",
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
    
def get_thirdlove():
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
    payload = {
        "page":1,
        "limit":50,
        "name":"Thirdlove",
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
    
def get_harpro():
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
    payload = {
        "page":1,
        "limit":50,
        "name":"Harpro",
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
    
def get_galaxy_by_harvic():
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
    payload = {
        "page":1,
        "limit":50,
        "name":"Galaxy By Harvic",
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
    
def get_mothersgold():
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
    payload = {
        "page":1,
        "limit":50,
        "name":"Mothersgold",
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
    
def get_tictoc():
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
    payload = {
        "page":1,
        "limit":50,
        "name":"Tic Toc",
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
    
def get_petlife():
    url = f"{BASE_URL}{BRANDS_LIST_PATH}"
    headers = get_headers()
    payload = {
        "page":1,
        "limit":50,
        "name":"Pet Life",
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
