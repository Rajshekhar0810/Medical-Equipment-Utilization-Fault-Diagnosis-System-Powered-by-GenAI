
import pandas as pd 
import json 


def load_usage_data(csv_path: str) -> pd.DataFrame:
    """
    Loads usage data from a CSV file into a pandas DataFrame.

    Args:
        csv_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded usage data.
    """
    try:
      return pd.read_csv(csv_path)
    except Exception as e:
        raise RuntimeError(f"Failed to read usage data from CSV: {e}") 

 
def load_device_metadata(json_path: str) -> dict:
    """
    Loads device metadata from a JSON file.

    Args:
        json_path (str): The path to the JSON file.

    Returns:
        dict: The loaded device metadata.
    """
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to read device metadata from JSON: {e}")
    
    
    
# brochure_parser.py = reads what the equipment is supposed to do (limits/specs)

# file_loader.py = reads what the equipment is actually doing (real-time logs)