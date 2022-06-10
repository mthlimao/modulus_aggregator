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
@click.option('-rp', '--run_path', type=click.Path(exists=True), nargs=1, required=True,
              help="Path related to single experiment run. "
                   "For now, this option is mandatory.")
def tags(run_path):
    """
    This command export the registered tags (for now, just tensors) in a .csv file.
    """
    try:
        run_path = Path(run_path).resolve(strict=True)
        # Check events files (choose whichever has more tags/tensors)
        number_tags = 0
        ea_object = None
        for filename in os.listdir(run_path):
            f = run_path / filename
            if os.path.isfile(f) and 'events.out.tfevents' in f.name:
                ea = event_accumulator.EventAccumulator(f.as_posix()).Reload()
                if len(ea.Tags()['tensors']) > number_tags:
                    number_tags = len(ea.Tags()['tensors'])
                    ea_object = ea
        
        write_to_csv(run_path, ea_object)
    
    except FileNotFoundError:
        click.echo(RUN_PATH_NOT_FOUND)
    
    except:
        click.echo(EXPORT_ERROR)


def write_to_csv(run_path, event_accumulator_object):
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
    df_tags.to_csv(run_path / 'tags.csv')
