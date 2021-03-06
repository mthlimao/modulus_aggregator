import os
import click
from pathlib import Path
from modulus_aggregator.constants import RUN_PATH_NOT_FOUND
from modulus_aggregator.utils import return_event_accumulator_object


@click.command()
@click.option('-ep', '--experiment_path', type=click.Path(exists=True), nargs=1, required=True,
              help="Path where the Modulus' experiment models are saved. "
                   "Each subpath of the experiment path will be related to a single run. " 
                   "The experiment path could be, for example, the 'outputs' or " 
                   "the 'multirun' directories generated by Modulus. "
                   "For now, this option is mandatory.")
def show(experiment_path):
    """
    This command basically shows to the user all registered tags in the experiment.
    This command assumes that every model trained in the --experiment_path has the
    same registered Tags.
    """
    try:
        experiment_path = Path(experiment_path).resolve(strict=True)

        for run in os.listdir(experiment_path):
            run_path = experiment_path / run            
            if run_path.is_dir():
                ea_object = return_event_accumulator_object(run_path)
                
                for tag_name, tag_values in ea_object.Tags().items():
                    if tag_values not in [[], False]:
                        click.echo(f"Showing {tag_name}:")
                        click.echo(f"{', '.join(tag_values)}")
                
                break

    except FileNotFoundError:
        click.echo(RUN_PATH_NOT_FOUND)
