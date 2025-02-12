import unittest
import os
from util import saveFile, loadFile

class FileHelperTest(unittest.TestCase):

  def test_save_and_load_file(self):
    data = {'name': 'John', 'age': 30}
    filename = 'test_file'
    file_path = saveFile(filename, data)
    loaded_data = loadFile(file_path)
    self.assertEqual(data, loaded_data)

    if os.path.exists(file_path):
        os.remove(file_path)

if __name__ == '__main__':
  unittest.main()