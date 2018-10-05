from rest_framework.serializers import HyperlinkedIdentityField


class HyperlinkedUserIDIdentityField(HyperlinkedIdentityField):
    """
    Overrides the get_url method to provide a custom url. In this
    case, the custom url displays the entire uri with only the user_id at the
    end
    """

    def get_url(self, obj, view_name, request, format):
        kwargs = {self.lookup_url_kwarg: obj.user_id.pk}
        return self.reverse(view_name, kwargs=kwargs,
                            request=request, format=format)


class HyperlinkedISBNIdentityField(HyperlinkedIdentityField):
    """
    Overrides the get_url method to provide a custom url. In this
    case, the custom url displays the entire uri with only the isbn at the end
    """

    def get_url(self, obj, view_name, request, format):
        kwargs = {self.lookup_url_kwarg: obj.isbn.pk}
        return self.reverse(view_name, kwargs=kwargs,
                            request=request, format=format)
