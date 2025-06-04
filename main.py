from api.brands_api import *
from process_mapping_accept import process_mapping_accept

def main():

    brand_functions = [
        # get_belt_rhinestone,
        # get_liberal_repellent,
        # get_galaxy_by_harvic,
        # get_harpro,
        # get_mothersgold,
        # get_tictoc,
        # get_thirdlove,
        # get_lapopart,
        # get_rustic_marlin,
        # get_petlife,
        # get_lauren_g_adams,
        # get_moonlight_makers,
        # get_bayeas,
        # get_onetify,
        # get_mnml,
        # get_pipa_fine_art,
        get_moomaya, #4.4k
        get_leg_avenue, #1.6k
    ]

    for fn in brand_functions:
        process_mapping_accept(fn)

if __name__ == '__main__':
    main()