import click

import modrc
from modrc.commands import setup


@click.group()
@click.option('--debug', is_flag=True, envvar='DEBUG', help='Show debug messages and print tracebacks.')
@click.version_option(version=modrc.__version__)
@click.pass_context
def main(ctx, debug):
    """The CLI to make managing your files across systems easier."""
    # set global context
    ctx.obj = {
        'debug': debug
    }

# commands
main.add_command(setup)
