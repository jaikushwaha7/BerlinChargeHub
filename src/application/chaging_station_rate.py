
class RatingRepository:
    async def save_rating(self, rating):
        pass

    async def get_ratings_for_station(self, station_id: str):
        return []


from src.domain.models.charging_station import ChargingStation

class ChargingStationRepository:
    station: ChargingStation

    async def find_by_postal_code(self, postal_code: str) -> ChargingStation:
        raise NotImplementedError("This method needs to be implemented.")

    async def update(self, station: ChargingStation) -> None:
        raise NotImplementedError("This method needs to be implemented.")


class RatingUseCase:
    def __init__(
        self,
        station_repository: ChargingStationRepository,
        rating_repository: RatingRepository
    ):
        self.station_repository = station_repository
        self.rating_repository = rating_repository

    async def rate_station(
        self,
        station_id: str,
        user_id: str,
        stars: int,
        review: Optional[str] = None
    ) -> None:
        if not 1 <= stars <= 5:
            raise ValueError("Stars must be between 1 and 5")

        rating = Rating(
            id=str(uuid.uuid4()),
            user_id=user_id,
            station_id=station_id,
            stars=stars,
            review=review,
            created_at=datetime.now()
        )

        await self.rating_repository.save_rating(rating)
        await self._update_station_average_rating(station_id)

    async def _update_station_average_rating(self, station_id: str) -> None:
        ratings = await self.rating_repository.get_ratings_for_station(station_id)
        average = sum(rating.stars for rating in ratings) / len(ratings)
        station = await self.station_repository.find_by_postal_code(station_id)
        station.average_rating = average
        await self.station_repository.update(station)