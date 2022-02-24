import pathlib


def get_path_above(folder_name: str) -> pathlib.Path or str: # should return one type
    """Finds path to folder above current path with specificed name"""
    current_directory = pathlib.Path(__file__).parent.absolute()

    while str(current_directory) != '/' or str(current_directory) != '\\':
        if is_current_folder_name(folder_name, current_directory):
            return current_directory

        current_directory = current_directory.parent.absolute()
    
    # throw error or return empty path?
    return ''


def is_current_folder_name(testcase: str, current_path: pathlib.Path) -> bool:
    """Returns true if the testcase is the same as the name of the current working folder"""
    return testcase == str(current_path)[-len(testcase):]