import pathlib
from time import gmtime, strftime


def add_datetime_to_path(base_path: pathlib.Path) -> pathlib.Path:
    """
        Joins subdirectories based on current datetime to basepath.

        Format for output path:

        base_path/year/month/day/hour
    """

    current_time = gmtime()
    year = strftime('%Y', current_time)
    month = strftime('%m', current_time)
    day = strftime('%d', current_time)
    hour = strftime('%H', current_time) #what if hour somehow overlaps? and something so no overwrite? pass hour in from airflow?
    
    return pathlib.Path(base_path, year, month, day, hour)


def get_path_above(folder_name: str) -> pathlib.Path:
    """
        Finds path to folder above current path with specificed name

        Raises ValueError if it does not find the specified path
    """

    current_directory = pathlib.Path(__file__).parent.absolute()

    while str(current_directory) != '/' or str(current_directory) != '\\':
        if is_current_folder_name(folder_name, current_directory):
            return current_directory

        current_directory = current_directory.parent.absolute()
    
    # throw error or return empty path? correct value type?
    raise ValueError
    # return ''


def is_current_folder_name(testcase: str, current_path: pathlib.Path) -> bool:
    """Returns true if the testcase is the same as the name of the current working folder"""

    return testcase == str(current_path)[-len(testcase):]
