#!/usr/bin/python3

# to add support for .NET kernels
# dotnet tool install -g Microsoft.dotnet-interactive
# dotnet interactive jupyter install

# to see available kernels list
# jupyter kernelspec list

import glob
import os
import logging
import multiprocessing
import nbformat
import re
import shutil
import sys

from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.exporters import HTMLExporter

# Ensure this is set
if not os.environ.__contains__("AUTH0_TOKEN"):
    raise Exception("Environment variable AUTH0_TOKEN should be set. CLIENT_ID/CLIENT_SECRET would triger too many auth0 API calls")

# Process command line
arguments = sys.argv
if arguments.__contains__("--html"):
    html = True
    generatedStatic = "_generated_html"
    templateExporter = HTMLExporter()
    arguments.remove("--html")
else:
    html = False
    generatedStatic = "_generated_static"
    templateExporter = None

"""
Execute a Jupyter notebook. This function ensures that figures are correctly created as SVG
so that conversion of the output notebook to md/html is expurged of any oddity (like 5MB of inlined JS for example)
We inject code for that matter, currently supported matplotlib and plotly
Arguments:
    notebook_path: The input notebook path
    notebook_output_path: The output notebook path
"""
def execute_notebook(notebook_path:str, notebook_output_path: str):
    py_matplotlib = "from matplotlib_inline import backend_inline as mplbi{}\nmplbi{}.set_matplotlib_formats('svg')\n\n"
    py_plotly = "import plotly.io as pio{}\npio{}.renderers.default = 'svg'\n\n"

    notebook_output_dir = os.path.dirname(notebook_output_path)
    os.makedirs(notebook_output_dir, exist_ok=True)
    notebook_path_temp = notebook_output_path + '.tmp'
    i=0
    try:
        with open(notebook_path) as f:
            nb = nbformat.read(f, as_version=4)
            # reprocess code cells 
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    if not html:
                        if cell.source.__contains__('import matplotlib'): # Python: Force SVG figures
                            i += 1
                            cell.source = py_matplotlib.format(i, i) + cell.source
                        if cell.source.__contains__('import plotly'): # Python: Force SVG figures
                            i += 1
                            cell.source = py_plotly.format(i, i) + cell.source
                    if cell.source.__contains__('/home/jovyan'):
                        cell.source = cell.source.replace('/home/jovyan', os.environ["HOME"]) # Fix nuget packages home

            # write reprocessed to temp notebook
            with open(notebook_path_temp, mode='w', encoding='utf-8') as f:
                nbformat.write(nb, f)

        # execute temp notebook
        with open(notebook_path_temp) as f:
            nb = nbformat.read(f, as_version=4)
            ep = ExecutePreprocessor(timeout=600)
            pwd = os.getcwd()
            try:
                logging.debug("Changing to directory {}".format(notebook_output_dir))
                os.chdir(notebook_output_dir)
                ep.preprocess(nb)
            finally:
                logging.debug("Changing to directory {}".format(pwd))
                os.chdir(pwd)

            # write to final output, after that, converting to converted or html will produce nice references to SVG images
            with open(notebook_output_path, mode='w', encoding='utf-8') as f:
                nbformat.write(nb, f)

        # Convert
    finally:
        try:
            os.remove(notebook_path_temp)
        except OSError:
            pass

"""
Get the expected converted file path for a given notebook
Arguments:
    notebook_path: The input notebook path
    exporter: The exporter
"""
def converted_notebook_path(notebook_path: str, exporter: HTMLExporter):
    current_dir = os.getcwd()
    notebook_output_path = os.path.realpath(notebook_path)
    notebook_output_path = notebook_output_path.replace(current_dir, "{}/{}".format(current_dir, generatedStatic))
    notebook_output_path = notebook_output_path.lower()
    notebook_output_path = notebook_output_path.replace('[','')
    notebook_output_path = notebook_output_path.replace(']','')
    notebook_output_path = notebook_output_path.replace(' ','-')
    if exporter is not None:
        notebook_output_path = os.path.splitext(notebook_output_path)[0] + exporter.file_extension
    return notebook_output_path

