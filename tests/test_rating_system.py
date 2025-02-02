from unittest import TestCase

from src.domain.models.rating_system import Rating


class TestRating(TestCase):

    def test_initialization_with_required_fields(self):
        rating = Rating(
            id="1",
            user_id="user123",
            station_id="station456",
            stars=5,
            review="Test review"
        )
        self.assertEqual(rating.id, "1")
        self.assertEqual(rating.user_id, "user123")
        self.assertEqual(rating.station_id, "station456")
        self.assertEqual(rating.stars, 5)

    def test_stars_valid_range(self):
        for star_rating in range(1, 6):  # Assuming valid star ratings are 1 through 5
            rating = Rating(
                id="1",
                user_id="user123",
                station_id="station456",
                stars=star_rating,
                review="Test review"
            )
            self.assertEqual(rating.stars, star_rating)

    def test_invalid_star_rating(self):
        with self.assertRaises(TypeError):  # Validator logic might not raise ValueError
            Rating(
                id="1",
                user_id="user123",
                station_id="station456",
                stars=6,  # Invalid star value as an example
                review="Test review"
            )
