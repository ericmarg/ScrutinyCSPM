from setuptools import setup, find_packages
from cli.commands import command1

setup(
    name="scrutinycspm",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "hvac>=2.1.0",
        "hydra-core >= 1.3.2",
        "azure-identity>=1.6.0",
        "azure-keyvault-secrets>=4.8.0",
        "PyGithub>=2.2.0",
        "cryptography>=42.0.5",
        "stevedore>=5.2.0",
        "azure-mgmt-resource>=23.0.1",
        "msticpy>=2.10.0",
        "azure.mgmt.network>=25.3.0",
        "azure.mgmt.resource>=23.0.1",
        "azure.mgmt.monitor>=6.0.2",
        "azure.mgmt.compute>=30.6.0",
        "pandas>=2.2.1"
        # other dependencies...
    ],
    entry_points={
        'cli.commands': [
            'command1 = cli.commands.command1:Command1',
        ],
        'cli.commands.command1.subcommand1': [
            'subcommand1 = cli.commands.command1_subcommand1:Command1Subcommand1',
        ],
        'cli.commands.command1.subcommand2': [
            'subcommand2 = cli.commands.command1_subcommand2:Command1Subcommand2',
        ],
        # Add similar entry points for command2 sub-commands
    },
    # ...
)