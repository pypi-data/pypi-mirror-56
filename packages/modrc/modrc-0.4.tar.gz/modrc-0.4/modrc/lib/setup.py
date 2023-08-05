import pathlib
import shutil
import yaml

from modrc import exceptions
from modrc.lib import helper


def initial_setup(symlink=None):
    """The initial setup process for ModRC to create the ModRC directory and its file structure.

    Parameters
    ----------
    symlink : :obj:`Path` or None
        The path where actual ModRC files exist that should be symlinked to.

    Returns
    -------
    :obj:`Path`
        The path to the newly created ModRC directory

    Raises
    ------
    ModRCIntegrityError
        Raised if the ModRC directory with the specified name already exists.
    """
    # create the modrc directory
    modrc_dir = pathlib.Path('~/.modrc').expanduser()
    if modrc_dir.is_dir():
        raise exceptions.ModRCIntegrityError('A ModRC directory is already here')
    elif symlink is None:
        modrc_dir.mkdir()
    else:
        modrc_dir.symlink_to(symlink.expanduser())
    # create files in the modrc directory
    modrc_file = modrc_dir.joinpath('modrc.yml')
    packages_dir = modrc_dir.joinpath('packages')
    live_dir = modrc_dir.joinpath('live')
    modrc_file.touch()
    packages_dir.mkdir()
    live_dir.mkdir()
    # symlink the ModRC directory if it is not in the user's home directory
    return modrc_dir

def populate_modrc_file(default_package=None, editor=None, auto_compile=None, auto_sync=None):
    """Populate the ModRC file with setup values.

    Parameters
    ----------
    default_package : str, optional
        The default package for this ModRC installation. Will not be modified if None.
    editor : str, optional
        The default editor for this ModRC installation. Will not be modified if None.
    auto_compile : bool, optional
        Should changes to the default package be compiled automatically. Will not be modified if None.
    auto_sync : bool, optional
        Should changes to the default package be synced to the repo automatically. Will not be modified if None.

    Raises
    ------
    ModRCIntegrityError
        Raised if the ModRC directory or file do not exist.
    """
    # open the ModRC file
    modrc_file = helper.get_modrc_file()
    with open(str(modrc_file), 'r') as yf:
        modrc_yaml = yaml.safe_load(yf)
        if modrc_yaml is None:
            modrc_yaml = {}
    # set the default package
    if default_package is not None:
        modrc_yaml['defaultpackage'] = default_package
    # set the editor
    if editor is not None:
        modrc_yaml['editor'] = editor
    # set auto compile
    if auto_compile is not None:
        modrc_yaml['autocompile'] = auto_compile
    # set auto sync
    if auto_sync is not None:
        modrc_yaml['autosync'] = auto_sync
    # write to the ModRC file
    with open(str(modrc_file), 'w') as yf:
        yaml.safe_dump(modrc_yaml, yf, default_flow_style=False)

def teardown(ignore_errors=False):
    """The teardown process for ModRC to delete the ModRC directory and its file structure.

    Parameters
    ----------
    ignore_errors : bool, optional
        Ignore errors for teardown. Defaults to False.

    Returns
    -------
    bool
        Return True if anything was deleted, False if nothing was deleted.

    Raises
    ------
    ModRCIntegrityError
        Raised if there is no ModRC directory to delete.
    """
    # get the ModRC directory path
    modrc_dir = pathlib.Path('~/.modrc').expanduser()
    # delete a symlink
    if modrc_dir.is_symlink():
        modrc_dir.unlink()
        return True
    # delete a directory
    if modrc_dir.is_dir():
        shutil.rmtree(str(modrc_dir))
        return True
    # raise exception if ModRC was not installed and errors should not be ignored
    if ignore_errors:
        return False
    raise exceptions.ModRCIntegrityError('ModRC is not setup')
