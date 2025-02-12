import os
import pickle
import sys
import time
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]
output_dir='output'
output_path=os.path.join(project_root, output_dir)
def saveFile(filename: str, data: any):
  try:
    timeString = time.strftime("%Y%m%d-%H%M%S")
    filename = filename + "_" + timeString + ".pickle"  # Use .pkl as the extension
    file_path = os.path.join(output_path, filename)
    print(file_path)
    with open(file_path, "wb") as pickle_out:
        pickle.dump(data, pickle_out)
    print(f"Data has been successfully saved to {file_path}.")
  except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
    
def loadFile(filename: str):
  try:
    file_path = os.path.join(output_path, filename)
    with open(file_path, "rb") as pickle_in:
        data = pickle.load(pickle_in)
    return data
  except Exception as e:
      print(f"An error occurred while loading the file {filename}: {e}")
      sys.exit(1)
    
  


