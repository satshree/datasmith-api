# from django.views import View
from rest_framework import status, viewsets  # , permissions
# from django.contrib.auth.mixins import LoginRequiredMixin
from .responses import error_response, success_response


# class BaseAuthView(LoginRequiredMixin, View):
#     """Base User Authenticated View"""

#     class Meta:
#         abstract = True


class BaseViewSet(viewsets.GenericViewSet):
    """Base View Set."""
    # permission_classes = [permissions.IsAuthenticated]

    status = status

    class Meta:
        abstract = True

    def error_response(self, message=None, error=None, data=None, status=status.HTTP_500_INTERNAL_SERVER_ERROR):
        return error_response(message, data, error, status)

    def success_response(self, message=None, error=None, data=None, status=status.HTTP_200_OK):
        return success_response(data, message, error, status)


# class BaseViewSet(BaseAuthViewSet):
#     """Base Unauthenticated View Set."""
#     permission_classes = []

#     class Meta:
#         abstract = True
