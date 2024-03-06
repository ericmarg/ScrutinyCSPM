from setuptools import setup, find_packages

setup(
    name="scrutinycspm",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "hvac>=2.1.0",
        "hydra-core >= 1.3.2"
        # other dependencies...
    ],
    # ...
)