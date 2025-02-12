import unittest
import os

# Discover all tests in the 'tests' folder
def run_tests():
  # Set the start directory for test discovery
  start_dir = os.path.dirname(__file__)
  
  # Discover all test cases (files ending with Test.py)')
  test_suite = unittest.defaultTestLoader.discover(start_dir, pattern='*Test.py')
  
  # Print a summary of the discovered tests
  for test in test_suite._tests:
    print(test)
  
  # Run the discovered test cases
  runner = unittest.TextTestRunner()
  runner.run(test_suite)

# Run the tests if this script is executed directly
if __name__ == '__main__':
  run_tests()