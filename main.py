import logging
import os

import pandas as pd

<<<<<<< HEAD
from src.pages.infrastructure.core import HelperTools as ht, methods as m1, UI as m2

from src.config.config import pdict

from src.utils.database_utils import init_db
from src.utils import logger as lg
=======
from src.utils.database_utils import init_db
>>>>>>> 07b7a626c6e11cf03ef32d8f14eed4df8e1bfe74

# -----------------------------------------------------------------------------

currentWorkingDirectory = os.path.dirname(os.path.abspath(__file__))
<<<<<<< HEAD
os.chdir(currentWorkingDirectory)

# -----------------------------------------------------------------------------
@ht.timer
@lg.logger_decorator
=======

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
>>>>>>> 07b7a626c6e11cf03ef32d8f14eed4df8e1bfe74
def main():
    """ Main: Generation of Streamlit App for visualizing electric charging stations & residents in Berlin """
    logging.info("Starting execution of the main function.")

    try:
<<<<<<< HEAD
        df_geodat_plz = pd.read_csv(f'{currentWorkingDirectory}\data\source\geodata_berlin_plz.csv', delimiter=';')  #
=======
        df_geodat_plz = pd.read_csv(f'{currentWorkingDirectory}\datasets\geodata_berlin_plz.csv', delimiter=';')  #
>>>>>>> 07b7a626c6e11cf03ef32d8f14eed4df8e1bfe74
        logging.info("geodata_berlin_plz.csv loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load geodata_berlin_plz.csv: {str(e)}")
        raise

    try:
<<<<<<< HEAD
        df_lstat = pd.read_csv(f'{currentWorkingDirectory}\data\source\Ladesaeulenregister.csv', delimiter=';')  #
=======
        df_lstat = pd.read_csv(f'{currentWorkingDirectory}\datasets\Ladesaeulenregister.csv', delimiter=';')  #
>>>>>>> 07b7a626c6e11cf03ef32d8f14eed4df8e1bfe74
        logging.info("Ladesaeulenregister.csv loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load Ladesaeulenregister.csv: {str(e)}")
        raise
    df_lstat2 = m1.preprop_lstat(df_lstat, df_geodat_plz, pdict)  #
    gdf_lstat3 = m1.count_plz_occurrences(df_lstat2)  #

    try:
<<<<<<< HEAD
        df_residents = pd.read_csv(f'{currentWorkingDirectory}\data\source\plz_einwohner.csv')  ##
=======
        df_residents = pd.read_csv(f'{currentWorkingDirectory}\datasets\plz_einwohner.csv')  ##
>>>>>>> 07b7a626c6e11cf03ef32d8f14eed4df8e1bfe74
        logging.info("plz_einwohner.csv loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load plz_einwohner.csv: {str(e)}")
        raise
    gdf_residents2 = m1.preprop_resid(df_residents, df_geodat_plz, pdict)

    # -----------------------------------------------------------------------------------------------------------------------

    # Running the streamlit function for the app
<<<<<<< HEAD
    m2.create_electric_charging_residents_heatmap(gdf_lstat3, gdf_residents2, df_lstat )
=======
    m1.create_electric_charging_residents_heatmap(gdf_lstat3, gdf_residents2, df_lstat )
>>>>>>> 07b7a626c6e11cf03ef32d8f14eed4df8e1bfe74


if __name__ == "__main__":
    init_db()
    main()

