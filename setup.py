from setuptools import setup, find_packages

setup(
    name="scrutinycspm",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "hvac>=2.1.0",
        "antlr4-python3-runtime",
        "azure-keyvault-secrets==4.7.0",
        "hydra-core >= 1.3.2",
        "numpy<2,>=1.22.4",
        "pandas",
        "azure-identity>=1.6.0",
        "azure-keyvault-secrets",
        "PyGithub",
        "cryptography>=42.0.5",
        "azure-mgmt-resource>=23.0.1",
        "msticpy>=2.10.0",
        "azure-mgmt-network>=25.3.0",
        "azure-mgmt-monitor",
        "azure-mgmt-compute>=30.6.0",
        "OPA-python-client>=1.3.2",
        "boto3>=1.34.74",
        "azure-mgmt-authorization>=4.0.0",
        "azure-mgmt-subscription>=3.1.1",
        "ansible>=9.4.0",
        "ansible-runner>=2.3.6",
        "ansible-lint>=24.2.2",
        "ansible-creator",
        "ansible-dev-tools",
        "azure-storage-blob",
        
        # other dependencies...
    ],
    # ...
)