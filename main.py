from api.brands_api import *
from process_mapping_accept import process_mapping_accept

def main():

    brand_functions = [
        # get_shopify_connected_brands,
        # get_italist_brands,
        # get_culture_kings_brands,
        # get_princess_polly,
        # get_refinery_no_1,
        # get_rustic_marlin,
        # get_uniikpillows,
        # get_doghugscat,
        # get_lapopart,
        # get_liberal_repellent,
        # get_belt_rhinestone,
        # get_thirdlove,
        # get_harpro,
        # get_galaxy_by_harvic,
        # get_mothersgold,
        # get_tictoc,
        # get_petlife,
        # get_lauren_g_adams,
        # get_moonlight_makers,
        # get_bayeas,
        # get_pipa_fine_art,
        # get_onetify,
        # get_mnml,
        # get_moomaya,
        # get_leg_avenue,
        # get_directdeals,
        # get_anna_kaci,
        # get_fine_color_jewels,
        get_fc_design,
    ]

    for fn in brand_functions:
        process_mapping_accept(fn)

if __name__ == '__main__':
    main()