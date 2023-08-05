import click
from viptela.vmanage_cli.export.templates import templates
from viptela.vmanage_cli.export.policy import policy

@click.group()
@click.pass_context
def export(ctx):
    """
    Export commands
    """

export.add_command(templates)
export.add_command(policy)