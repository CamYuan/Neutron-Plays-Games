from pathlib import Path
import unittest
import os
from util import saveFile, loadFile


project_root = Path(__file__).resolve().parents[2]
output_dir='output'
output_path=os.path.join(project_root, output_dir)
print(output_path)

class FileHelperTest(unittest.TestCase):

    def test_save_and_load_file(self):
        # Define some sample data
        data = {'name': 'John', 'age': 30}
        filename = 'test_file'

        # Call saveFile to save data
        saveFile(filename, data)

        # Load the data back using loadFile
        loaded_data = loadFile(filename)

        # Test if the data saved and loaded is the same
        self.assertEqual(data, loaded_data)

        # Clean up: remove the test file after the test
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == '__main__':
    unittest.main()