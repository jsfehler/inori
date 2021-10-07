Headers
=======

Client Headers
--------------

Headers can be added onto a Client instance. These values will be used on
every request.

.. code-block:: python

    client = Client('https://foo.com/v1/')
    client.headers['Accept'] = 'application/json'


Route Headers
-------------

Headers can be added onto a Route instance. These values will only be used
on that Route.

.. code-block:: python

    client = Client('https://foo.com/v1/')

    route = client.add_route("bar")
    route.headers['Accept'] = 'application/json'


Using Functions as Headers
++++++++++++++++++++++++++

On both Client and Route, functions can be added using the `headers`
attribute as a decorator. These functions will be run every time a
request is made.

The object that owns the header is provided as the first argument to the
function.

.. code-block:: python

    client = Client('https://foo.com/v1/')

    @client.headers("Powerful Word")
    def powerful_word(client):
        return "Word"

    route = client.add_route("bar")

    @route.headers("Powerful Number")
    def powerful_number(route):
        return "123"
