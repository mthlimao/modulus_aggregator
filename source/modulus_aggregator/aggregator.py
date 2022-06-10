import click
from modulus_aggregator.constants import VERSION
from modulus_aggregator.tags_exporter import export


@click.group()
def cli():
    """\b    
    Developed by me.
    """
    pass


@cli.command()
def about():
    """General Package Info and Contacts."""

    click.echo(f"Modulus Exporter v{VERSION}.\n")
    pass


cli.add_command(export)
