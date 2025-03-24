from utils.api_utils import get_brands_list, call_product_mapping_list, get_detailed_mapping, accept_mapping
import json
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_eligible_variants(brand_id):
    """
    Extract all eligible variants from a brand regardless of parent flags.
    This bypasses the parent validation and directly looks at variant eligibility.
    """
    eligible_variants = []
    
    # Step 1: Get all parent mappings
    mapping_list_response = call_product_mapping_list(brand_id)
    if not mapping_list_response:
        logger.error(f"Failed to retrieve product mapping list for brand {brand_id}")
        return eligible_variants
    
    parent_mappings = mapping_list_response.get("data", [])
    if not parent_mappings:
        logger.info(f"No product mappings found for brand {brand_id}")
        return eligible_variants
    
    logger.info(f"Found {len(parent_mappings)} parent mappings for brand {brand_id}")
    
    # Step 2: Check each parent's variants, regardless of parent eligibility
    for parent in parent_mappings:
        external_id = parent.get("id")
        parent_title = parent.get("externalProduct", {}).get("title", "Unknown Product")
        
        logger.info(f"Checking variants for parent: {parent_title} (ID: {external_id})")
        
        # Get detailed mapping
        detailed_mapping = get_detailed_mapping(external_id, brand_id)
        if not detailed_mapping:
            logger.error(f"Failed to get detailed mapping for parent {external_id}")
            continue
        
        # Extract variants
        detailed_data = detailed_mapping.get("data", {})
        variants_obj = detailed_data.get("variants", {})
        variants_list = variants_obj.get("data", [])
        
        if not variants_list:
            logger.info(f"No variants found for parent {external_id}")
            continue
        
        logger.info(f"Found {len(variants_list)} variants for parent {external_id}")
        
        # Check each variant directly
        variant_count = 0
        eligible_count = 0
        
        for variant in variants_list:
            variant_count += 1
            item_mapping = variant.get("itemMapping", {})
            variant_title = variant.get("title", "Unknown Variant")
            
            # Check if this variant meets ALL criteria
            if (item_mapping.get("allInformationForImportProvided") is True and
                item_mapping.get("prefilledValuesVerified") is True and
                item_mapping.get("dataPrefillingFinished") is True and
                item_mapping.get("allMandatoryAttributesConfigured") is True):
                
                mapping_id = item_mapping.get("id")
                if mapping_id:
                    eligible_count += 1
                    logger.info(f"Variant '{variant_title}' with mapping ID {mapping_id} is eligible for approval")
                    eligible_variants.append(mapping_id)
                else:
                    logger.warning(f"Variant {variant_title} has no mapping ID")
            else:
                # Log which flags are failing
                failing_flags = []
                if item_mapping.get("allInformationForImportProvided") is not True:
                    failing_flags.append("allInformationForImportProvided")
                if item_mapping.get("prefilledValuesVerified") is not True:
                    failing_flags.append("prefilledValuesVerified")
                if item_mapping.get("dataPrefillingFinished") is not True:
                    failing_flags.append("dataPrefillingFinished")
                if item_mapping.get("allMandatoryAttributesConfigured") is not True:
                    failing_flags.append("allMandatoryAttributesConfigured")
                
                logger.info(f"Variant '{variant_title}' does not meet all criteria. Failed flags: {', '.join(failing_flags)}")
        
        logger.info(f"Parent {external_id}: {eligible_count} of {variant_count} variants are eligible for approval")
    
    return eligible_variants

def approve_variants_in_batches(eligible_variants, batch_size=10):
    """
    Approve variants in batches to avoid overwhelming the API
    """
    total_variants = len(eligible_variants)
    logger.info(f"Preparing to approve {total_variants} eligible variants in batches of {batch_size}")
    
    approved_count = 0
    
    # Process in batches
    for i in range(0, total_variants, batch_size):
        batch = eligible_variants[i:i+batch_size]
        
        logger.info(f"Processing batch {i//batch_size + 1} of {(total_variants + batch_size - 1) // batch_size} with {len(batch)} variants")
        
        # Call the accept mapping endpoint
        accept_response = accept_mapping(batch)
        
        if accept_response and accept_response.get("data"):
            success_count = sum(1 for item in accept_response.get("data", []) if item.get("success", False))
            approved_count += success_count
            
            logger.info(f"Successfully approved {success_count} out of {len(batch)} variants in this batch")
            
            # Log any errors
            errors = accept_response.get("errors", [])
            if errors:
                logger.error(f"Errors during approval: {json.dumps(errors, indent=2)}")
        else:
            logger.error(f"Batch approval failed")
        
        # Small delay between batches
        if i + batch_size < total_variants:
            logger.info("Waiting 2 seconds before processing next batch...")
            time.sleep(2)
    
    return approved_count

def main():
    """
    Main workflow to process brands and approve eligible product mappings.
    """
    logger.info("Starting product mapping approval workflow")
    
    # Get brands list
    brands_data = get_brands_list()
    if not brands_data:
        logger.error("No brands data retrieved. Exiting.")
        return
    
    brands_list = brands_data.get("data", [])
    if not brands_list:
        logger.info("No brands found in the response. Exiting.")
        return
    
    logger.info(f"Retrieved {len(brands_list)} brands")
    
    # Track total approvals
    total_approved = 0
    
    # Process each eligible brand
    for brand in brands_list:
        brand_id = brand.get("id")
        brand_name = brand.get("name", "Unknown Brand")
        integration_completed = brand.get("integrationCompleted") is True
        unapproved_items_no = brand.get("unapprovedItemsNo", 0)
        
        if integration_completed and unapproved_items_no > 0:
            logger.info(f"Processing brand: {brand_name} (ID: {brand_id}) with {unapproved_items_no} unapproved items")
            
            # Get all eligible variants regardless of parent status
            eligible_variants = extract_eligible_variants(brand_id)
            
            if eligible_variants:
                logger.info(f"Found {len(eligible_variants)} eligible variants for brand {brand_name}")
                
                # Approve the variants in batches
                approved = approve_variants_in_batches(eligible_variants)
                total_approved += approved
                
                logger.info(f"Approved {approved} variants for brand {brand_name}")
            else:
                logger.info(f"No eligible variants found for brand {brand_name}")
        else:
            logger.info(f"Skipping brand {brand_id} ({brand_name}) - " +
                       f"Integration completed: {integration_completed}, Unapproved items: {unapproved_items_no}")
    
    logger.info(f"Workflow completed. Total approved items: {total_approved}")

if __name__ == "__main__":
    main()