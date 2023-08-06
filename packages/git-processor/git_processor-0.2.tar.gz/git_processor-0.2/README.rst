Git Processor
=============

A git log processor for better stats.


Setup
-----

Install the library with:

.. code:: bash

    # From pypi
    python3 -m pip install git_processor
    # From local
    python3 -m pip install .

Run the ``generate_git_logs.sh`` in where you have all your repository then copy it into the jupyter folder.

Let's use jupyter to display the information.

.. code:: bash

    pyhton3 -m pip install jupyter
    cd jupyter/
    jupyter notebook


Testing
-------

To find out more info about the testing configuration, check out the
``tox.ini`` file.

.. code:: bash

   # Run the test suite
   tox
   # Run the linter:
   tox -e lint