"""
Get the expected converted 'input file' path for a given file (example: my_notebook_input.csv)
Arguments:
    inputfile_path: The input notebook path
    exporter: The exporter
"""
def converted_inputfile_path(notebook_path: str):
    current_dir = os.getcwd()
    inputfile_path = os.path.realpath(notebook_path)
    inputfile_path = inputfile_path.replace(current_dir, "{}/{}".format(current_dir, generatedStatic))
    inputfile_path = inputfile_path.lower()
    inputfile_path = inputfile_path.replace('[','')
    inputfile_path = inputfile_path.replace(']','')
    inputfile_path = inputfile_path.replace(' ','-')
    return inputfile_path

"""
Get the expected output file path for a given notebook
Arguments:
    notebook_path: The input notebook path
"""
def executed_notebook_path(notebook_path: str):
    current_dir = os.getcwd()
    notebook_output_path = os.path.realpath(notebook_path)
    notebook_output_path = notebook_output_path.replace(current_dir, "{}/{}".format(current_dir, generatedStatic))
    notebook_output_path = notebook_output_path.lower()
    notebook_output_path = notebook_output_path.replace('[','')
    notebook_output_path = notebook_output_path.replace(']','')
    notebook_output_path = notebook_output_path.replace(' ','-')
    return notebook_output_path


"""
Convert Jupyter notebook using the given exporter (ex: HTMLExporter).
We also extract resources like images and store them to sub directories.
Arguments:
    notebook_path: The input notebook path
    exporter: The exporter
Returns:
    The converted file path
"""
def convert_notebook(notebook_path: str, exporter: HTMLExporter):
    output_path = os.path.splitext(notebook_path)[0] + exporter.file_extension
    name = os.path.splitext(os.path.basename(notebook_path))[0]
    resource_path_relative_folder= "{}_files".format(name)
    subdir = os.path.dirname(output_path) + "/" + resource_path_relative_folder
    try:
        shutil.rmtree(subdir)
    except:
        pass
    
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
        converted, resources_ditionary = exporter.from_notebook_node(nb)
        
        # save resources
        if resources_ditionary is not None:
            resources_ditionary_outputs = resources_ditionary["outputs"]
            if resources_ditionary_outputs is not None:
                for key in resources_ditionary_outputs:
                    resource_path = "{}/{}".format(subdir, key)
                    resource_output_dir = os.path.dirname(resource_path)
                    os.makedirs(resource_output_dir, exist_ok=True)
                    logging.info("Writing converted notebook resource {} to {}".format(key, resource_path))
                    with open(resource_path, 'wb') as fw:
                        fw.write(resources_ditionary_outputs[key])       
                    resource_path_relative = "{}/{}".format(resource_path_relative_folder, key)             
                    converted = converted.replace(key, resource_path_relative)
        
        # save main
        logging.info("Writing converted notebook to {}".format(output_path))
        with open(output_path, 'w', encoding='utf-8') as fw2:
            fw2.write(converted)

    return output_path

