import logging
import os

import pandas as pd

from src.pages.infrastructure.core import HelperTools as ht, methods as m1, UI as m2

from src.config.config import pdict

from src.utils.database_utils import init_db
from src.utils import logger as lg

# -----------------------------------------------------------------------------

currentWorkingDirectory = os.path.dirname(os.path.abspath(__file__))
os.chdir(currentWorkingDirectory)

# -----------------------------------------------------------------------------
@ht.timer
@lg.logger_decorator
def main():
    """ Main: Generation of Streamlit App for visualizing electric charging stations & residents in Berlin """
    logging.info("Starting execution of the main function.")

    try:
        df_geodat_plz = pd.read_csv(f'{currentWorkingDirectory}\data\source\geodata_berlin_plz.csv', delimiter=';')  #
        logging.info("geodata_berlin_plz.csv loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load geodata_berlin_plz.csv: {str(e)}")
        raise

    try:
        df_lstat = pd.read_csv(f'{currentWorkingDirectory}\data\source\Ladesaeulenregister.csv', delimiter=';')  #
        logging.info("Ladesaeulenregister.csv loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load Ladesaeulenregister.csv: {str(e)}")
        raise
    df_lstat2 = m1.preprop_lstat(df_lstat, df_geodat_plz, pdict)  #
    gdf_lstat3 = m1.count_plz_occurrences(df_lstat2)  #

    try:
        df_residents = pd.read_csv(f'{currentWorkingDirectory}\data\source\plz_einwohner.csv')  ##
        logging.info("plz_einwohner.csv loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load plz_einwohner.csv: {str(e)}")
        raise
    gdf_residents2 = m1.preprop_resid(df_residents, df_geodat_plz, pdict)

    # -----------------------------------------------------------------------------------------------------------------------

    # Running the streamlit function for the app
    m2.create_electric_charging_residents_heatmap(gdf_lstat3, gdf_residents2, df_lstat )


if __name__ == "__main__":
    init_db()
    main()

