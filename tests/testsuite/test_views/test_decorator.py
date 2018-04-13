from __future__ import absolute_import

import rules
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import reverse
from django.utils.encoding import force_str
from rest_framework.test import APITestCase
from testapp.models import Book
from testapp import views


class PermissionRequiredDecoratedAPIViewTests(APITestCase):

    """Tests the behavior of the mixin when used on an APIView
    """

    def test_user_with_permission_gets_access(self):
        user = User.objects.get(username='anton')
        # assert that the user has the right permission

        self.assertTrue(self.client.login(username='anton', password='secr3t'))
        response = self.client.get(reverse('decorated_view'))
        self.assertEqual(200, response.status_code)

    def test_user_without_permission_gets_no_access(self):
        user = User.objects.get(username='beatrix')
        # assert that the user has no permissions

        self.assertTrue(self.client.login(username='beatrix', password='secr3t'))
        response = self.client.get(reverse('decorated_view'))
        self.assertEqual(403, response.status_code)

    def test_user_with_object_permission_gets_access(self):
        user = User.objects.get(username='anton')
        # assert that the user has the right permission

        self.assertTrue(self.client.login(username='anton', password='secr3t'))
        response = self.client.head(reverse('decorated_view'))
        self.assertEqual(200, response.status_code)

    def test_user_without_object_permission_permission_gets_no_access(self):
        user = User.objects.get(username='beatrix')
        # assert that the user has no permissions

        self.assertTrue(self.client.login(username='beatrix', password='secr3t'))
        response = self.client.head(reverse('decorated_view'))
        self.assertEqual(403, response.status_code)

    def test_user_with_permissions_gets_access(self):
        user = User.objects.get(username='anton')
        # assert that the user has the right permissions

        self.assertTrue(self.client.login(username='anton', password='secr3t'))
        response = self.client.patch(reverse('decorated_view'))
        self.assertEqual(200, response.status_code)

    def test_user_with_partial_permissions_gets_no_access(self):
        user = User.objects.get(username='beatrix')
        # assert that the user has not all permissions

        self.assertTrue(self.client.login(username='beatrix', password='secr3t'))
        response = self.client.patch(reverse('decorated_view'))
        self.assertEqual(403, response.status_code)
        
    def test_user_without_permissions_gets_no_access(self):
        user = User.objects.get(username='carlos')
        # assert that the user has no permissions

        self.assertTrue(self.client.login(username='carlos', password='secr3t'))
        response = self.client.patch(reverse('decorated_view'))
        self.assertEqual(403, response.status_code)

    def test_user_with_object_permissions_gets_access(self):
        user = User.objects.get(username='anton')
        # assert tha the user has the right permissions

        self.assertTrue(self.client.login(username='anton', password='secr3t'))
        response = self.client.post(reverse('decorated_view'))
        self.assertEqual(200, response.status_code)

    def test_user_with_partial_permissions_gets_no_access(self):
        user = User.objects.get(username='beatrix')
        # assert that the user has not all permissions

        self.assertTrue(self.client.login(username='beatrix', password='secr3t'))
        response = self.client.post(reverse('decorated_view'))
        self.assertEqual(403, response.status_code)
        
    def test_user_without_permissions_gets_no_access(self):
        user = User.objects.get(username='carlos')
        # assert that the user has no permissions

        self.assertTrue(self.client.login(username='carlos', password='secr3t'))
        response = self.client.post(reverse('decorated_view'))
        self.assertEqual(403, response.status_code)
