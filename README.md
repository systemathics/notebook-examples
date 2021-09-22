# Ganymede | on-demand financial data

This repository contains Jupyter notebooks to request analytics and retrieve bespoke datasets by calling Systemathics API. Samples and building blocks are available to help you designing your bespoke analytics and data requests:

- Reference data
- Corporate actions
- Historical financial data and calculations: daily and tick data
- Best executions samples
- Future roll strategies and trading strategies
- Monitoring dashboard including data storage and normalization metrics

## Best practices

Please find below some useful hints for Ganymede, the JupyterLab environment.
* `Stop non used kernels`: when you are done with a Jupyter notebook, make sure you stop the kernel to take full advantage of available resources. To do so, navigate to **Running terminals and kernels** on the top left sidebar and **shut down** the chosen notebook.
* `Log-out`: once you finished working on your JupyterLab environment, please go to **File** on the top left of the main menu and click **Log out**.
* `Token regeneration`: access to Ganymede is granted through an *authentication token* with a limited lifetime. When running a notebook and an error "Unauthenticated" raises, please make sure your *Log out* and re-login. To check your token validity, refer to [this link](https://jwt.io/)  and copy/paste your token, which is generated in the *Step 2* of every Jupyter notebooks.

## Systemathics API version

[![PyPI version](https://badge.fury.io/py/systemathics.apis.svg)](https://badge.fury.io/py/systemathics.apis) [![NuGet version](https://badge.fury.io/nu/systemathics.apis.svg)](https://badge.fury.io/nu/systemathics.apis)

## Useful links

- [Systemathics website](https://www.systemathics.com/) 
- [Systemathics data offer website](https://ganymede.cloud/)
- [Ganymede](https://ganymede.cloud/data/): credentials required to access JupyterLab environment
- [Documentation](https://ganymede.cloud/api-documentation.html): includes API documentation and tutorials (authentication, services, request parameters, reply formats...)

