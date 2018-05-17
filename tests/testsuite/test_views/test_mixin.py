from __future__ import absolute_import

import rules
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import reverse
from rest_framework.test import APITestCase
from testapp.models import Book
from testapp import views


class PermissionRequiredMixedAPIViewTests(APITestCase):

    """Tests the behavior of the mixin when used on an APIView
    """

    def test_user_with_permission_gets_access(self):
        user = User.objects.get(username='anton')
        permissions = views.SinglePermissionView().get_permission_required()
        self.assertTrue(all([user.has_perm(perm) for perm in permissions]))

        self.assertTrue(self.client.login(username='anton', password='secr3t'))
        response = self.client.get(reverse('single_permission_view'))
        self.assertEqual(200, response.status_code)

    def test_user_without_permission_gets_no_access(self):
        user = User.objects.get(username='beatrix')
        permissions = views.SinglePermissionView().get_permission_required()
        self.assertTrue(any([not user.has_perm(perm) for perm in permissions]))

        self.assertTrue(self.client.login(username='beatrix', password='secr3t'))
        response = self.client.get(reverse('single_permission_view'))
        self.assertEqual(403, response.status_code)

    def test_user_with_permissions_gets_access(self):
        user = User.objects.get(username='anton')
        permissions = views.MultiplePermissionsView().get_permission_required()
        self.assertTrue(all([user.has_perm(perm) for perm in permissions]))

        self.assertTrue(self.client.login(username='anton', password='secr3t'))
        response = self.client.get(reverse('multiple_permissions_view'))
        self.assertEqual(200, response.status_code)

    def test_user_with_partial_permissions_gets_no_access(self):
        user = User.objects.get(username='beatrix')
        permissions = views.MultiplePermissionsView().get_permission_required()
        self.assertTrue(any([not user.has_perm(perm) for perm in permissions]))

        self.assertTrue(self.client.login(username='beatrix', password='secr3t'))
        response = self.client.get(reverse('multiple_permissions_view'))
        self.assertEqual(403, response.status_code)

    def test_user_without_permissions_gets_no_access(self):
        user = User.objects.get(username='carlos')
        permissions = views.MultiplePermissionsView().get_permission_required()
        self.assertTrue(all([not user.has_perm(perm) for perm in permissions]))

        self.assertTrue(self.client.login(username='carlos', password='secr3t'))
        response = self.client.get(reverse('multiple_permissions_view'))
        self.assertEqual(403, response.status_code)

    def test_improperly_configured_api_view_raises(self):
        with self.assertRaises(ImproperlyConfigured):
            response = self.client.get(reverse('improperly_configured_api_view'))


class PermissionRequiredMixedGenericAPIViewTests(APITestCase):

    """Tests the behavior of the mixin when used on a GenericAPIView
    """

    def test_object_permission_falls_back_to_required_permissions(self):
        view = views.GenericViewWithoutObjectPermissions()
        self.assertEquals(None, view.object_permission_required)
        self.assertEquals(view.get_permission_required(),
                          view.get_object_permission_required())

    def test_user_with_object_permission_gets_access_to_object(self):
        user = User.objects.get(username='anton')
        permissions = views.SinglePermissionGenericView().get_object_permission_required()
        self.assertTrue(all([user.has_perm(perm) for perm in permissions]))

        self.assertTrue(self.client.login(username='anton', password='secr3t'))
        response = self.client.post(reverse('single_permission_generic_view', args=(1,)))
        self.assertEqual(200, response.status_code)

    def test_user_with_object_permissions_gets_access_to_object(self):
        user = User.objects.get(username='anton')
        permissions = views.MultiplePermissionsGenericView().get_object_permission_required()
        self.assertTrue(all([user.has_perm(perm) for perm in permissions]))

        self.assertTrue(self.client.login(username='anton', password='secr3t'))
        response = self.client.post(reverse('multiple_permissions_generic_view', args=(1,)))
        self.assertEqual(200, response.status_code)

    def test_user_with_partial_object_permissions_gets_no_access_to_object(self):
        user = User.objects.get(username='beatrix')
        view = views.MultiplePermissionsGenericView()
        permissions = view.get_object_permission_required()
        obj = view.queryset.get(pk=1)
        self.assertTrue(any([not user.has_perm(perm, obj) for perm in permissions]))

        self.assertTrue(self.client.login(username='beatrix', password='secr3t'))
        response = self.client.post(reverse('multiple_permissions_generic_view', args=(1,)))
        self.assertEqual(403, response.status_code)

    def test_user_without_object_permission_gets_no_access_to_object(self):
        user = User.objects.get(username='carlos')
        view = views.MultiplePermissionsGenericView()
        permissions = view.get_object_permission_required()
        obj = view.queryset.get(pk=1)
        self.assertTrue(all([not user.has_perm(perm, obj) for perm in permissions]))

        self.assertTrue(self.client.login(username='carlos', password='secr3t'))
        response = self.client.post(reverse('multiple_permissions_generic_view', args=(1,)))
        self.assertEqual(403, response.status_code)
