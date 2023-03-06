Constructing a Client
---------------------

For simple use cases, creating a new instance of Client and adding routes
can be enough:

>>> client = inori.Client('http://my.api.com/v1')
>>> client.add_route('allThings')
>>> client.add_route('allPeople/${peopleId}')

>>> client.allPeople(peopleId=1).get()



When constructing a Client that will require extra logic, the Client can be
sub-classed:

.. code-block:: python

    class MyClient(inori.Client):
         route_paths = {
             'allThings',
             'allPeople/${peopleId}'
         }

         def __init__(self):
             super().__init__(self, 'http://my.api.com/v1')

         def get_one_thing(self, thing):
             result = self.allThings.get()
             return [i for i in result if i == thing]


The `route_paths` attribute can be set at the class level
to specify routes for the Client. The Route objects will be created on init.

>>> my_client = MyClient()
>>> my_client.allPeople(peopleId=1).get()


Customizing the Session
=======================

Each Route in a Client has its own requests.Session() instance
for making HTTP requests.

The `new_session()` method can be overloaded to change the behaviour
of the session objects created for each Route.

In this example, an Adapter is mounted to the session.

.. code-block:: python

    import requests

    from requests.adapters import HTTPAdapter


    class MyClient(inori.Client):
        route_paths = {
            'allThings',
            'allPeople/${peopleId}',
        }

        def new_session(self):
            session = requests.Session()

            adapter = HTTPAdapter(max_retries=3)
            session.mount("https://", adapter)

            return session
