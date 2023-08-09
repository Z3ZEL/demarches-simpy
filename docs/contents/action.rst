Taking a look at Action
++++++++++++++++++++++++

.. hint:: 
    Let's create a simple program that retrieve a Dossier, change one of its annotation
    and submit it to the Demarche

.. seealso:: 
    The method is nearly the same for all actions, you can check them
    in the :doc:`Actions <../refs/demarches_simpy.actions>` section.

Retrieving a Dossier
--------------------

First you need to retrieve a Dossier object as we did in the previous example.

.. literalinclude:: ./getting_started_exemple/action.py
    :language: python
    :linenos:
    :lines: 1-7

.. note:: 

    You can notice here that we didn't use a Demarche object to retrieve a Dossier,
    if you know a Dossier's number you can manually create a Dossier object from a Profile
    and a Dossier number.

Get an instructeur id
---------------------

To submit a Dossier to the Demarche you need to provide an instructeur id, this id can be 
retrieved either with the Demarche or with the Dossier object.

.. literalinclude:: ./getting_started_exemple/action.py
    :language: python
    :linenos:
    :lines: 9-23

.. caution:: 

        You can access to instructeurs_id on a Dossier only if the dossier has been
        passed to INSTRUCTION state (because the instructeur_id is assigned at this state or later)

.. note::
    
        You can assign an instructeur id directly in the Profile constructor.

Creating the Action
-------------------

Now that we have a Dossier and an instructeur id we can create an Action, for this 
tutorial we will create an AnnotationModifier action. But all objects that derives from 
the IAction interface works the same way.

.. literalinclude:: ./getting_started_exemple/action.py
    :language: python
    :linenos:
    :lines: 25-38

Here we've created an AnnotationModifier action by passing the Dossier object we want to modify.
For now all action objects works independently from the Demarche object, and alterate a Dossier.
We can retrieve an annotation (which is a dict) and modify its *stringValue*.

.. note::

    You can passing the instructeur_id directly in the action constructor if you profile doesn't have one.


Submitting the Action
---------------------

Until now, the changement we made on the annotation is local, we need to perform the action to take effect.
We can perform the action by passing the modified annotation to the *perform* method.

.. literalinclude:: ./getting_started_exemple/action.py
    :language: python
    :linenos:
    :lines: 40-47

The result if the perform method is always an integer that represent the state of the action.
The IAction inteface defines three constants that can be used to check the result of the action.

* 0 : SUCCESS 
* 1 : NETWORK_ERROR
* 2 : REQUEST_ERROR

.. note::

    If the action has also a result, you can retrieve it with specific methods of the action.
    Take also note that an action can also implement more error codes.

Full example
------------

.. literalinclude:: ./getting_started_exemple/action.py
    :language: python
    :linenos:
