from utils.api_utils import get_brands_list, call_product_mapping_list, get_detailed_mapping, accept_mapping, get_italist_brands
import json
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_all_variants(brand_id):
    """
    Extract variants from a brand that have inventory amount of 6 or higher.
    """
    all_variants = []
    
    # get all parent mappings
    mapping_list_response = call_product_mapping_list(brand_id)
    if not mapping_list_response:
        logger.error(f"Failed to retrieve product mapping list for brand {brand_id}")
        return all_variants
    
    parent_mappings = mapping_list_response.get("data", [])
    if not parent_mappings:
        logger.info(f"No product mappings found for brand {brand_id}")
        return all_variants
    
    logger.info(f"Found {len(parent_mappings)} parent mappings for brand {brand_id}")
    
    #process each parent with inventory filtering at parent level
    for parent in parent_mappings:
        external_id = parent.get("id")
        if not external_id:
            logger.warning("Parent missing 'id' field, skipping")
            continue
            
        parent_title = parent.get("externalProduct", {}).get("title", "Unknown Product")
        
        # check inventory range, skip if less than 6
        inventory_range = parent.get("inventoryAmountRange", {})
        inventory_min = inventory_range.get("from", 0)
        inventory_max = inventory_range.get("to", 0)
        
        logger.info(f"Parent: {parent_title} - Inventory Range: {inventory_min} to {inventory_max}")
        
        if inventory_min < 6:
            logger.info(f"Parent {parent_title} has inventory min ({inventory_min}) less than 6, checking individual variants")
        
        # get detailed mapping for all parents, as individual variants might still have sufficient inventory
        detailed_mapping = get_detailed_mapping(external_id, brand_id)
        if not detailed_mapping:
            logger.error(f"Failed to get detailed mapping for parent {external_id}")
            continue
        
        # check if we have data
        if "data" not in detailed_mapping:
            logger.error(f"Missing 'data' key in detailed mapping for parent {external_id}")
            continue
            
        # extract variants
        detailed_data = detailed_mapping.get("data", {})
        
        # check for variants
        if "variants" not in detailed_data:
            logger.error(f"Missing 'variants' key in detailed data for parent {external_id}")
            continue
            
        variants_obj = detailed_data.get("variants", {})
        
        # check if variants has data
        if "data" not in variants_obj:
            logger.error(f"Missing 'data' key in variants object for parent {external_id}")
            continue
            
        variants_list = variants_obj.get("data", [])
        
        if not variants_list:
            logger.info(f"No variants found for parent {external_id}")
            continue
        
        logger.info(f"Found {len(variants_list)} variants for parent {external_id}")
        
        # process all variants with inventory check
        eligible_count = 0
        skipped_count = 0
        
        for variant in variants_list:
            variant_id = variant.get("id", "No ID")
            variant_title = variant.get("title", "Unknown Variant")
            
            # check variant inventory
            inventory_amount = variant.get("inventoryAmount", 0)
            
            if inventory_amount < 6:
                logger.info(f"Variant '{variant_title}' has inventory ({inventory_amount}) less than 6, skipping")
                skipped_count += 1
                continue
                
            # check for itemMapping
            if "itemMapping" not in variant:
                logger.warning(f"Variant {variant_title} missing 'itemMapping' field, skipping")
                skipped_count += 1
                continue
                
            item_mapping = variant.get("itemMapping", {})
            
            # get the mapping ID for approval
            mapping_id = item_mapping.get("id")
            
            if mapping_id:
                logger.info(f"Variant '{variant_title}' has inventory {inventory_amount} ≥ 6, adding for approval")
                all_variants.append(mapping_id)
                eligible_count += 1
            else:
                logger.warning(f"Variant '{variant_title}' has no mapping ID, skipping")
                skipped_count += 1
        
        logger.info(f"Parent {external_id}: {eligible_count} eligible variants, {skipped_count} skipped due to low inventory or missing mapping ID")
    
    logger.info(f"Total variants with inventory ≥ 6 for brand {brand_id}: {len(all_variants)}")
    return all_variants

def approve_variants_in_batches(eligible_variants, batch_size=10):
    """
    Approve variants in batches to avoid overwhelming the API
    """
    if not eligible_variants:
        logger.warning("No variants provided for approval")
        return 0
        
    total_variants = len(eligible_variants)
    logger.info(f"Preparing to approve {total_variants} variants in batches of {batch_size}")
    
    approved_count = 0
    
    # process in batches
    for i in range(0, total_variants, batch_size):
        batch = eligible_variants[i:i+batch_size]
        
        logger.info(f"Processing batch {i//batch_size + 1} of {(total_variants + batch_size - 1) // batch_size} with {len(batch)} variants")
        
        # call the accept mapping endpoint
        accept_response = accept_mapping(batch)
        
        if accept_response and accept_response.get("data"):
            success_count = sum(1 for item in accept_response.get("data", []) if item.get("success", False))
            approved_count += success_count
            
            logger.info(f"Successfully approved {success_count} out of {len(batch)} variants in this batch")
            
            # log any errors
            errors = accept_response.get("errors", [])
            if errors:
                logger.error(f"Errors during approval: {json.dumps(errors, indent=2)}")
        else:
            logger.error(f"Batch approval failed")
        
        # small delay between batches
        if i + batch_size < total_variants:
            logger.info("Waiting 2 seconds before processing next batch...")
            time.sleep(2)
    
    return approved_count

def main():
    all_brands = []

    # get Shopify brands
    shopify_brands_response = get_brands_list()
    if shopify_brands_response and "data" in shopify_brands_response:
        shopify_brands = shopify_brands_response["data"]
        logger.info(f"Found {len(shopify_brands)} Shopify brands.")
        all_brands.extend(shopify_brands)
    else:
        logger.error("Failed to fetch Shopify brands.")

    # get Italist brands
    italist_brands_response = get_italist_brands()
    if italist_brands_response and "data" in italist_brands_response:
        italist_brands = italist_brands_response["data"]
        logger.info(f"Found {len(italist_brands)} Italist brands.")
        all_brands.extend(italist_brands)
    else:
        logger.error("Failed to fetch Italist brands.")

    logger.info(f"Total brands to process: {len(all_brands)}")
    
    total_variants = 0
    total_approved = 0

    # process all brands
    for brand in all_brands:
        brand_id = brand.get("id")
        brand_name = brand.get("name", "Unknown Brand")

        logger.info(f"Processing brand: {brand_name} (ID: {brand_id})")

        variants = extract_all_variants(brand_id)
        if variants:
            total_variants += len(variants)
            approved = approve_variants_in_batches(variants)
            total_approved += approved
            logger.info(f"Approved {approved} out of {len(variants)} variants for brand {brand_name}.")
        else:
            logger.info(f"No variants found for brand {brand_name}.")
    
    logger.info(f"Process complete. Attempted to approve {total_variants} variants across all brands.")
    logger.info(f"Successfully approved {total_approved} variants in total.")

if __name__ == "__main__":
    main()