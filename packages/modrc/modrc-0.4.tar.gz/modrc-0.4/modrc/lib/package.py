import yaml

from modrc import exceptions
from modrc.lib import helper


def create_package(package_name, repo_url=None):
    """Create a new ModRC package.

    Parameters
    ----------
    package_name : str
        The name of the new package.
    repo_url : str
        The URL of the packages repository.

    Returns
    -------
    :obj:`Path`
        The path to the new package.

    Raises
    ------
    ModRCIntegrityError
        Raised if either the ModRC or packages directory do not exist.
    """
    # get the packges directory
    packages_dir = helper.get_packages_dir()
    # define the package directories and files
    new_package_dir = packages_dir.joinpath(package_name)
    new_package_yml = new_package_dir.joinpath('package.yml')
    # create the package directories and files
    new_package_dir.mkdir()
    new_package_yml.touch()
    # add the repo url to package.yml if it was passed into the method
    if repo_url is not None:
        package_file = new_package_dir.joinpath('package.yml')
        with open(str(package_file), 'r') as yf:
            package_yaml = yaml.safe_load(yf)
            if package_yaml is None:
                package_yaml = {}
        package_yaml['repourl'] = repo_url
        # write to the package.yml
        with open(str(package_file), 'w') as yf:
            yaml.safe_dump(package_yaml, yf, default_flow_style=False)
    return new_package_dir

def get_package(package_name):
    """Get a package by name.

    Parameters
    ----------
    package_name : str
        The name of the package to get.

    Returns
    -------
    :obj:`Path`
        The path to the package

    Raises
    ------
    ModRCIntegrityError
        Raised if the packages directory does not exist.
    ModRCPackageDoesNotExistError
        Raised if the package does not exist.
    """
    packages_dir = helper.get_packages_dir()
    new_package_dir = packages_dir.joinpath(package_name)
    if not new_package_dir.is_dir():
        raise exceptions.ModRCPackageDoesNotExistError('Package does not exist')
    return new_package_dir

def get_package_file(package_name):
    """Get a package.yml file by package name.

    Parameters
    ----------
    package_name : str
        The name of the package to the package.yml file from.

    Returns
    -------
    :obj:`Path`
        The path to the package.yml file.

    Raises
    ------
    ModRCIntegrityError
        Raised if the packages directory does not exist.
    ModRCPackageDoesNotExistError
        Raised if the package or package.yml file does not exist.
    """
    package_dir = get_package(package_name)
    package_file = package_dir.joinpath('package.yml')
    if not package_file.is_file():
        raise exceptions.ModRCPackageDoesNotExistError
    return package_file
