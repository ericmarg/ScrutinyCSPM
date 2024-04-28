# Setting Environment Variables for Scrutiny CSPM Azure Access

This README file provides step-by-step instructions for setting environment variables on Windows, Linux, and macOS, as well as an example of how to access those variables in your Python code using `os.environ`.

Remember to replace the placeholder values (`your_subscription_id`, `your_tenant_id`, `your_client_id`, `your_client_secret`) with your actual values when setting the environment variables.

## Windows

1. Open the Start menu and search for "Environment Variables".
2. Click on "Edit the system environment variables".
3. In the System Properties window, click on the "Environment Variables" button.
4. Under "User variables" or "System variables", click on "New".
5. Enter the variable name (e.g., `AZURE_SUBSCRIPTION_ID`) and its corresponding value.
6. Click "OK" to save the variable.
7. Repeat steps 4-6 for each environment variable you want to set.
8. Close any open command prompt windows and reopen them for the changes to take effect.

## Linux and macOS

1. Open a terminal window.
2. Open the shell configuration file for your current user:
   - For Bash shell: `nano ~/.bashrc`
   - For Zsh shell: `nano ~/.zshrc`
3. Add the following lines at the end of the file for each environment variable you want to set:

```bash
export AZURE_SUBSCRIPTION_ID="your_subscription_id"
export AZURE_TENANT="your_tenant_id"
export AZURE_CLIENT_ID="your_client_id"
export AZURE_SECRET="your_client_secret"

```

Replace `your_subscription_id`, `your_tenant_id`, `your_client_id`, and `your_client_secret` with their respective values.
4. Save the changes and exit the text editor.
5. Reload the shell configuration file:
- For Bash shell: `source ~/.bashrc`
- For Zsh shell: `source ~/.zshrc`

## Accessing Environment Variables in Python

In your Python code, you can access the environment variables using the `os.environ` dictionary. For example:

```python
import os

subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
tenant_id = os.environ['AZURE_TENANT']
client_id = os.environ['AZURE_CLIENT_ID']
client_secret = os.environ['AZURE_SECRET']
```