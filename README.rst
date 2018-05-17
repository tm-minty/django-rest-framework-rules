django-rest-framework-rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^

``django-rest-framework-rules`` aims to seamlessly integrate ``rules`` -  a tiny but powerful app providing object-level permissions - into the Django REST framework.

Parts of the original `django-rules documentation`_ were used to improve the reading experience of this document.

Table of Contents
=================

- `Requirements`_
- `Run tests`_
- `How to install`_
- `Using rest_framework_rules`_

  - `PermissionRequiredMixin with the APIView and GenericAPIView`_
  - `PermissionRequiredMixin with the ViewSet and GenericViewSet`_
  - `permission_required decorator with APIView and ViewSet methods`_
  - `using list_route and detail_route decorator with the PermissionRequiredMixin`_

- `Changelog`_
- `Licence`_

Requirements
============

This package was made to be used with ``Django``, ``django-rules`` and the ``django-rest-framework``.

Build status
============

.. image:: https://travis-ci.org/escodebar/django-rest-framework-rules.svg?branch=master

Run tests
=========

.. code:: bash

    $ git clone http://github.com/escodebar/django-rest-framework-rules.git
    $ cd django-rest-framework-rules
    $ python3 -m venv . && source bin/activate
    $ pip install -r requirements_test.txt
    $ (django-rest-framework-rules) ./runtests.sh

How to install
==============

Using pip:

.. code:: bash

    $ pip install django-rest-framework-rules

Using rest_framework_rules
==========================

``rest_framework_rules`` aims to integrate ``rules`` permission system into the Django REST framework.

    ``rules`` is based on the idea that you maintain a dict-like object that maps string keys used as identifiers of some kind, to callables, called *predicates*.
    Predicates can do pretty much anything with the given arguments, but must always return True if the condition they check is true, False otherwise.
    (Read more about rules in the `django-rules documentation - Using Rules`_.)

For a better illustration of the usage of ``rest_framework_rules`` let's assume the following setup:
We are proud owners of an app (climb-app!) which allows routesetters to advertise their newly created routes / boulders.
The climbers can use the app to review the routes / boulders and propose solutions for these.

Given such an application, one could think of the following permissions:

Routesetters may
- create new boulders
- retrieve boulders' details
- update their boulders
- delete their boulders
- retrieve their boulders' reviews
- retrieve their boulders' solutions

Climbers may
- retrieve boulders' details
- create boulder reviews
- retrieve boulders' reviews
- update their reviews
- delete their reviews
- create a boulder solution
- retrieve boulders' solutions
- update their boulder solutions
- delete their boulder solutions

Let's define some predicates and the beforementioned permissions (this code usually resides in ``rules.py`` in your application folder).

.. code:: python

    from climb_app.models import Climber, RouteSetter
    import rules
    
    @rules.predicate
    def is_a_climber(user):
        return Climber.objects.filter(user=user).exists()

    @rules.predicate
    def is_a_routesetter(user):
        return RouteSetter.objects.filter(user=user).exists()

    @rules.predicate
    def is_related_to_routesetters_boulder(user, content=None):
        if content is None or not hasattr(content, 'boulder'):
            return False
        return content.boulder.routesetter == user

    @rules.predicate
    def object_is_none(user, obj=None):
        return obj is None

    @rules.predicate
    def is_author(user, content):
        if not hasattr(content, 'author'):
            return False
        return content.author == user

    rules.add_perm('climb_app.create_boulder', is_a_routesetter)
    rules.add_perm('climb_app.retrieve_boulder', is_a_climber | is_a_routesetter & is_author)
    rules.add_perm('climb_app.update_boulder', is_a_routesetter & is_author)
    rules.add_perm('climb_app.delete_boulder', is_a_routesetter & is_author)
    rules.add_perm('climb_app.retrieve_reviews', is_a_routesetter)
    rules.add_perm('climb_app.retrieve_climbers', is_a_routesetter)

    rules.add_perm('climb_app.create_climber_content', is_a_climber)
    rules.add_perm('climb_app.retrieve_climber_content',
                   (is_a_climber |
                    is_a_routesetter & is_related_to_routesetters_boulder |
                    is_a_routesetter & object_is_none))
    rules.add_perm('climb_app.update_climber_content', is_a_climber & is_author)
    rules.add_perm('climb_app.delete_climber_content', is_a_climber & is_author)

