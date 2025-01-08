import unittest
import os
currentWorkingDirectory = os.path.dirname(os.path.abspath(__file__))
os.chdir(currentWorkingDirectory)
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from config import pdict

class TestConfig(unittest.TestCase):

    def test_required_keys_exist(self):
        # Check that all expected keys are in the config dictionary
        expected_keys = [
            'geocode', 
            'file_lstations', 
            'file_residents', 
            'file_geodat_plz', 
            'file_geodat_dis', 
            'file_suggestions', 
            'file_reports'
        ]
        for key in expected_keys:
            self.assertIn(key, pdict, f"Missing key: {key}")

    def test_value_types(self):
        # Test that values are of the expected type
        self.assertIsInstance(pdict['geocode'], str)
        self.assertIsInstance(pdict['file_lstations'], str)
        self.assertIsInstance(pdict['file_residents'], str)
        self.assertIsInstance(pdict['file_geodat_plz'], str)
        self.assertIsInstance(pdict['file_geodat_dis'], str)
        self.assertIsInstance(pdict['file_suggestions'], str)
        self.assertIsInstance(pdict['file_reports'], str)

    def test_non_empty_values(self):
        # Check that all values are non-empty (important for file paths)
        for key in pdict:
            self.assertGreater(len(pdict[key]), 0, f"Value for {key} should not be empty")

    def test_file_paths_exist(self):
        # Ensure that file paths are valid (files exist)
        import os
        self.assertTrue(os.path.exists(pdict['file_residents']), "File not found: file_residents")
        self.assertTrue(os.path.exists(pdict['file_lstations']), "File not found: file_lstations")
        self.assertTrue(os.path.exists(pdict['file_geodat_plz']), "File not found: file_geodat_plz")
        self.assertTrue(os.path.exists(pdict['file_geodat_dis']), "File not found: file_geodat_dis")
        self.assertTrue(os.path.exists(pdict['file_suggestions']), "File not found: file_suggestions")
        self.assertTrue(os.path.exists(pdict['file_reports']), "File not found: file_reports")

if __name__ == '__main__':
    unittest.main()
