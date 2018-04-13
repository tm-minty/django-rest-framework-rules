from __future__ import absolute_import

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import reverse
from rest_framework.test import APITestCase
from testapp import viewsets


class PermissionRequiredMixedViewSetTests(APITestCase):

    """Tests the behavior of the mixin when used on an ViewSet
    """
    def test_user_with_permission_gets_access(self):
        user = User.objects.get(username='anton')
        permissions = viewsets.SinglePermissionViewSet().get_permission_required()
        self.assertTrue(all([user.has_perm(perm) for perm in permissions]))

        self.assertTrue(self.client.login(username='anton', password='secr3t'))
        response = self.client.get(reverse('single_permission_viewset-detail', args=(1,)))
        self.assertEqual(200, response.status_code)

    def test_user_without_permission_gets_no_access(self):
        user = User.objects.get(username='beatrix')
        permissions = viewsets.SinglePermissionViewSet().get_permission_required()
        self.assertTrue(any([not user.has_perm(perm) for perm in permissions]))

        self.assertTrue(self.client.login(username='beatrix', password='secr3t'))
        response = self.client.get(reverse('single_permission_viewset-detail', args=(1,)))
        self.assertEqual(403, response.status_code)

    def test_user_with_permissions_gets_access(self):
        user = User.objects.get(username='anton')
        permissions = viewsets.MultiplePermissionsViewSet().get_permission_required()
        self.assertTrue(all([user.has_perm(perm) for perm in permissions]))

        self.assertTrue(self.client.login(username='anton', password='secr3t'))
        response = self.client.get(reverse('multiple_permissions_viewset-detail', args=(1,)))
        self.assertEqual(200, response.status_code)

    def test_user_with_partial_permissions_gets_no_access(self):
        user = User.objects.get(username='beatrix')
        permissions = viewsets.MultiplePermissionsViewSet().get_permission_required()
        self.assertTrue(any([not user.has_perm(perm) for perm in permissions]))

        self.assertTrue(self.client.login(username='beatrix', password='secr3t'))
        response = self.client.get(reverse('multiple_permissions_viewset-detail', args=(1,)))
        self.assertEqual(403, response.status_code)

    def test_user_without_permissions_gets_no_access(self):
        user = User.objects.get(username='carlos')
        permissions = viewsets.MultiplePermissionsViewSet().get_permission_required()
        self.assertTrue(all([not user.has_perm(perm) for perm in permissions]))

        self.assertTrue(self.client.login(username='carlos', password='secr3t'))
        response = self.client.get(reverse('multiple_permissions_viewset-detail', args=(1,)))
        self.assertEqual(403, response.status_code)

    def test_improperly_configured_viewset_raises(self):
        with self.assertRaises(ImproperlyConfigured):
            response = self.client.get(reverse('improperly_configured_viewset-detail', args=(1,)))


class PermissionRequiredMixedGenericViewSetTests(APITestCase):

    """Tests the behavior of the mixin when used on a GeneriViewSet
    """

    def test_object_permission_falls_back_to_required_permissions(self):
        viewset = viewsets.GenericViewSetWithoutObjectPermissions()
        self.assertEquals(None, viewset.object_permission_required)
        self.assertEquals(viewset.get_permission_required(),
                          viewset.get_object_permission_required())

    def test_user_with_object_permission_gets_access_to_object(self):
        user = User.objects.get(username='anton')
        permissions = viewsets.SinglePermissionGenericViewSet().get_object_permission_required()
        self.assertTrue(all([user.has_perm(perm) for perm in permissions]))

        self.assertTrue(self.client.login(username='anton', password='secr3t'))
        response = self.client.get(reverse('single_permission_generic_viewset-detail', args=(1,)))
        self.assertEqual(200, response.status_code)

    def test_user_with_object_permissions_gets_access_to_object(self):
        user = User.objects.get(username='anton')
        permissions = viewsets.SinglePermissionGenericViewSet().get_object_permission_required()
        self.assertTrue(all([user.has_perm(perm) for perm in permissions]))

        self.assertTrue(self.client.login(username='anton', password='secr3t'))
        response = self.client.get(reverse('single_permission_generic_viewset-detail', args=(1,)))
        self.assertEqual(200, response.status_code)

    def test_user_with_partial_object_permissions_gets_no_access_to_object(self):
        user = User.objects.get(username='beatrix')
        viewset = viewsets.MultiplePermissionsGenericViewSet()
        permissions = viewset.get_object_permission_required()
        obj = viewset.queryset.get(pk=1)
        self.assertTrue(any([not user.has_perm(perm, obj) for perm in permissions]))

        self.assertTrue(self.client.login(username='beatrix', password='secr3t'))
        response = self.client.get(reverse('multiple_permissions_generic_viewset-detail', args=(1,)))
        self.assertEqual(403, response.status_code)

    def test_user_without_object_permission_gets_no_access_to_object(self):
        user = User.objects.get(username='carlos')
        viewset = viewsets.MultiplePermissionsGenericViewSet()
        permissions = viewset.get_object_permission_required()
        obj = viewset.queryset.get(pk=1)
        self.assertTrue(all([not user.has_perm(perm, obj) for perm in permissions]))

        self.assertTrue(self.client.login(username='carlos', password='secr3t'))
        response = self.client.post(reverse('multiple_permissions_generic_viewset-detail', args=(1,)))
        self.assertEqual(403, response.status_code)