PermissionRequiredMixin with the APIView and GenericAPIView
-----------------------------------------------------------

The ``PermissionRequiredMixin`` allows to define a required permission name (``permission_required``).
This permission name (or list of such) is needed by the request's user to access the methods of the view.

I could think of the following use case within climb-app!
Let's allow climbers to *check* boulders once they were able to solve them.
(This is basically adding a solution without data.)

.. code:: python

    from climb_app.models import Boulder, Solution
    from rest_framework.response import Response
    from rest_framework.views import APIView
    from rest_framework_rules.mixins import PermissionRequiredMixin

    class CheckmarkBoulderView(PermissionRequiredMixin, APIView):
        permission_required = 'climb_app.create_climber_content'

        def get(self, request, *args, **kwargs):
            solution, created = Solution.objects.get_or_create(
                user=request.user,
                boulder=Boulder.objects.get(pk=kwargs.get('boulder_pk')),
            )
            if created:
                return Response(status=204)
            return Response(status=304)

When used with a ``GenericAPIView``, the ``PermissionRequiredMixin`` allows to define an ``object_permission_required`` (defaults to ``permission_required`` if not set).
This permission (or list of permissions) is required by the request's user to call the ``get_object`` method of the view.

In the context of climb-app! this could be used with the views for retrieving and updating boulder reviews:

.. code:: python

    from climb_app.models import Review
    from climb_app.serializer import ReviewSerializer
    from rest_framework.generics import GenericAPIView
    from rest_framework.response import Response
    from rest_framework_rules.mixins import PermissionRequiredMixin

    class RetrieveReviewView(PermissionRequiredMixin, GenericAPIView):
        permission_required = 'climb_app.retrieve_climber_content'
        queryset = Review.objects.all()

        def get(self, request, *args, **kwargs):
            review = self.get_object()
            serializer = ReviewSerializer(review)
            return Response(data=serializer.data)

    class CreateOrUpdateReviewView(PermissionRequiredMixin, GenericAPIView):
        object_permission_required = 'climb_app.update_climber_content'
        permission_required = 'climb_app.create_climber_content'
        queryset = Review.objects.all()

        def post(self, request, *args, **kwargs):
            solution, created = Review.objects.get_or_create(
                user=request.user,
                boulder=Boulder.objects.get(pk=kwargs.get('boulder_pk')),
            )
            if created:
                return Response(status=204)
            return Response(status=304)

        def put(self, request, *args, **kwargs):
            review = self.get_object()
            # update review...
            return Response(status=204)

PermissionRequiredMixin with the ViewSet and GenericViewSet
-----------------------------------------------------------

The ``PermissionRequiredMixin`` can be used as well with ``ViewSet`` and ``GenericViewSet``.
The user need to have the ``permission_required`` to call actions of a viewset and ``object_permission_required`` (which defaults to ``permission_required`` if not set) to call ``get_object``.

Let's use this in climb app! to allow routesetters to create, delete boulders and list the reviews of their boulders.

.. code:: python

    from climb_app.models import Boulder, Review
    from climb_app.serializers import BoulderSerializer, ReviewSerializer
    from rest_framework.response import Response
    from rest_framework.viewsets import GenericViewSet, ViewSet
    from rest_framework_rules.mixins import PermissionRequiredMixin

    class ReviewViewSet(PermissionRequiredMixin, ViewSet):
        permission_required = 'climb_app.retrieve_reviews'

        def list(self, request):
            queryset = Review.objects.filter(boulder__author=request.user)
            serializer = ReviewSerializer(queryset, many=True)
            return Response(serializer.data)

    class BoulderViewSet(PermissionRequiredMixin, GenericViewSet):
        object_permission_required = 'climb_app.delete_boulder'
        permission_required = 'climb_app.create_boulder'

        def create(self, request, *args, **kwargs):
            # create boulders...
            return Response(status=204)

        def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            instance.delete()
            return Response(status=204)

