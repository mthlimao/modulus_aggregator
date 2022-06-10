import os
import click
import pandas as pd
from pathlib import Path
from tensorboard.backend.event_processing import event_accumulator
from modulus_aggregator.constants import RUN_PATH_NOT_FOUND, EXPORT_ERROR


@click.group()
def export():
    """Group of commands 'export'."""
    pass


@export.command()
@click.option('-ep', '--experiment_path', type=click.Path(exists=True), nargs=1, required=True,
              help="Path where the Modulus' experiment models are saved. "
                   "Each subpath of the experiment path will be related to a single run. " 
                   "The experiment path could be, for example, the 'outputs' or " 
                   "the 'multirun' directories generated by Modulus. "
                   "For now, this option is mandatory.")
def tags(experiment_path):
    """
    This command export the registered tags (for now, just tensors) in a .csv file.
    """
    try:
        df_tags = None
        experiment_path = Path(experiment_path).resolve(strict=True)
        
        for run in os.listdir(experiment_path):
            run_path = experiment_path / run
            click.echo(f'Exporting tags for {run_path.name}...')
            if run_path.is_dir():
                # Check events files (choose whichever has more tags/tensors)
                number_tags = 0
                ea_object = None
                for event_file in [file for file in os.listdir(run_path) if 'events.out.tfevents' in file]:
                    f = run_path / event_file
                    ea = event_accumulator.EventAccumulator(f.as_posix()).Reload()
                    if len(ea.Tags()['tensors']) > number_tags:
                        number_tags = len(ea.Tags()['tensors'])
                        ea_object = ea
                
                df_run = write_to_dataframe(run_path, ea_object)
                df_tags = pd.concat([df_tags, df_run], axis=0) if df_tags is not None else df_run        

        df_tags.to_csv(experiment_path / 'tags.csv', index=False)
        click.echo('Tags successfully exported.')
    
    except FileNotFoundError:
        click.echo(RUN_PATH_NOT_FOUND)
    
    except:
        click.echo(EXPORT_ERROR)


def write_to_dataframe(run_path, event_accumulator_object):
    # Iterate through tags (in current case, tensors)
    tags_dict = {
        'run' : [],
        'tag' : [],
        'step' : [],
        'value' : [],
        'wall_time' : [],
    }

    for t in event_accumulator_object.Tags()['tensors']:
        if len(event_accumulator_object.Tensors(t)[0].tensor_proto.float_val) > 0:
            for tensor_event in event_accumulator_object.Tensors(t):
                tags_dict['run'].append(run_path.name)
                tags_dict['tag'].append(t)
                tags_dict['step'].append(tensor_event.step)
                tags_dict['value'].append(tensor_event.tensor_proto.float_val[0])
                tags_dict['wall_time'].append(tensor_event.wall_time)
    
    df_tags = pd.DataFrame(tags_dict)

    return df_tags