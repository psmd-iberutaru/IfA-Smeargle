Quickstart
==========

It is important that it is made clear that this is a module and a collection
of scripts more than a fully packaged program. To attempt to use it as such
may be a bit hard.

Nevertheless, this page guides one on how to use IfA-Smeargle for the 
reduction and analysis of their detector data.


Installation
------------

Installing IfA-Smeargle is not too difficult. It is a Python module like any 
other. Its source can be downloaded from the appropriate `GitHub IfA-Smeargle 
link <https://github.com/psmd-iberutaru/IfA-Smeargle>`_.

The entire directory is filled with other files not quite associated
with the module itself. (These files are still needed for historical and 
development purposes.) The directory/folder labeled ``IfA_Smeargle`` is the
module code itself. It can be imported like any other same directory module
(via ``import IfA_Smeargle as ifas``, as suggested).


Pipelines, Data Directories, and Configuration Files/Classes
------------------------------------------------------------

IfA-Smeargle reduction methods are not too difficult. However,
three elements must be clearly understood for proper usage. In general, they
are not too complicated.

Pipelines
`````````

Pipelines is simply an instructional list of what should be executed, in 
what order and to what quantity. Not every reduction functionality that 
IfA-Smeargle provided is needed for every data set. It is important that 
the proper pipeline is picked for the right data set.

Every and all built-in pipelines, by design, can be found in the ZULU line 
(module documentation can be found here: 
:doc:`ZULU documentation <python_docstrings/IfA_Smeargle.zulu>`.

Also, all built-in pipelines require 2 and only 2 positional parameters, 
usually structured as such::

   pipeline(data_directory, configuration_class)

This is intentional, and any development towards new proposed built-in 
pipelines should also adhere to this format.

Data Directories
````````````````

Data directories are most likely the easiest to understand. They are basically
strings to where the data is being stored. It is generally the design of 
every pipeline that it adapts their document renaming and processing to raw
data right out of the appropriate detector. Therefore, modification of raw
data or its file/file-structure is generally unneeded.

To feed a pipeline the proper data directory, just send it an absolute or 
relative (suggested) path to the data itself as a UNIX string path. Any 
built-in pipeline should be able to handle itself afterwards.

Configuration Files/Classes
```````````````````````````

Configuration files/classes are different and a bit more complex. It is a
general principle of IfA-Smeargle that any and all customization or 
parameters to any reduction functions are contained in a configuration 
file/class.

A configuration file just stores a configuration class; all configuration files
have the ``.ifaspkl`` file extension. IfA-Smeargle is hard-coded to reject 
any file without such extension and to always write configuration classes 
with such extension. Do not rename any file not made by IfA-Smeargle with 
such file extension.

In order to make a configuration file, please use the Jupyter notebook labeled
``ifas_configuration_recipe.ipynb``. This writes a configuration file as 
specified. 

.. warning::
   Configuration files and classes are not forward compatible. There 
   is however a function to convert older configuration classes/files to newer
   versions while preserving the old configuration data. See the :func:`Fast Forward Configuration Class <IfA_Smeargle.yankee.yankee_functions.yankee_fast_forward_configuration_class>` function for more information.


Executing Pipelines
-------------------

We are all well and good now; having learned the three basic elements of this
module. The only thing left is to combine them into one call so that the 
pipeline will run on the data within the data directory in accordance to 
parameters set by the configuration file. There are currently three ways
(really two ways) that this can be done. Listed below are the three primary
and suggested ways that pipelines should be executed.

Jupyter Notebook
````````````````

Jupyter notebook is very helpful in sectioning off code and running it 
individually. It is currently the suggested of the three equally valid ways
to execute a pipeline. 

Like any other Python module, IfA-Smeargle can be imported as a local module 
into the Jupyter notebook Python script using ``import IfA_Smeargle as ifas``.
(As per Python imports, the ``ifas`` isn't needed, but it is the suggested 
abbreviation for this module.) Please note that this is a local import rather
than a package import. Feel free to add this module into your Python package
directory at your own risk. 

You can then load your configuration files as one would load normal files in 
Jupyter notebook via the YANKEE line; then run built-in pipelines found in the
ZULU line like normal function call.

To load a configuration file and have it be a configuration class, the simplest
way is likely to invoke the following function call::

   config_class = ifas.yankee.SmeargleConfig('path/to/ifas_config.ifaspkl')

To execute a pipeline, as they are generally stored in ZULU, calling them 
from there is the suggested way to do it::

   __ = ifas.zulu.pipelines.pipeline_name(data_directory, configuration_class)

Python Interactive Session
``````````````````````````

This is not too different from Jupyter notebook method. In a similar vein to
the Jupyter notebook scheme, IfA-Smeargle can be imported into an interactive 
session or a full-fledged Python script using ``import IfA_Smeargle as ifas``
(while obeying local import rules, unless in package path directory).

From that point on, as it is within a Python session (like Jupyter notebook), 
to call pipelines and load configuration files and execute them as needed.

See `Jupyter Notebook`_ for more information on how to use IfA-Smeargle within
Python environment. 

Command-line Call
`````````````````

It is common for Python scripts to be run from from the command-line interface. 
As such, this module allows pipelines to be run from a command-line interface 
via ``ifas_execute.py``.

The command-call for ``ifas_execute.py`` must be done within the same directory
as the Python file, or one parent directory above it. It will likely be unable
to import local directories if it is executed outside of these areas. The 
data directory and configuration file directory paths should not have theses
restrictions. 

All command-line calls will likely be in a format similar to the one below::

   python ifas_execute.py 'pipeline_name' 'data_directory' 'configuration_file'

Note that all parameters should be strings which contain the paths (or in the 
case of ``pipeline_name``, the exact name of the pipeline itself.) There is 
an optional silent flag (``-s`` or ``--silent``); it defaults to False.