import os
import json
import time
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

BASE_URL = os.getenv('BASE_URL')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
APP_PLATFORM = os.getenv('APP_PLATFORM')
WEB_VERSION = os.getenv('WEB_VERSION')
DEVICE_FP = os.getenv('DEVICE_FP')
REFRESH_TOKEN_PATH = os.getenv('REFRESH_TOKEN_PATH')
ACCESS_TOKEN_FILE_PATH = os.getenv('ACCESS_TOKEN_FILE_PATH')
TOKEN_FILE = os.getenv("ACCESS_TOKEN_FILE_PATH", "token.json")
X_FLIPINATOR_TOOLS = os.getenv('X_FLIPINATOR_TOOLS')

def store_token_data(data):
    with open(TOKEN_FILE, 'w') as file:
        json.dump(data, file)

def load_token_data():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as file:
            return json.load(file)
    return None

def is_token_valid(token_data):
    # current time in milliseconds
    current_time = int(time.time() * 1000)
    return token_data and current_time < token_data['data']['auth']['expiresAt']

def refresh_access_token():
    url = f'{BASE_URL}{REFRESH_TOKEN_PATH}'
    headers = {
        "App-Platform": APP_PLATFORM,
        "web-version": WEB_VERSION,
        "device-fp": DEVICE_FP,
        "x-flipinator-tools": X_FLIPINATOR_TOOLS
    }
    params = {
        "refreshToken": REFRESH_TOKEN
    }
    response = requests.post(url=url, headers=headers, json=params)
    if response.status_code == 200:
        token_data = response.json()
        store_token_data(token_data)
        return token_data['data']['auth']['accessToken']

    logger.error(f"Failed to refresh access token. Status code: {response.status_code}")
    return None

def get_flip_access_token():
    token_data = load_token_data()
    if token_data and is_token_valid(token_data):
        return token_data['data']['auth']['accessToken']
    logger.info("Access token is missing or expired. Refreshing token...")
    return refresh_access_token()

def get_headers(token):
    token = get_flip_access_token()
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {token}",
        "x-flipinator-tools": X_FLIPINATOR_TOOLS
    }
    return headers

if __name__ == "__main__":
    token = get_flip_access_token()
    if token:
        print("Access token retrieved:", token)
    else:
        print("Failed to retrieve access token")