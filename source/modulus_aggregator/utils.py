import os
from pathlib import Path
from tensorboard.backend.event_processing import event_accumulator


def return_event_accumulator_object(run_path: Path):
    # Check events files (choose whichever has more tensors)
    # number_tensors = 0
    # ea_object = None
    ea_object = event_accumulator.EventAccumulator(run_path.as_posix()).Reload()
    # for event_file in [file for file in os.listdir(run_path) if 'events.out.tfevents' in file]:
    #     f = run_path / event_file
    #     ea = event_accumulator.EventAccumulator(f.as_posix()).Reload()
    #     if len(ea.Tags()['tensors']) > number_tensors:
    #         number_tensors = len(ea.Tags()['tensors'])
    #         ea_object = ea
    
    return ea_object
