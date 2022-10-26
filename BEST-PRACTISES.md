# Best practices

## Ganymede's online Jupyter Lab

* `Stop non used kernels`: when you are done with a Jupyter notebook, make sure you stop the kernel to take full advantage of available resources. To do so, navigate to **Running terminals and kernels** on the top left sidebar and **shut down** the chosen notebook.
* `Log-out`: once you finished working on your JupyterLab environment, save your changes (either by downloading or pushing to your personal git repository) then go to **File** on the top left of the main menu and click **Log out**. An auto-logout period otherwise be applied and you could loose your work. 

## Ganymede's gRPC API

* `Token regeneration`: access to Ganymede is granted through an *authentication token* with a limited lifetime. When running a notebook and an error "Unauthenticated" raises, please make sure your *Log out* and re-login. To check your token validity, refer to [this link](https://jwt.io/)  and copy/paste your token, which is generated in the *Step 2* of every Jupyter notebooks.

