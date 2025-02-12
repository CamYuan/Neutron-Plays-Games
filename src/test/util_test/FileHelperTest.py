from pathlib import Path
import unittest
import os
from util import saveFile, loadFile

class FileHelperTest(unittest.TestCase):

    def test_save_and_load_file(self):
        # Define some sample data
        data = {'name': 'John', 'age': 30}
        filename = 'test_file'

        # Call saveFile to save data
        file_path = saveFile(filename, data)

        # Load the data back using loadFile
        loaded_data = loadFile(file_path)

        # Test if the data saved and loaded is the same
        self.assertEqual(data, loaded_data)

        # Clean up: remove the test file after the test
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    unittest.main()