# test_interface.py

class BaseTest:
    def run_test(self):
        """
        Interface that all test will inherit from
        """
        raise NotImplementedError("Each test must implement the 'run_test' method.")
