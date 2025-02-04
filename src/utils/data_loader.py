import pandas as pd
from src.domain.models.charging_station import ChargingStation, Location


class DataLoader:
    @staticmethod
    def load_stations(file_path: str) -> list[ChargingStation]:
        stations = []
        data = pd.read_csv(file_path)
        for _, row in data.iterrows():
            location = Location(row['latitude'], row['longitude'])
            # available ports equivalent to number of charging stations in a postal code
            station = ChargingStation(row['Postleitzahl'], location=row['Anzahl Ladepunkte'])
            stations.append(station)
        return stations