permission_required decorator with APIView and ViewSet methods
--------------------------------------------------------------

Permissions can be set using the ``permission_required`` decorator.
The required permission(s) is passed as first argument to the decorator.
The decorator also has an optional ``fn`` argument, which is either the context object itself or a callable returning the context object.
The arguments passed to the context object callable are the same as the ones of the decorated method.

.. code:: python

    from climb_app.models import Boulder, Solution
    from rest_framework.response import Response
    from rest_framework.views import APIView
    from rest_framework_rules.decorators import permission_required

    class CheckmarkBoulderView(APIView):

        @permission_required('climb_app.create_climber_content')
        def get(self, request, *args, **kwargs):
            solution, created = Solution.objects.get_or_create(
                user=request.user,
                boulder=Boulder.objects.get(pk=kwargs.get('boulder_pk')),
            )
            if created:
                return Response(status=204)
            return Response(status=304)


    class BoulderViewSet(ViewSet):

        @permission_required('climb_app.access_method')
        def create(self, request):
            # create boulder...
            return Response(status=204)

        @permission_required(
            'someapp.access_method',
            fn=lambda request, pk: Boulder.objects.get(pk=pk))
        def destroy(self, request, pk):
            boulder = Boulder.objects.get(pk=pk)
            boulder.delete()
            return Response(status=204)


using list_route and detail_route decorator with the PermissionRequiredMixin
----------------------------------------------------------------------------

``rest_framework`` provides the decorators ``list_route`` and ``detail_route`` to define custom routes in viewsets.
These can be used as well with ``django-rest-framework-rules`` under the condition, that the ``ViewSet`` is mixed with the ``PermissionRequiredMixin``.

Let's add some custom routes to the ``BoulderViewSet`` defined in climb-app! to allow routesetter to retrieve all reviews of a boulder and list all climbers which have solved the routesetter's boulders.

.. code:: python

    from rest_framework.decorators import list_route, detail_route
    from rest_framework.response import Response
    from rest_framework.viewsets import ViewSet
    from rest_framework_rules.mixins import PermissionRequiredMixin

    class BoulderViewSet(PermissionRequiredMixin, GenericViewSet):
        object_permission_required = 'climb_app.delete_boulder'
        permission_required = 'climb_app.create_boulder'

        def create(self, request, *args, **kwargs):
            # create boulders...
            return Response(status=204)

        def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            instance.delete()
            return Response(status=204)

        @detail_route(methods=['get'], permission_required='climb_app.retrieve_reviews')
        def reviews(self, request, pk):
            boulder = self.get_object()
            queryset = (Review.objects
                        .filter(boulder=boulder)
                        .order_by('created'))
            serializer = ReviewSerializer(queryset=queryset, many=True)
            return Response(serializer.data)

        @list_route(methods=['get'], permission_required='climb_app.retrieve_climbers')
        def climbers(self, request):
            queryset = Climber.objects.filter(solution__boulder__author=request.user).distinct()
            serializer = ClimberSerializer(queryset=queryset, many=True)
            return Response(serializer.data)

Changelog
=========

``v1.0.0`` - 2018/05/15
    - Dropped python 2.7 support.

``v0.1.1`` - 2017/11/17
    - Improve README and package setup.

``v0.1.0`` - 2017/11/13
    - Implemented PermissionRequiredMdddixin, permission_required decorator and the django rest framework integration tests.

``v0.0.1`` - 2017/10/30
    - Forked from https://github.com/dfunckt/django-rules


Licence
=======

``django-rest-framework-rules`` is distributed under the MIT licence.

Copyright (c) 2017 Pablo Escodebar

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

.. _django-rules documentation: https://github.com/dfunckt/django-rules/blob/7688fdac68e7de6832f28f7b96ebf1f98f32f3c8/README.rst
.. _django-rules documentation - Using Rules: https://github.com/dfunckt/django-rules/blob/7688fdac68e7de6832f28f7b96ebf1f98f32f3c8/README.rst#using-rules

