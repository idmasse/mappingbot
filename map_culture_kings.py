import time
import logging
from api.auth_api import get_flip_access_token
from api.brands_api import get_culture_kings_brands
from api.mapping_api import get_product_mappings, get_product_variants, accept_item_mappings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_mapping_accept():
    """
    This function chains all API calls:
      - Retrieves an access token
      - Retrieves brand ID(s)
      - Requests the product mappings pages to get product ids
      - For each product id, retrieves the variants itemMapping ids for variants with sufficient inventory
      - Calls the accept endpoint with all the collected itemMappin ids in batches
      - Stops accepting once TARGET successes have been reached, logging total counts
    """
    token = get_flip_access_token()
    if not token:
        logger.error("Failed to retrieve flip access token.")
        return

    brands_response = get_culture_kings_brands()
    if not brands_response or "data" not in brands_response:
        logger.error("No brands data found.")
        return

    all_item_mapping_ids = []

    for brand in brands_response["data"]:
        brand_id = brand.get("id")
        brand_name = brand.get('name')
        if not brand_id:
            logger.warning("Brand missing id, skipping")
            continue

        logger.info(f"Processing brand {brand_name} ({brand_id})")
        
        # get all product mappings for the brand
        product_mappings = get_product_mappings(brand_id, brand_name, token)
        if not product_mappings:
            logger.warning(f"No product mappings data found for {brand_name} ({brand_id})")
            continue

        # get each product id
        for product in product_mappings:
            product_id = product.get("id")
            if not product_id:
                logger.warning("Product mapping entry missing id. Skipping product")
                continue

            logger.info(f"Processing product mapping id: {product_id}")
            
            # retrieve all variants for each product id
            variants = get_product_variants(product_id, token)
            if not variants:
                logger.warning(f"No variants data found for product id: {product_id}")
                continue

            # get the "itemMapping" ids from each variant only if inventory > 6
            for variant in variants:
                inventory = variant.get("inventoryAmount", 0)
                if inventory > 6:
                    item_mapping = variant.get("itemMapping")
                    if item_mapping and "id" in item_mapping:
                        item_mapping_id = item_mapping["id"]
                        all_item_mapping_ids.append(item_mapping_id)
                        logger.info(f"Collected itemMapping id: {item_mapping_id} from a variant with inventory {inventory}")
                    else:
                        logger.warning(f"Variant in product id {product_id} is missing itemMapping data")
                else:
                    logger.info(f"Skipping variant in product id {product_id} because inventory is {inventory}")

    # process and accept the collected item mapping ids in batches and stop at TARGET
    batch_size = 30
    total_items = len(all_item_mapping_ids)
    accepted_count = 0
    TARGET = 4000

    if total_items:
        logger.info(f"Total collected itemMapping ids: {total_items} for {brand_name} ({brand_id})")
        for i in range(0, total_items, batch_size):
            if accepted_count >= TARGET:
                logger.info(f"Reached target of {TARGET} accepted items; stopping further accepts")
                break

            batch_ids = all_item_mapping_ids[i:i+batch_size]
            logger.info(f"Accepting batch of {len(batch_ids)} itemMapping ids: {batch_ids}")
            accept_response = accept_item_mappings(batch_ids, token)
            if accept_response:
                logger.info(f"Successfully accepted batch - response: {accept_response}")
                # count successes and failures for batch
                data = accept_response.get("data", [])
                errors = accept_response.get("errors", [])

                # True==1, False==0
                successes = sum(success.get("success", False) for success in data)
                failures  = sum(not failure.get("success", True)  for failure in errors)

                accepted_count += successes
                logger.info(f"Batch result for {brand_name}: {successes} succeeded, {failures} failed; total accepted: {accepted_count}")
            else:
                logger.error(f"Failed to accept batch of itemMapping ids: {batch_ids}")
            time.sleep(1) # ico rate limits
    else:
        logger.warning("No itemMapping ids collected for acceptance")

if __name__ == "__main__":
    process_mapping_accept()