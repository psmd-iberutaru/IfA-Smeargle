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
   functionality is present, but, there may be some caveats. If you 
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

You can find the entire library documentation here: :doc:`IfA-Smeargle Function Documentation <python_docstrings/IfA_Smeargle>`.

Structured Pipelines
--------------------

Structured pipelines are pipelines that are created using the data array 
class provided by this module. The class is the 
:class:`IfasDataArray <IfA_Smeargle.zulu.zulu_main.IfasDataArray>` 
class. It acts as a IfA-Smeargle wrapper around a standard ``.fits`` file.

In general, this class is representative of a data array. It is specific 
to this library. All of the important functions (in regards to pipeline 
creation) that the IfA-Smeargle library provides can be called via this
class. However, most of the functions of the 
:doc:`BRAVO module <python_docstrings/IfA_Smeargle.bravo>` cannot 
interact with the IfasDataArray class as the BRAVO module focuses on the
entire data directory. 

In order to load a ``.fits`` file into a IfasDataArray class, it can
be called directly. 

.. code-block:: python

   import IfA_Smeargle as ifas

   data_array = ifas.zulu.IfasDataArray(pathname='path/to/fits_file.fits', 
                                        configuration_class=None, blank=False)
   # A blank IfasDataArray class can also be created if need be.
   blank_data_array = ifas.zulu.IfasDataArray(pathname=None, 
                                              configuration_class=None, blank=True)

The IfasDataArray class implements interfaces with the important parts
of the imported file. These atributes may be directly interfaced with
as they are standard Python/Scipy/Astropy objects and may be overwritten
accordingly.

.. code-block:: python

   import IfA_Smeargle as ifas

   # This is the '.fits' file header.
   data_array.header
   # This is the '.fits' file data; it may be a ndarray or a masked array.
   data_array.data
   data_array.datamask # If it has a data mask, it is represented here.
   # This is the configuration class.
   data_array.config

The IfasDataArray, with its modifications, can also be written to file. 
The output is unsurprisingly a ``.fits`` file.

.. code-block:: python

   import IfA_Smeargle as ifas
   
   # The pathname is the file name that will be written.
   print(data_array.filepathname)
   # Saved to a .fits file.
   astropy_hdul_file = data_array.write_fits_file(overwrite=True, silent=False)

More information of the built in functions can be found by running :code:`data_array.help()`


