import sys
import unittest
import os

# 

# Discover all tests in the 'tests' folder
def run_tests():
  # Set the start directory for test discovery
  start_dir = os.path.dirname(__file__)
  print("Running tests in " + start_dir)
  
  # Discover all test cases (files ending with .test.py)')
  test_suite = unittest.defaultTestLoader.discover(start_dir, pattern='*.test.py', top_level_dir=start_dir)
  
  # Run the discovered test cases
  runner = unittest.TextTestRunner()
  runner.run(test_suite)

# Run the tests if this script is executed directly
if __name__ == '__main__':
  sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../main')))
  run_tests()