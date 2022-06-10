from setuptools import setup, find_namespace_packages

setup(
    name='modulus_aggregator',
    version='0.1',
    author_email='mthlima@cos.ufrj.br',
    install_requires=[
        'click',
        'pathlib',
        'pandas',
        'tensorboard',
    ],
    # tell setuptools that all packages will be under the 'source' directory
    packages=find_namespace_packages('source'),
    package_dir={'': 'source'},
    entry_points='''
        [console_scripts]
        modagg=modulus_aggregator.aggregator:cli
    ''',
)