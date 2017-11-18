from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from . import views
from . import viewsets

router = DefaultRouter()
router.register(r'single_permission_viewset',
                viewsets.SinglePermissionViewSet,
                base_name='single_permission_viewset')
router.register(r'multiple_permissions_viewset',
                viewsets.MultiplePermissionsViewSet,
                base_name='multiple_permissions_viewset')
router.register(r'improperly_configured_viewset',
                viewsets.ImproperlyConfiguredViewSet,
                base_name='improperly_configured_viewset')
router.register(r'single_permission_generic_viewset',
                viewsets.SinglePermissionGenericViewSet,
                base_name='single_permission_generic_viewset')
router.register(r'multiple_permissions_generic_viewset',
                viewsets.MultiplePermissionsGenericViewSet,
                base_name='multiple_permissions_generic_viewset')
router.register(r'decorated_viewset',
                viewsets.DecoratedViewSet,
                base_name='decorated_viewset')
router.register(r'decorated_custom_route',
                viewsets.DecoratedViewSetWithCustomRoutes,
                base_name='decorated_custom_route')

urlpatterns = [
    url(r'^decorated_view/$',
        views.DecoratedView.as_view(),
        name='decorated_view'),
    url(r'^single_permission_view/$',
        views.SinglePermissionView.as_view(),
        name='single_permission_view'),
    url(r'^multiple_permission_view/$',
        views.MultiplePermissionsView.as_view(),
        name='multiple_permissions_view'),
    url(r'^single_permission_generic_view/(?P<pk>[0-9]+)/$',
        views.SinglePermissionGenericView.as_view(),
        name='single_permission_generic_view'),
    url(r'^multiple_permissions_generic_view/(?P<pk>[0-9]+)/$',
        views.MultiplePermissionsGenericView.as_view(),
        name='multiple_permissions_generic_view'),
    url(r'^improperly_configured_api_view/$',
        views.ImproperlyConfiguredAPIView.as_view(),
        name='improperly_configured_api_view'),
] + router.urls
