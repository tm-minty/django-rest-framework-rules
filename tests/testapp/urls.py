from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from . import viewsets

router = DefaultRouter()
router.register(r'single_permission_viewset',
                viewsets.SinglePermissionViewSet,
                basename='single_permission_viewset')
router.register(r'multiple_permissions_viewset',
                viewsets.MultiplePermissionsViewSet,
                basename='multiple_permissions_viewset')
router.register(r'improperly_configured_viewset',
                viewsets.ImproperlyConfiguredViewSet,
                basename='improperly_configured_viewset')
router.register(r'single_permission_generic_viewset',
                viewsets.SinglePermissionGenericViewSet,
                basename='single_permission_generic_viewset')
router.register(r'multiple_permissions_generic_viewset',
                viewsets.MultiplePermissionsGenericViewSet,
                basename='multiple_permissions_generic_viewset')
router.register(r'decorated_viewset',
                viewsets.DecoratedViewSet,
                basename='decorated_viewset')
router.register(r'decorated_custom_route',
                viewsets.DecoratedViewSetWithCustomRoutes,
                basename='decorated_custom_route')
router.register(r'decorated_one_object_permission',
                viewsets.DecoratedViewSetOneObjectPermission,
                basename='decorated_one_object_permission')

urlpatterns = [
    path('decorated_view/',
        views.DecoratedView.as_view(),
        name='decorated_view'),
    path('single_permission_view/',
        views.SinglePermissionView.as_view(),
        name='single_permission_view'),
    path('multiple_permission_view/',
        views.MultiplePermissionsView.as_view(),
        name='multiple_permissions_view'),
    path('single_permission_generic_view/<int:pk>/',
        views.SinglePermissionGenericView.as_view(),
        name='single_permission_generic_view'),
    path('multiple_permissions_generic_view/<int:pk>/',
        views.MultiplePermissionsGenericView.as_view(),
        name='multiple_permissions_generic_view'),
    path('improperly_configured_api_view/',
        views.ImproperlyConfiguredAPIView.as_view(),
        name='improperly_configured_api_view'),
] + router.urls
