import logging
from utils.flip_auth import get_flip_access_token
from api.brands_api import get_shopify_connected_brands
from api.mapping_api import get_product_mappings, get_product_variants, accept_item_mappings
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = os.getenv('BASE_URL')

def process_full_mapping_accept():
    """
      - Retrieves brands via get_shopify_connected_brands
      - For each brand, requests its product mappings and collects the product ids
      - For each product mapping ID, retrieves its variants
      - Collects all itemMapping ids from variants (only for variants with inventory > #)
      - Calls the accept mapping endpoint in batches with collected itemMapping ids
    """
    access_token = get_flip_access_token()
    if not access_token:
        logger.error("Failed to retrieve flip access token.")
        return

    brands_response = get_shopify_connected_brands()
    if not brands_response or "data" not in brands_response:
        logger.error("No brands data found.")
        return

    all_item_mapping_ids = []

    # Loop through each brand returned by get_shopify_connected_brands()
    for brand in brands_response["data"]:
        brand_id = brand.get("id")
        brand_name = brand.get('name')
        if not brand_id:
            logger.warning("Brand entry missing 'id'. Skipping this brand.")
            continue

        logger.info(f"Processing brand: {brand_name} / {brand_id}")
        
        # Call product mappings endpoint for the brand
        product_mappings_response = get_product_mappings(brand_id, access_token)
        if not product_mappings_response or "data" not in product_mappings_response:
            logger.warning("No product mappings data found for brand id: %s", brand_id)
            continue

        # Process each product mapping (each product)
        for product in product_mappings_response["data"]:
            product_id = product.get("id")
            if not product_id:
                logger.warning("Product mapping entry missing 'id'. Skipping product.")
                continue

            logger.info(f"Processing product mapping id: {product_id}")
            
            # Retrieve variants for the product mapping
            variants_response = get_product_variants(product_id, access_token)
            if not variants_response or "data" not in variants_response:
                logger.warning(f"No variants data found for product id: {product_id}")
                continue

            # Extract the "itemMapping" ids from each variant only if inventory is sufficient
            for variant in variants_response["data"]:
                inventory = variant.get("inventoryAmount", 0)
                if inventory > 6:
                    item_mapping = variant.get("itemMapping")
                    if item_mapping and "id" in item_mapping:
                        item_mapping_id = item_mapping["id"]
                        all_item_mapping_ids.append(item_mapping_id)
                        logger.info(f"Collected itemMapping id: {item_mapping_id} from a variant with inventory: {inventory}")
                    else:
                        logger.warning(f"Variant in product id {product_id} is missing itemMapping data.")
                else:
                    logger.info(f"Skipping variant in product id {product_id} because inventory is {inventory}")

    # Process and accept the collected item mapping ids in batches
    batch_size = 20
    total_items = len(all_item_mapping_ids)
    if total_items:
        logger.info(f"Total collected itemMapping ids: {total_items}")
        for i in range(0, total_items, batch_size):
            batch_ids = all_item_mapping_ids[i:i+batch_size]
            logger.info(f"Accepting batch of len({batch_ids}) itemMapping ids: {batch_ids}")
            accept_response = accept_item_mappings(batch_ids, access_token)
            if accept_response:
                logger.info(f"Successfully accepted batch. Response: {accept_response}")
            else:
                logger.error(f"Failed to accept batch of itemMapping ids: {batch_ids}")
    else:
        logger.warning("No itemMapping ids collected for acceptance.")

if __name__ == "__main__":
    process_full_mapping_accept()