"""
Convert Jupyter notebook using the given exporter (ex: HTMLExporter).
We also extract resources like images and store them to sub directories.
Arguments:
    notebook_path: The input notebook path
    exporter: The exporter
Returns:
    The converted file path
"""
def statify(notebook_path: str, templateExporter: HTMLExporter):
    notebook_output_path = executed_notebook_path(notebook_path)    
    try:
        # If an 'input' directory is there next to the notebook, copy its content
        inputs_dir = "{}/input/*".format(os.path.dirname(notebook_path))
        inputs = glob.glob(inputs_dir, recursive=True)
        for input in inputs:
            copy = converted_inputfile_path(input)
            print("Copying\n  {} to\n  {}".format(input, copy))
            copy_dir = os.path.dirname(copy)
            os.makedirs(copy_dir, exist_ok=True)
            shutil.copyfile(input, copy)

        # Execute the notebook
        logging.info("Executing notebook {} and saving results to {}".format(notebook_path, notebook_output_path))
        execute_notebook(notebook_path, notebook_output_path)
        logging.info("Executed notebook {} and saved results to {}".format(notebook_path, notebook_output_path))

        # Rework
        logging.info("Reworking {}".format(notebook_output_path))
        content_new = None
        with open(notebook_output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            q = content
            q = re.sub(r'Bearer ([a-zA-Z0-9\._-]*)', 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZXNzYWdlIjoibm90IGEgcmVhbCB0b2tlbiJ9.N3ar08-nYnP33H210Pp74lraRRW1A052iXrVnssAf22nQes-SmD9ngjxoBiGOw4H6UV2ch29h6Qi4Nd4YaTs5A', q, flags=re.MULTILINE) # valid JWT giving access to nothing
            q = re.sub(os.environ['HOME'], '~', q, flags=re.MULTILINE) # replace home dir string by ~
            if len(q) != len(content):
                content_new = q
        if content_new is not None:
            with open(notebook_output_path, 'w', encoding='utf-8') as w:
                w.write(content_new)

        if templateExporter is not None:
            # Convert the notebook
            logging.info("Converting notebook {}".format(notebook_output_path))
            converted_path = convert_notebook(notebook_output_path, templateExporter)
            logging.info("Converted notebook {} and saved to {}".format(notebook_output_path, converted_path))

            # Rework
            logging.info("Reworking {}".format(converted_path))
            content_new = None
            with open(converted_path, 'r', encoding='utf-8') as f:
                content = f.read()
                q = content
                css_script = re.compile('<\s*style type="text/css">.*?<\s*/\s*style\s*>', re.S | re.I) # factorize Jupyter css, it's big (800+KB)
                q = css_script.sub('<link rel="stylesheet" type="text/css" href="http://systemathics.io/stylesheets/jupyter.css" />', q)
                if len(q) != len(content):
                    content_new = q
            if content_new is not None:
                with open(converted_path, 'w', encoding='utf-8') as w:
                    w.write(content_new)
    finally:
        try:
            if templateExporter is not None:
                logging.info("Deleting {}".format(notebook_output_path))
                os.remove(notebook_output_path)
        except OSError:
            pass

# Main

logging.basicConfig(stream = sys.stdout, 
                    filemode = "w",
                    format = "%(levelname)s %(asctime)s - %(message)s", 
                    level = logging.INFO)

argc = len(arguments)
if argc == 2:
    # statify just the given notebook
    statify(arguments[1], templateExporter)
elif argc == 1:
    # Create the notebooks files list to process
    def getfiles(prefix: str):
        logging.info("Will now find for {}".format(prefix))
        files = []
        files_to_process = []
        files = files + glob.glob("{}/**/*.ipynb".format(prefix), recursive=True)
        for file in files:
            expected = converted_notebook_path(file, templateExporter)
            if not os.path.exists(expected):
                files_to_process.append(file)
                logging.info("Will statify {} as {} doesn't already exists".format(file, expected))
            else:
                logging.debug("Will not statify {} as {} already exists".format(file, expected))

        logging.info("Will process {} not yet converted .ipynb files (out of {} available)".format(len(files_to_process), len(files)))
        logging.info("")
        return files_to_process

    # Execute in parallel
    for prefix in ["python","csharp","fsharp"]:
        # Execution function
        def statify1(file: str):
            try:
                statify(file, templateExporter)
            except Exception as ex:
                logging.error("Could not statify {}:\n{}".format(file, ex))
                pass

        files_to_process = getfiles(prefix)
        if prefix == "python":
            n = 8
        else:
            n = 1 # dotnet interactive messes up with listen ports !
        try:
            pool = multiprocessing.Pool(n)
            pool.map(statify1, files_to_process)
        finally:
            pool.close()
