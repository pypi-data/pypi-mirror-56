import random
from .endpoints import Endpoints

class Instance:
    """Wrapper for the creation and deletion of a component.

    An instance object provides __enter__ and __exit__ methods.
    They use the component's andpoints specification to
    create a resource and delete it.

    During enter, a component is created using the endpoint
    comp.endpoints.create.
    As payload data, it uses a random element from the
    generated list of valids for comp.endpoints.CREATE.

    During exit, the component is deleted using the endpoint
    comp.endpooints.delete.
    As payload data, it uses a random element from the
    generated list of valids for comp.endpoints.DELETE.

    The payload submitted when calling the create entpoint
    is stored in self.spec.
    The result of the create endpoint is stored in
    self.data for accessing it later.

    Parameters
    ----------
    comp: Component object
        Component to create an instance from
    parent: Instance object, default None
        Instance of a parent (as specified by the component's parent)
    **values: arbitrary
        Arbitrary values to overwrite values (from valids) for resource creation

    Examples
    --------
    comp = ...
    with Instance(comp) as instance:
        print(instance.data)
        print(instance.spec)
    """
    def __init__(self, comp, parent=None, **values):
        self.comp = comp
        self.parent = parent
        self.values = values

    def __enter__(self):
        if self.comp.parent is not None and self.parent is None:
            self.parent = Instance(self.comp.parent)
            self.parent.__enter__()
            self.parent_created = True
        else:
            self.parent_created = False

        valids = random.choice(self.comp.get_valids(Endpoints.CREATE))
        values_ = {**valids, **self.values}
        self.data = self.comp.endpoints.create(values_, self.parent)
        self.spec = values_
        return self

    def __exit__(self, type, value, traceback):
        valids = random.choice(self.comp.get_valids(Endpoints.DELETE))
        self.comp.endpoints.delete(valids, self)
        if self.parent_created:
            self.parent.__exit__(None, None, None)


import pytest
from .util import rand_int, rand_str, rand_uuid
from .property import Property
from .properties import Properties
from .endpoints import Endpoints
from .component import Component

def test_constr():
    p1 = Property("p1", rand_str, rand_int)
    p2 = Property("p2", rand_int, rand_str)
    def create(values, parent):
        return values
    def delete(values, instance):
        return instance.data
    endpoints = Endpoints(create=create, delete=delete)
    comp = Component("c1", Properties(p1, p2), endpoints)
    with Instance(comp) as instance:
        pass
