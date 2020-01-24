from telnyx.aio.api_resources.abstract.api_resource import APIResource


class SingletonAPIResource(APIResource):
    @classmethod
    def retrieve(cls, **params):
        return super(SingletonAPIResource, cls).retrieve(None, **params)

    @classmethod
    def class_url(cls):
        if cls == SingletonAPIResource:
            raise NotImplementedError(
                "SingletonAPIResource is an abstract class.  You should "
                "perform actions on its subclasses (e.g. Balance)"
            )
        # Namespaces are separated in object names with periods (.) and in URLs
        # with forward slashes (/), so replace the former with the latter.
        base = cls.OBJECT_NAME.replace(".", "/")
        return "/v2/%s" % (base,)

    def instance_url(self):
        return self.class_url()
