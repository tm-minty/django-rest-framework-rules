from __future__ import absolute_import

import rules


# Predicates

@rules.predicate
def is_anton(user, target):
    return user.username == 'anton'

@rules.predicate
def is_beatrix(user, target):
    return user.username == 'beatrix'

@rules.predicate
def is_carlos(user, target):
    return user.username == 'carlos'

@rules.predicate
def is_author(user, target):
    return user == target.author


# Permissions

rules.add_perm('testapp.access_single_permission_view', is_anton)
rules.add_perm('testapp.access_multiple_permissions_view_1', is_anton)
rules.add_perm('testapp.access_multiple_permissions_view_2', is_anton | is_beatrix)

rules.add_perm('testapp.access_single_permission_generic_view', is_anton)
rules.add_perm('testapp.access_multiple_permissions_generic_view', is_anton | is_beatrix)
rules.add_perm('testapp.access_single_permission_object', is_anton)
rules.add_perm('testapp.access_multiple_permissions_object_1', is_anton)
rules.add_perm('testapp.access_multiple_permissions_object_2', is_anton | is_beatrix)

rules.add_perm('testapp.access_single_permission_method', is_anton)
rules.add_perm('testapp.access_multiple_permissions_method_1', is_anton)
rules.add_perm('testapp.access_multiple_permissions_method_2', is_anton | is_beatrix)
rules.add_perm('testapp.access_single_object_permission_method', is_anton)
rules.add_perm('testapp.access_multiple_object_permissions_method_1', is_anton)
rules.add_perm('testapp.access_multiple_object_permissions_method_2', is_anton | is_beatrix)

rules.add_perm('testapp.access_single_permission_viewset', is_anton)
rules.add_perm('testapp.access_multiple_permissions_viewset_1', is_anton)
rules.add_perm('testapp.access_multiple_permissions_viewset_2', is_anton | is_beatrix)

rules.add_perm('testapp.access_single_permission_generic_viewset', is_anton)

rules.add_perm('testapp.access_single_permission_detail_route', is_anton)
rules.add_perm('testapp.access_multiple_permissions_detail_route_1', is_anton)
rules.add_perm('testapp.access_multiple_permissions_detail_route_2', is_anton | is_beatrix)
