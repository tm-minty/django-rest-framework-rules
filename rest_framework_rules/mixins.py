from django.core.exceptions import ImproperlyConfigured


class PermissionRequiredMixin:

    object_permission_required = None
    permission_required = None

    def get_permission_required(self):

        if self.permission_required is None:
            # This prevents a misconfiguration of the view into which the mixin
            # is mixed. If the mixin is used, at least one permission should be
            # required.
            raise ImproperlyConfigured(
                '{0} is missing the permission_required attribute. Define '
                '{0}.permission_required, or override '
                '{0}.get_permission_required().'
                .format(self.__class__.__name__)
            )

        if isinstance(self.permission_required, str):
            perms = (self.permission_required, )
        else:
            perms = self.permission_required

        return perms

    def get_object_permission_required(self):

        if self.object_permission_required is None:
            return self.get_permission_required()

        if isinstance(self.object_permission_required, str):
            perms = (self.object_permission_required, )
        else:
            perms = self.object_permission_required

        return perms

    def check_object_permissions(self, request, obj):
        user = request.user
        missing_permissions = [
            perm for perm in self.get_object_permission_required()
            if not user.has_perm(perm, obj)
        ]
        if any(missing_permissions):
            self.permission_denied(
                request,
                message=('MISSING: {}'.format(', '.join(missing_permissions))))

    def check_permissions(self, request):
        user = request.user
        missing_permissions = [perm for perm in self.get_permission_required()
                               if not user.has_perm(perm)]
        if any(missing_permissions):
            self.permission_denied(
                request,
                message=('MISSING: {}'.format(', '.join(missing_permissions))))
