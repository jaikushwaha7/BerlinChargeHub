from unittest import TestCase
from unittest.mock import patch, call
import pickle
import time
from core.infrastructure.HelperTools import pickle_in, pickle_out, binom, \
    intersect, remNanFromListFloat, remNullItemsFromList, remNanFromDict, \
    remNullItemsFromDict, timer, logger_decorator

FILENAME = "datasets/pickler.pkl"
TO_SAVE = "This is a string object we will pickle up"

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

    def test_pickling(self):

        # HelperTools result
        pickle_out(TO_SAVE, FILENAME)
        helper_tools_result = pickle_in(FILENAME)
        
        # Ground truth result (actual)
        with open(FILENAME, "wb") as file:
            pickle.dump(TO_SAVE, file)

        with open(FILENAME, 'rb') as file:
            ground_truth_result = pickle.load(file)

        self.assertEqual(helper_tools_result, ground_truth_result)
    
    
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

    @patch('logging.info')  # Mock logging.info
    @patch('logging.error')  # Mock logging.error
    def test_logger_decorator(self, mock_error, mock_info):
        # Test add function (no exception)
        result = add(10, 5)
        self.assertEqual(result, 15)

        # Verify logging calls for add
        mock_info.assert_any_call("Called add with args: (10, 5), kwargs: {}")
        mock_info.assert_any_call("add returned 15")

        # Test divide function (no exception)
        result = divide(10, 2)
        self.assertEqual(result, 5)

        # Verify logging calls for divide
        mock_info.assert_any_call("Called divide with args: (10, 2), kwargs: {}")
        mock_info.assert_any_call("divide returned 5.0")

        # Test divide function (exception raised)
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

        # Verify logging calls for exception
        mock_info.assert_any_call("Called divide with args: (10, 0), kwargs: {}")
        mock_error.assert_called_with("divide raised an exception: Cannot divide by zero")



