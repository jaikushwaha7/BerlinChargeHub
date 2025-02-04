import unittest


def is_valid_berlin_postal_code(postal_code):
    # Verify the postal code is numeric and exactly 5 digits
    if not postal_code.isdigit() or len(postal_code) != 5:
        return False

    # Convert to integer
    postal_code = int(postal_code)

    # Check if within Berlin's range
    return 10115 <= postal_code <= 14199


class TestBerlinPostalCode(unittest.TestCase):

    def test_valid_postal_codes(self):
        self.assertTrue(is_valid_berlin_postal_code("10115"))  # Lower limit
        self.assertTrue(is_valid_berlin_postal_code("14199"))  # Upper limit
        self.assertTrue(is_valid_berlin_postal_code("11000"))  # Random valid

    def test_invalid_postal_codes(self):
        self.assertFalse(is_valid_berlin_postal_code("10114"))  # Below range
        self.assertFalse(is_valid_berlin_postal_code("14200"))  # Above range
        self.assertFalse(is_valid_berlin_postal_code("123"))  # Too short
        self.assertFalse(is_valid_berlin_postal_code("123456"))  # Too long
        self.assertFalse(is_valid_berlin_postal_code("ABCDE"))  # Non-numeric

    def test_edge_cases(self):
        self.assertTrue(is_valid_berlin_postal_code("10115"))  # Exact lower bound
        self.assertTrue(is_valid_berlin_postal_code("14199"))  # Exact upper bound
        self.assertFalse(is_valid_berlin_postal_code("010115"))  # Leading zero
        self.assertFalse(is_valid_berlin_postal_code("10115 "))  # Whitespace
        self.assertFalse(is_valid_berlin_postal_code("12$#34"))  # Special characters


if __name__ == "__main__":
    unittest.main()
