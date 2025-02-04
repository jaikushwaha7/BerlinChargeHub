import unittest


class TestDictionary(unittest.TestCase):

    def setUp(self):
        """Set up the dictionary provided in the example."""
        self.p = dict()
        self.p['picklefolder'] = 'pickles'
        self.p['geocode'] = 'PLZ'
        self.p["file_lstations"] = "Ladesaeulenregister.csv"
        self.p["file_residents"] = "plz_einwohner.csv"
        self.p["file_geodat_plz"] = "geodata_berlin_plz.csv"
        self.p["file_geodat_dis"] = "geodata_berlin_dis.csv"
        self.pdict = self.p.copy()

    def test_keys_exist(self):
        """Test that all required keys exist in the dictionary."""
        required_keys = [
            'picklefolder', 'geocode', 'file_lstations',
            'file_residents', 'file_geodat_plz', 'file_geodat_dis'
        ]
        for key in required_keys:
            self.assertIn(key, self.p, f"Key '{key}' is missing from the dictionary.")

    def test_default_values(self):
        """Test that the default values in the dictionary are correct."""
        self.assertEqual(self.p['picklefolder'], 'pickles')
        self.assertEqual(self.p['geocode'], 'PLZ')
        self.assertEqual(self.p["file_lstations"], "Ladesaeulenregister.csv")
        self.assertEqual(self.p["file_residents"], "plz_einwohner.csv")
        self.assertEqual(self.p["file_geodat_plz"], "geodata_berlin_plz.csv")
        self.assertEqual(self.p["file_geodat_dis"], "geodata_berlin_dis.csv")

    def test_copy_dictionary(self):
        """Test that `p.copy()` correctly creates a duplicate dictionary."""
        self.assertEqual(self.p, self.pdict)  # Ensure the copy matches the original
        self.assertIsNot(self.p, self.pdict)  # Ensure it's not the same reference (deep copy)

    def test_file_keys_are_csv(self):
        """Test that file keys have string values ending in `.csv`."""
        file_keys = [
            "file_lstations", "file_residents",
            "file_geodat_plz", "file_geodat_dis"
        ]
        for key in file_keys:
            value = self.p[key]
            self.assertIsInstance(value, str, f"Value of key '{key}' is not a string.")
            self.assertTrue(value.endswith('.csv'), f"Value of key '{key}' is not a valid CSV file.")

    def test_no_empty_values(self):
        """Test that no key in the dictionary has an empty value."""
        for key, value in self.p.items():
            self.assertTrue(value, f"Key '{key}' has an empty or falsy value.")

    def test_file_keys_have_valid_names(self):
        """Test that file keys have meaningful, non-default names."""
        invalid_names = ["file.csv", "data.csv", "unnamed.csv"]
        for key in ["file_lstations", "file_residents", "file_geodat_plz", "file_geodat_dis"]:
            self.assertNotIn(self.p[key], invalid_names, f"Key '{key}' has an invalid name.")
