import click
from clint import textui

from modrc import exceptions
from modrc.lib import setup as modrc_setup
from modrc.lib import package as modrc_package


@click.group()
def setup():
    """Install or uninstall ModRC."""
    pass

@setup.command()
def install():
    """Install ModRC into the current user's home folder."""
    # SETUP
    # get the debug context
    debug = click.get_current_context().obj['debug']

    # INTERACTIVE
    # choose package creation or installation
    package_name, repo_url = prompt_package_creation_installation()
    # choose the default editor
    editor = textui.prompt.query('File editor', default='vim')
    # choose to automatically compile default package changes
    auto_compile = textui.prompt.yn('Automatically compile changes', default='y')
    # choose to automatically sync default package changes
    auto_sync = textui.prompt.yn('Automatically sync changes', default='y')

    # INSTALLATION
    # try to install ModRC
    success = True
    try:
        # setup the ModRC dir
        modrc_setup.initial_setup()
        # set the system configuration settings
        modrc_setup.populate_modrc_file(default_package=package_name, editor=editor, auto_compile=auto_compile, auto_sync=auto_sync)
        # create a new package
        if package_name is not None:
            modrc_package.create_package(package_name, repo_url=repo_url)
        # clone an existing package
        elif repo_url is not None:
            # TODO: clone the package from the URL
            pass
    except exceptions.ModRCIntegrityError:
        # re-raise the exception if debugging is on
        if debug:
            raise
        success = False
    # set the default editor

    # FINISH
    # react to the outcome of the installation
    if success:
        textui.puts('ModRC successfully installed at ~/.modrc')
    else:
        textui.puts(textui.colored.red('ModRC is already installed'))

@setup.command()
def uninstall():
    """Uninstall ModRC from the current user's home folder."""
    # context
    debug = click.get_current_context().obj['debug']
    # try to uninstall ModRC
    success = True
    try:
        modrc_setup.teardown()
    except exceptions.ModRCIntegrityError:
        if debug:
            raise
        success = False
    # react to the outcome of the command
    if success:
        textui.puts('ModRC uninstalled at ~/.modrc')
    else:
        textui.puts('ModRC is not currently installed')

def prompt_package_creation_installation():
    package_name = None
    repo_url = None
    # create new package
    if not textui.prompt.yn('Create a new package', default='n'):
        package_name = textui.prompt.query('Package name')
        # add repo to package
        if textui.prompt.yn('Add repo clone URL', default='y'):
            repo_url = textui.prompt.query('Repo clone URL')
    # install existing package
    elif textui.prompt.yn('Add an existing package repo', default='y'):
        repo_url = textui.prompt.query('Repo clone URL')
    return package_name, repo_url
