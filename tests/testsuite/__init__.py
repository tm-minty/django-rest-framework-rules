from django.contrib.auth.models import User, Group
from testapp.models import Book

import testapp.rules  # to register rules


def setup_package():
    anton = User.objects.create_user('anton', password='secr3t')
    beatrix = User.objects.create_user('beatrix', password='secr3t')
    carlos = User.objects.create_user('carlos', password='secr3t')

    Book.objects.create(title="anton's book", author=anton)
    Book.objects.create( title="beatrix' book", author=beatrix)
    Book.objects.create(title="carlos' book", author=carlos)


def teardown_package():
    Book.objects.get(title="anton's book").delete()
    Book.objects.get(title="beatrix' book").delete()
    Book.objects.get(title="carlos' book").delete()
    User.objects.get(username='anton').delete()
    User.objects.get(username='beatrix').delete()
    User.objects.get(username='carlos').delete()
