import pathlib
from dateutil import parser
from time import gmtime, strftime

# update
def add_datetime_to_path(base_path: pathlib.Path, datetime: str) -> pathlib.Path:
    """
        Joins subdirectories based on current datetime to basepath.

        Format for output path:

        base_path/year/month/day/hour
    """
    dt = parser.parse(datetime)
    year = dt.strftime('%Y')
    month = dt.strftime('%m')
    day = dt.strftime('%d')
    hour = dt.strftime('%H') #what if hour somehow overlaps? and something so no overwrite? pass hour in from airflow?
    
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


def get_path_with_current_datetime(base_dir_name: str, data_dir_name: str) -> pathlib.Path:
    """
        Finds the base path, adds a sub path, then adds a datetime based series of subpaths

        Example called path below @ 2022-02-22 02:22:22 with 'in_the_news' in path c/

        get_path_with_current_datetime('in_the_news', 'data/scraped')

        Outputs Path:
        c/in_the_news/data/scraped/2022/02/22/02
    """
    #update docstring format?
    app_root_path = get_path_above(base_dir_name) # handle error or wrong path
    data_path = app_root_path.joinpath(data_dir_name)
    return add_datetime_to_path(data_path)


def is_current_folder_name(testcase: str, current_path: pathlib.Path) -> bool:
    """Returns true if the testcase is the same as the name of the current working folder"""

    return testcase == str(current_path)[-len(testcase):]
