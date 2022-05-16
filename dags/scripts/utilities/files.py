import csv
import pathlib


def csv_to_dict(csv_file: pathlib.Path) ->list[dict[str, str]]:
    """Converts a .csv file to an array of dictionaries"""
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        output_dict = [row for row in reader]
    
    return output_dict