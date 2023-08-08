A simple program
++++++++++++++++
.. hint:: 
    Let's create a simple program that retrieve Dossier's states for each Dossier in the Demarche

Creating the Profile object
---------------------------

To begin, you need to create a :doc:`Profile <../refs/demarches_simpy.connection>` object that contains api token and manage connection with
Demarches Simplifées, all objets in this package contains a reference to a Profile object.

.. literalinclude:: ./getting_started_exemple/a_simple_program.py
    :language: python
    :linenos:
    :lines: 1-5

.. note::
        
        You can set verbose to True to display all debug messages.
        Moreover you can trigger verbose all by running your python programm with the **-v** option.

Creating the Demarche object
----------------------------

Now you can create a :doc:`Demarche <../refs/demarches_simpy.demarche>` object that contains all information about a Demarche.

.. literalinclude:: ./getting_started_exemple/a_simple_program.py
    :language: python
    :linenos:
    :lines: 6-7


Replace the 00000 by the demarche number you want to retrieve.  To know this demarche number
you need to the Démarches Simplifiées website, and be sure that your API token scope contains
the demarche you want to retrieve. [1]_


.. note::
            
        You can also locate the verbose option to a specific object to get log only from this object and its children.

Getting Dossiers
----------------

Then you can use the function get_dossiers() to retrieve all :doc:`Dossier </refs/demarches_simpy.dossier>` from the Demarche object :

.. literalinclude:: ./getting_started_exemple/a_simple_program.py
    :language: python
    :linenos:
    :lines: 8-11

The get_dossiers() function return a list of Dossier object, each Dossier object contains all information about a Dossier.


The complete exemple : 

.. literalinclude:: ./getting_started_exemple/a_simple_program.py
    :language: python
    :linenos:

.. [1] Retrieving a demarche by its id is currently not supported)


