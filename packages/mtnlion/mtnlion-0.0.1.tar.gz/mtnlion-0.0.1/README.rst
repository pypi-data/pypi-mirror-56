=================
Mountian Lion CSS
=================

Note on the badges: The badges reflect the current developmnet state of the project.
All releases must successfully pass the pipeline prior to release.

+----------------+-----------------------+
| Badge          | Service               |
+================+=======================+
| PyPI           | |version|             |
+----------------+-----------------------+
| Read the docs  | |devel-documentation| |
+----------------+-----------------------+
| Pipeline       | |devel-ci|            |
+----------------+-----------------------+
| Coverage       | |devel-cov|           |
+----------------+-----------------------+
                
Mountain Lion Continuum-Scale Lithium-Ion Cell Simulator uses FEniCS to solve partial differential equation models for lithium-ion cells.

* Free software: MIT license
* Documentation: https://mtnlion.readthedocs.io.

Features
--------

* Fast and customizable using model-based design
* Easily attach external controllers to the cell model
* Built-in Rothe's method time stepping using first-order implicit Euler's method

Included Models
---------------

* Doyle-Fuller-Newman isothermal cell model
* Thermal model
* Metallic lithium plaing model
* Solid-electrolyte interphase (SEI) model
* Double-layer capacitance model

Getting Started
---------------

mtnlion can be installed via PyPI using ``pip install mtnlion --user``. 
However, you'll have to ensure that the correct version of FEniCS is already installed on your machine. 
You can reference the `installation guide <https://mtnlion.readthedocs.io/en/devel/source/installation.html>`_. for help preparing your own development environment.
The `contributing guide <https://mtnlion.readthedocs.io/en/devel/source/contributing.html>`_ is also available for those who wish to add to this projec.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

.. |documentation| image:: https://readthedocs.org/projects/mtnlion/badge/?version=master
   :target: http://mtnlion.readthedocs.io/en/master/?badge=master
.. |version|  image:: https://img.shields.io/pypi/v/mtnlion.svg
   :target: https://pypi.python.org/pypi/mtnlion
.. |ci| image:: https://gitlab.com/macklenc/mtnlion/badges/master/pipeline.svg
   :target: https://gitlab.com/macklenc/mtnlion/commits/master
.. |cov| image:: https://gitlab.com/macklenc/mtnlion/badges/master/coverage.svg
   :target: https://gitlab.com/macklenc/mtnlion/commits/master

.. |devel-documentation| image:: https://readthedocs.org/projects/mtnlion/badge/?version=devel
   :target: http://mtnlion.readthedocs.io/en/devel/?badge=devel
.. |devel-version|  image:: https://img.shields.io/pypi/v/mtnlion.svg
   :target: https://pypi.python.org/pypi/mtnlion
.. |devel-ci| image:: https://gitlab.com/macklenc/mtnlion/badges/devel/pipeline.svg
   :target: https://gitlab.com/macklenc/mtnlion/commits/devel
.. |devel-cov| image:: https://gitlab.com/macklenc/mtnlion/badges/devel/coverage.svg
   :target: https://gitlab.com/macklenc/mtnlion/commits/devel