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
        get_lapopart,
        # get_rustic_marlin,
        # get_petlife
    ]

    for fn in brand_functions:
        process_mapping_accept(fn)

if __name__ == '__main__':
    main()