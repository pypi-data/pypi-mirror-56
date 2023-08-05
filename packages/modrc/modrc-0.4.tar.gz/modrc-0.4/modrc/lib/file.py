import os

from modrc import exceptions
from modrc.lib import helper, package


def create_file(file_name, package_name):
    """Create a new file in a package.

    Parameters
    ----------
    file_name : str
        The name of the file to create.
    package_name : str
        The name of the package that the file will go in.

    Returns
    -------
    :obj:`Path`
        Returns the path to the new file.

    Raises
    ------
    ModRCIntegrityError
        Raised if ModRC is not installed properly.
    ModRCPackageDoesNotExistError
        Raised if the package could not be found.
    ModRCFileExistsError
        Raised if the file already exists in the package.
    """
    # try to get the package
    package_dir = package.get_package(package_name)
    # check if the file already exists
    file_dir = package_dir.joinpath('files', file_name)
    if file_dir.is_dir():
        raise exceptions.ModRCFileExistsError('File already exists')
    # create the file dir
    file_dir.mkdir(parents=True)
    return file_dir

def get_file(file_name, package_name):
    """Retrieve a file from a package.

    Parameters
    ----------
    file_name : str
        The name of the file to retrieve.
    package_name : str
        The name of the package that the file is in.

    Returns
    -------
    :obj:`Path`
        Returns the path to the file.

    Raises
    ------
    ModRCIntegrityError
        Raised if ModRC is not installed properly.
    ModRCPackageDoesNotExistError
        Raised if the package could not be found.
    ModRCFileDoesNotExistError
        Raised if the file of package is not found.
    """
    # try to get the package directory
    package_dir = package.get_package(package_name)
    # try to the file directory
    file_dir = package_dir.joinpath('files', file_name)
    if not file_dir.is_dir():
        raise exceptions.ModRCFileDoesNotExistError('File does not exist')
    return file_dir

def create_file_filter(filter_name, file_name, package_name):
    """Create a new file filter for a file.

    Parameters
    ----------
    filter_name : str
        The name of the new filter.
    file_name : str
        The file to create the filter for.
    package_name : str
        The package that the file is in.

    Returns
    -------
    :obj:`Path`
        Returns the path to the new file filter.

    Raises
    ------
    ModRCIntegrityError
        Raised if ModRC is not installed properly.
    ModRCPackageDoesNotExistError
        Raised if the package could not be found.
    ModRCFileNotFoundError
        Raised if the package or file is not found.
    ModRCFilterNameError
        Raised if the filter name is invalid.
    """
    # try to get the file
    file_dir = get_file(file_name, package_name)
    # validate file filter name
    if not helper.valid_filter_name(filter_name):
        raise exceptions.ModRCFilterNameError('Invalid file filter name')
    # create the file filter
    file_filter = file_dir.joinpath(filter_name)
    file_filter.touch()
    return file_filter

def compile_file(file_name, package_name, system):
    """Compile a given file from a package.

    Parameters
    ----------
    file_name : str
        The name of the file to compile.
    package_name : str
        The name of the package that the file is in.
    system : str
        The version string for the system, same format as filter names.

    Returns
    -------
    :obj:`Path`
        Returns the path to the live file.

    Raises
    ------
    ModRCIntegrityError
        Raised if ModRC is not installed properly.
    ModRCPackageNotFoundError
        Raised if the package could not be found.
    ModRCFileNotFoundError
        Raised if the file or package could not be found.
    ModRCFilterDoesNotExistError
        Raised if no filters exist for the file being compiled.
    """
    # try to get the file
    file_dir = get_file(file_name, package_name)
    # check for filters
    if not os.listdir(str(file_dir)):
        raise exceptions.ModRCFilterDoesNotExistError('No filters exist in the file')
    # create the compiled file
    compiled_file = helper.get_live_dir().joinpath(file_name)
    if compiled_file.exists():
        compiled_file.unlink()
    compiled_file.touch()
    # iterate over all file filters and write their contents to the compiled file
    for file_filter in file_dir.iterdir():
        # skip files that do not match part of the system string
        if str(file_filter.name) != 'global' and system.find(str(file_filter.name)) != 0:
            continue
        # concatenate the filter to the end of the compiled file
        with open(str(compiled_file), 'a') as cf, open(str(file_filter), 'r') as ff:
            for line in ff.readlines():
                cf.write(line)
    # return the path to the compiled file
    return compiled_file

def get_live_file(file_name):
    """Retrieve a live file.

    Parameters
    ----------
    file_name : str
        The name of the live file to retrieve.

    Returns
    -------
    :obj:`Path`
        Returns the path to the live file.

    Raises
    ------
    ModRCIntegrityError
        Raised if ModRC is not installed properly.
    ModRCLiveFileDoesNotExistError
        Raised if the file or package could not be found.
    """
    # try and get the live file
    live_file = helper.get_live_dir().joinpath(file_name)
    if not live_file.is_file():
        raise exceptions.ModRCLiveFileDoesNotExistError('Live file does not exist')
    return live_file
