from iam.domain.mixins import Authorizable


class AuthorizableModel(Authorizable):

    @classmethod
    def get_resource_class(cls):
        m = cls._meta
        return f"{m.app_label}.{m.object_name}"
