# modulus_aggregator
This project aims to be a data aggregator for Modulus experiments. It's CLI package which allows the user to export data saved in tags (currently, just tensors) and save it in a python friendly format (.csv).

This data aggregation procedure makes it possible for the specialist to conduct deeper analysis, specially in a scenario with multiple trained models.

## Feature overview
- Commands to export tensors in a .csv (either standard or wide-form dataframe format)
- Saves wall time per step
- Support for any subpath structures

## Run configuration
This package is meant to run in a environment with Modulus installed. So, once the repository is cloned to the environment, the user just has to run the command `pip install .` in the repo
directory.

Once the *modulus_aggregator* package is installed, the user can check the available commands in the CLI by using the command `modagg --help`.

## Directory Structure

An example of a typical directory structure for a Modulus Experiment is shown:

    modulus_experiment
    ├── conf                        # directory containing configuration files
    ├── outputs (or multirun)       # directory containing the trained Modulus models (usually called outputs or mulirun)
    │   ├── run_arch_1                  # directory containing modulus files of one specific run
    │   │   ├── .hydra                  # subdirectory containing hydra config files
    │   │   │   └──...
    │   │   ├── constraints             # subdirectory containing Modulus constraint files
    │   │   │   └──...
    │   │   ├── ...
    │   │   └── events.out.tfevents...  # file containing tags information
    │   │   
    │   ├── run_arch_2
    │   ├── ...
    │   └── run_arch_X
    └── modulus_experiment_code.py  # python file developed for the Modulus experiment

The *modulus_aggregator* package will search for the different runs (in this current example) saved in the outputs directory. To do that, the user has to specify this specific path in the commands available. For more information, the user can always use the option `--help` in the package command.

## Data Formats

The *modulus_aggregator* package exports the tensor data in a very similar format as exported in the Tensorflow dataframe api (https://www.tensorflow.org/tensorboard/dataframe_api).

In the standard format, the .csv file is exported with the following collumns:
- *run*: name of the run, represented by the run directory name (for example, run_arch_X);
- *tag*: the tag name, represented by the measured metric;
- *step*: the step number;
- *value*: the tag value;
- *wall_time*: the measured wall time for the current step

The user also has the possibility to save the data in a wide-form (pivoted) format by using the `--export_pivot` option, which saves each *tag* as a different column. For this to be possible, the same number of steps must had been recorded for each *tag* in the experiment. In case it's not possible to save it in the pivoted form, the package saves the data in the standard format.

By default, the data is saved in the directory containing the trained Modulus models.
