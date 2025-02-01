from unittest import TestCase
import time
from src.infrastructure.core.HelperTools import (pickle_in, pickle_out, binom, \
    intersect, remNanFromListFloat, remNullItemsFromList, remNanFromDict, \
    remNullItemsFromDict)
from src.utils.logger import logger_decorator

def sample_function_for_timing(x, y):
    time.sleep(0.1)

# Sample functions to test the decorator
@logger_decorator
def add(a, b):
    return a + b

@logger_decorator
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

class TestHelperTools(TestCase):


    def test_binom(self):
        helper_tools_result = binom(6, 3)
        
        self.assertEqual(helper_tools_result, 20)
        
    def test_intersect(self):
        helper_tools_result = intersect({1, 2, 3}, {3, 4, 5})
        
        self.assertEqual(helper_tools_result, [3])
        
    def test_remove_from_lists(self):
        helper_test_result_1 = remNanFromListFloat([float("nan"), 0.3, 1.2, 3.3])
        helper_test_result_2 = remNullItemsFromList([None, 1, 2, 3])
        
        self.assertEqual(helper_test_result_1, [0.3, 1.2, 3.3])
        self.assertEqual(helper_test_result_2, [1, 2, 3])

    def test_remove_from_dicts(self):
        helper_test_result_1 = remNanFromDict({'key1': float("nan"), 'key2': 0.3, 'key3': 1.4})
        helper_test_result_2 = remNullItemsFromDict({'key1': None, 'key2': 0.3, 'key3': 1.4})
        
        self.assertEqual(helper_test_result_1, {'key2': 0.3, 'key3': 1.4})
        self.assertEqual(helper_test_result_2, {'key2': 0.3, 'key3': 1.4})




