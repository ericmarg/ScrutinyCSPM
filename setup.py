from setuptools import setup, find_packages

setup(
    name="scrutinycspm",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "hvac>=2.1.0",
        "hydra-core >= 1.3.2",
        "azure-identity>=1.6.0",
        "azure-keyvault-secrets>=4.8.0",
        "PyGithub>=2.2.0"
        # other dependencies...
    ],
    # ...
)