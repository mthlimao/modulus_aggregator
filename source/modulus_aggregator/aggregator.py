import click
from modulus_aggregator.constants import VERSION, REPO_LINK
from modulus_aggregator.export.export import export
from modulus_aggregator.show.show import show


@click.group()
def cli():
    """\b 
    Main command of modulus_aggregator package.
    This package aims to be a data aggregator for Modulus experiments. 
    
    \b
    It's CLI package which allows the user to export data saved in tags (currently, just tensors) 
    and save it in a python friendly format (.csv).

    \b
    This data aggregation procedure makes it possible for the specialist to conduct deeper analysis, 
    specially in a scenario with multiple trained models.
    """
    pass


@cli.command()
def about():
    """General Package Info and Contacts."""

    click.echo(f"Modulus Aggregator v{VERSION}.")
    click.echo(f"Github Repo: {REPO_LINK}.")


cli.add_command(export)
cli.add_command(show)
