django-rest-framework-rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^

``django-rest-framework-rules`` aims to seamlessly integrate ``rules`` -  a tiny but powerful app providing object-level permissions - into the Django REST framework.

Please visit https://github.com/dfunckt/django-rules for a more detailed description on how to configure rules and  define predicates, rules and permissions.

Table of Contents
=================

- `Requirements`_
- `How to install`_

  - `Configuring Django`_

- `Using rest_framework_rules`_

  - `PermissionRequiredMixin with the APIView and GenericAPIView`_
  - `PermissionRequiredMixin with the ViewSet and GenericViewSet`_
  - `permission_required decorator with APIView and ViewSet methods`_
  - `using list_route and detail_route decorator with the PermissionRequiredMixin`_

- `Changelog`_
- `Licence`_

Requirements
============

How to install
==============

Manually:

.. code:: bash

    $ git clone https://github.com/escodebar/django-rest-framework-rules.git
    $ cd django-rest-framework-rules
    $ python setup.py install

Run tests with:

.. code:: bash

    $ ./runtests.sh


Configuring Django
------------------

Add ``rest_framework_rules`` to ``INSTALLED_APPS``:

.. code:: python

    INSTALLED_APPS = (
        # ...
        'rest_framework',
        'rest_framework_rules',
        'rules',
    )

Using rest_framework_rules
==========================

PermissionRequiredMixin with the APIView and GenericAPIView
-----------------------------------------------------------

Example:

.. code:: python

    from rest_framework.generics import GenericAPIView
    from rest_framework.views import APIView
    from rest_framework_rules.mixins import PermissionRequiredMixin

    class SomeView(PermissionRequiredMixin, APIView):
        permission_required = 'someapp.access_view'

    class SomeGenericAPIView(PermissionRequiredMixin, GenericAPIView):
        object_permission_required = 'someapp.access_model_instance'
        permission_required = 'someapp.access_generic_view'

PermissionRequiredMixin with the ViewSet and GenericViewSet
-----------------------------------------------------------

Example:

.. code:: python

    from rest_framework.viewsets import GenericViewSet, ViewSet
    from rest_framework_rules.mixins import PermissionRequiredMixin

    class SomeViewSet(PermissionRequiredMixin, ViewSet):
        permission_required = 'someapp.access_viewset'

    class SomeGenericViewSet(PermissionRequiredMixin, GenericViewSet):
        object_permission_required = 'someapp.access_model_instance'
        permission_required = 'someapp.access_generic_viewset'

permission_required decorator with APIView and ViewSet methods
--------------------------------------------------------------

Example

.. code:: python

    from rest_framework.views import APIView
    from rest_framework.viewsets import ViewSet
    from rest_framework_rules.decorators import permission_required
    from someapp.models import SomeModel

    class SomeView(APIView):

        @permission_required('someapp.access_method')
        def get(self, request, *args, **kwargs):
            pass

        @permission_required(
            'someapp.access_method',
            fn=lambda request, *args, **kwargs: SomeModel.objects.get(pk=kwargs.get('pk')))
        def post(self, request, *args, **kwargs):
            pass

    class SomeViewSet(ViewSet):

        @permission_required('someapp.access_method')
        def list(self, request):
            pass

        @permission_required(
            'someapp.access_method',
            fn=lambda request, pk: SomeModel.objects.get(pk=pk))
        def retrieve(self, request, pk):
            pass

using list_route and detail_route decorator with the PermissionRequiredMixin
----------------------------------------------------------------------------

Example

.. code:: python

    from rest_framework.decorators import list_route, detail_route
    from rest_framework.viewsets import ViewSet
    from rest_framework_rules.mixins import PermissionRequiredMixin

    class SomeViewSet(PermissionRequiredMixin, ViewSet):

        @list_route(methods=['get'], permission_required='someapp.access_route')
        def some_list(self, request):
            pass

        @detail_route(methods=['post'],
                      permission_required='someapp.access_route',
                      object_permission_required='someapp.access_model_instance')
        def some_detail(self, request, pk=None):
            pass

Changelog
=========

``v0.1.0`` - 2017/11/13
    - Implemented PermissionRequiredMixin, permission_required decorator and the django rest framework integration tests.

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
