Creating Pipelines
==================

As highlighted in the :doc:`Quickstart Guide <quickstart>` that pipelines
are the core of this library. In general, many of pipelines provided for
you are ready and configured for usage.

However, often the default pipeline will not work for everyone. In this 
case, pipelines can be created. There are two ways to create the pipeline.
The first way is to use this library in an imperative manner, and code 
as so. The second way, the preferred method, is to use the library's built 
in structure class.

.. note:: The structure class is still in development. Most of its 
   functionality is present, but, there may be some caveat. If you 
   encounter one, please contact the maintainers of this library.

Imperative Pipelines
--------------------

There is no supported infrastructure for imperative pipeline programming.
Though, this is by design. 

In order to allow for the greatest flexibility
when programming other pipelines, this library tried to use the `Numpy/Scipy
<https://www.scipy.org/>`_ and `Astropy <https://www.astropy.org/>`_ 
libraries as much as it could. 

To code a pipeline using this library and those libraries, please read the 
library documentation for each of the functions and methods. These 
routines use standard Python objects and standard Scipy objects for
greatest flexibility.

You can find the entire library documentation here: doc:`<python_docstrings/modules>`


