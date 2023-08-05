import click
from viptela.vmanage_cli.import_cmd.templates import templates
from viptela.vmanage_cli.import_cmd.policy import policy

@click.group('import')
@click.pass_context
def import_cmd(ctx):
    """
    Import commands
    """

import_cmd.add_command(templates)
import_cmd.add_command(policy)