# Ganymede | on-demand financial data | connecting to the gRPC API

This folder is dedicated to showcasing various environments that can connect to Ganymede gRPC API.

There are several ways to access Ganymede gRPC API, depending on your subscribed plan:
- From the Internet at large (public gRPC endpoints)
- From within a Virtual Private Cloud (private gRPC endpoints)

The API is secured and always requires users to authenticate with a token, as explained [here](https://dev.systemathics.eu/api-documentation.html#remoteaccess)

The Python and .NET packages come with embedded token and connection helpers, those are driven by a few [environment variables](https://dev.systemathics.eu/api-documentation.html#environment), the next section demonstrates how they are used.

## Interactive access : Jupyter Lab

Here are a few ways to leverage Jupyter Lab:

- Windows: Using [stock installers for Python and Jupyter Lab](https://dev.systemathics.eu/docs/sample-notebooks-remote-access-walkthrough-windows.html) (see: [jupyter-lab-windows.cmd](./jupyter-lab-windows.cmd))
- Windows: Using [Anaconda data science platform](https://dev.systemathics.eu/docs/sample-notebooks-remote-access-walkthrough-anaconda-windows.html) (see: [jupyter-lab-anaconda-windows.ps1](./jupyter-lab-anaconda-windows.ps1) and [env.ps1](./env.ps1))
- Unix: Running [Jupyter Lab inside a docker container](https://dev.systemathics.eu/docs/sample-notebooks-remote-access-walkthrough-unix.html) (see: [docker-jupyter-lab.sh](./docker-jupyter-lab.sh/) and [env.sh](./env.sh))

- Hosted: We provide a fully managed [online Jupyter Lab](https://dev.systemathics.eu/api-documentation.html#webhosted) with pre-installed capabilities to execute Python, C# and F#

## Direct access from any software stack

gRPC is [cross platform and cross language](https://grpc.io/docs/languages) allowing Ganymede to be called from almost any software.

## Code samples

There are plenty of code examples in [Python](/python/), [C#](/csharp/) and [F#](/fsharp/) that can be run from Jupyter.
