

class Authorizable:
    """Represents an object that is authorizable."""

    @classmethod
    def get_resource_class(cls):
        """Returns the resource class of the objec."""
        raise NotImplementedError

    def get_resource_qualname(self):
        """Returns the qualified name of a resource,
        identifying it within the global scope of
        a system.
        """
        raise NotImplementedError

    def get_principal_authorizations(self, principal):
        """Return a set holding the authorizations that
        the principal has on this entity. The default
        implementation returns an empty set, meaning
        no permissions.
        """
        return set()
