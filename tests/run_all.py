import unittest

def parsesql_test_suite():
    """Test suite for parsesql tests"""
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('.')
    return test_suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(parsesql_test_suite())
    