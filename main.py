import logging
import os

import pandas as pd

from src.utils.database_utils import init_db

# -----------------------------------------------------------------------------

currentWorkingDirectory = os.path.dirname(os.path.abspath(__file__))

os.chdir(currentWorkingDirectory)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            os.path.join(currentWorkingDirectory, 'log', f"app_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.log"),
            mode='w')
    ]
)
logging.info(f"Current working directory: {os.getcwd()}")

import pandas as pd
from src.infrastructure.core import methods as m1
from src.infrastructure.core import HelperTools as ht

from config import pdict


# -----------------------------------------------------------------------------
@ht.timer
def main():
    """ Main: Generation of Streamlit App for visualizing electric charging stations & residents in Berlin """
    logging.info("Starting execution of the main function.")

    try:
        df_geodat_plz = pd.read_csv(f'{currentWorkingDirectory}\datasets\geodata_berlin_plz.csv', delimiter=';')  #
        logging.info("geodata_berlin_plz.csv loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load geodata_berlin_plz.csv: {str(e)}")
        raise

    try:
        df_lstat = pd.read_csv(f'{currentWorkingDirectory}\datasets\Ladesaeulenregister.csv', delimiter=';')  #
        logging.info("Ladesaeulenregister.csv loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load Ladesaeulenregister.csv: {str(e)}")
        raise
    df_lstat2 = m1.preprop_lstat(df_lstat, df_geodat_plz, pdict)  #
    gdf_lstat3 = m1.count_plz_occurrences(df_lstat2)  #

    try:
        df_residents = pd.read_csv(f'{currentWorkingDirectory}\datasets\plz_einwohner.csv')  ##
        logging.info("plz_einwohner.csv loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load plz_einwohner.csv: {str(e)}")
        raise
    gdf_residents2 = m1.preprop_resid(df_residents, df_geodat_plz, pdict)

    # -----------------------------------------------------------------------------------------------------------------------

    # Running the streamlit function for the app
    m1.create_electric_charging_residents_heatmap(gdf_lstat3, gdf_residents2, df_lstat )


if __name__ == "__main__":
    init_db()
    main()

