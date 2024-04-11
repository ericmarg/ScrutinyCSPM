from setuptools import setup, find_packages

setup(
    name="scrutinycspm",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "hvac>=2.1.0",
        "hydra-core >= 1.3.2",
        "numpy<2,>=1.22.4",
        "pandas",
        "azure-identity>=1.6.0",
        "azure-keyvault-secrets>=4.8.0",
        "PyGithub>=2.2.0",
        "cryptography>=42.0.5",
        "azure-mgmt-resource>=23.0.1",
        "msticpy>=2.10.0",
        "azure-mgmt-network>=25.3.0",
        "azure-mgmt-monitor>=6.0.2",
        "azure-mgmt-compute>=30.6.0",
        "OPA-python-client>=1.3.2",
        "boto3>=1.34.74",
        "azure-mgmt-authorization>=4.0.0",
        "azure-mgmt-subscription>=3.1.1",
        "ansible>=9.4.0",
        "ansible-runner>=2.3.6"
        # other dependencies...
    ],
    # ...
)