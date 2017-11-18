from __future__ import absolute_import

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_rules.decorators import permission_required
from rest_framework_rules.mixins import PermissionRequiredMixin
from testapp.models import Book
from testapp.serializers import BookSerializer

class SimpleResponseMixin:
    def get(self, request, *args, **kwargs):
        return Response({'woo': 'hoo'})


class GenericSimpleResponseMixin:

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return Response({'the man': 'you'})

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        return Response({'pk': book.pk})


class ImproperlyConfiguredAPIView(PermissionRequiredMixin,
                                  APIView):
    pass

class DecoratedView(APIView):

    @permission_required('testapp.access_single_permission_method')
    def get(self, request, *args, **kwargs):
        return Response({'the man': 'you'})

    @permission_required('testapp.access_single_object_permission_method',
                         fn=lambda x: Book.objects.get(author__username='anton'))
    def head(self, request, *args, **kwargs):
        return Response({'the man': 'you'})

    @permission_required('testapp.access_multiple_permissions_method_1',
                         'testapp.access_multiple_permissions_method_2')
    def patch(self, request, *args, **kwargs):
        return Response({'the man': 'you'})

    @permission_required('testapp.access_multiple_object_permissions_method_1',
                         'testapp.access_multiple_object_permissions_method_2',
                         fn=lambda x: Book.objects.get(author__username='anton'))
    def post(self, request, *args, **kwargs):
        return Response({'the man': 'you'})


class SinglePermissionView(PermissionRequiredMixin,
                           SimpleResponseMixin,
                           APIView):
    permission_required = 'testapp.access_single_permission_view'


class MultiplePermissionsView(PermissionRequiredMixin,
                              SimpleResponseMixin,
                              APIView):
    permission_required = ('testapp.access_multiple_permissions_view_1',
                           'testapp.access_multiple_permissions_view_2')


class GenericViewWithoutObjectPermissions(PermissionRequiredMixin,
                                          GenericSimpleResponseMixin,
                                          GenericAPIView):
    permission_required = 'testapp.permission_required'


class SinglePermissionGenericView(PermissionRequiredMixin,
                                  GenericSimpleResponseMixin,
                                  GenericAPIView):
    object_permission_required = 'testapp.access_single_permission_object'
    permission_required = 'testapp.access_single_permission_generic_view'


class MultiplePermissionsGenericView(PermissionRequiredMixin,
                                     GenericSimpleResponseMixin,
                                     GenericAPIView):
    object_permission_required = ('testapp.access_multiple_permissions_object_1',
                                  'testapp.access_multiple_permissions_object_2')
    permission_required = 'testapp.access_multiple_permissions_generic_view'
