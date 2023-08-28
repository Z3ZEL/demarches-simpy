Dossier Filtering
+++++++++++++++++
.. hint::
    Dossier Filtering is a feature that allows you to filter the list of dossiers displayed in the Dossier List View.
    You can use it to filter the list of dossiers by the dossier's attributes, by the dossier's state or with more complex filters.

Basic filtering : Retrieving a specific dossier
-----------------------------------------------

The function :doc:`get_dossiers <../refs/demarches_simpy.demarche>` allows you to retrieve all dossiers of a demarche.
You can pass a filter argument to this function to filter the list of dossiers. Let's retrieve a dossier by its number :


.. literalinclude:: ./getting_started_exemple/filtered_dossier.py
    :language: python
    :linenos:
    :lines: 1-13

.. note:: 
    The '-1' argument passed to the function indicate that we don't want a limit on the number of dossiers returned.
    If you want to retrieve only one dossier, you can pass 1 as the limit argument.


Background fetching
-------------------

The id or the number of a dossier is part of the Dossier object. We don't need to fetch the dossier to retrieve its id or number.
That's why it will be fast. But if we want to apply a filter on a property (which will be fetched) we need
to enable bakcground_fetching option, which will fetch the dossier in background. It will increase the speed
of the research. If you don't enable this option it will work but it will take longer.

.. literalinclude:: ./getting_started_exemple/filtered_dossier.py
    :language: python
    :linenos:
    :lines: 15-25


Advanced usage
--------------

We saw that background_fetching will fetch property in background. But if the property is conditionnal it won't be fetched.
For instance 'fields' of a dossier is conditionnal. If you want to filter on a conditionnal property you need to enable them at default by using
default_variables dict.

.. literalinclude:: ./getting_started_exemple/filtered_dossier.py
    :language: python
    :linenos:
    :lines: 26-35

Full example
------------

.. literalinclude:: ./getting_started_exemple/action.py
    :language: python
    :linenos:
