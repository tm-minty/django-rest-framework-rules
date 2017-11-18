from __future__ import absolute_import

from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework_rules.decorators import permission_required
from rest_framework_rules.mixins import PermissionRequiredMixin
from rules.contrib.views import objectgetter
from .models import Book
from .serializers import BookSerializer


class SimpleViewSetMixin:

    def retrieve(self, request, pk=None):
        return Response({'the man': 'you'})

    def list(self, request):
        return Response({'the man': 'you'})


class GenericViewSetMixin(SimpleViewSetMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ImproperlyConfiguredViewSet(PermissionRequiredMixin,
                                  SimpleViewSetMixin,
                                  ViewSet):
    pass


class DecoratedViewSet(ViewSet):

    @permission_required('testapp.access_single_permission_method')
    def list(self, request):
        return Response({'the man': 'you'})

    @permission_required('testapp.access_single_object_permission_method',
                         fn=lambda request, pk: Book.objects.get(author__username='anton'))
    def retrieve(self, request, pk=None):
        return Response({'the man': 'you'})

    @permission_required('testapp.access_multiple_permissions_method_1',
                         'testapp.access_multiple_permissions_method_2')
    def create(self, request):
        return Response({'the man': 'you'})

    @permission_required('testapp.access_multiple_permissions_method_1',
                         'testapp.access_multiple_permissions_method_2',
                         fn=lambda request, pk: Book.objects.get(author__username='anton'))
    def update(self, request, pk=None):
        return Response({'the man': 'you'})


class DecoratedViewSetWithCustomRoutes(PermissionRequiredMixin, ViewSet):

    @list_route(methods=['get'], permission_required='testapp.access_single_permission_detail_route')
    def single_permission_list_route(self, request):
        return Response({'the man': 'you'})

    @list_route(methods=['get'], permission_required=('testapp.access_multiple_permissions_detail_route_1',
                                                      'testapp.access_multiple_permissions_detail_route_2'))
    def multiple_permissions_list_route(self, request):
        return Response({'the man': 'you'})

    @detail_route(methods=['post'],
                  permission_required='testapp.access_single_permission_detail_route',
                  object_permission_required='testapp.access_single_permission_object')
    def single_permission_detail_route(self, request, pk=None):
        return Response({'the man': 'you'})

    @detail_route(methods=['post'],
                  permission_required='testapp.access_single_permission_detail_route',
                  object_permission_required=('testapp.access_multiple_permissions_object_1',
                                              'testapp.access_multiple_permissions_object_2'))
    def multiple_permissions_detail_route(self, request, pk=None):
        return Response({'the man': 'you'})


class SinglePermissionViewSet(PermissionRequiredMixin,
                              SimpleViewSetMixin,
                              ViewSet):
    permission_required = 'testapp.access_single_permission_viewset'


class MultiplePermissionsViewSet(PermissionRequiredMixin,
                                 SimpleViewSetMixin,
                                 ViewSet):
    permission_required = ('testapp.access_multiple_permissions_viewset_1',
                           'testapp.access_multiple_permissions_viewset_2')


class GenericViewSetWithoutObjectPermissions(PermissionRequiredMixin,
                                             GenericViewSetMixin,
                                             GenericViewSet):
    permission_required = 'testapp.permission_required'


class SinglePermissionGenericViewSet(PermissionRequiredMixin,
                                     GenericViewSetMixin,
                                     GenericViewSet):
    object_permission_required = 'testapp.access_single_permission_object'
    permission_required = 'testapp.access_single_permission_generic_viewset'


class MultiplePermissionsGenericViewSet(PermissionRequiredMixin,
                                        GenericViewSetMixin,
                                        GenericViewSet):
    object_permission_required = ('testapp.access_single_permission_permission_object_1',
                                  'testapp.access_single_permission_permission_object_2')
    permission_required = 'testapp.access_single_permission_generic_viewset'
