from rest_framework import permissions


class CustomObjectPermissions(permissions.DjangoObjectPermissions):
    """!
    Clase que gestiona los roles y permisos de los usuarios en los endpoints

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        perms = self.get_required_permissions(request.method, view.model)
        return (request.user and request.user.has_perms(perms))

    def has_object_permission(self, request, view, obj):
        perms = self.get_required_permissions(request.method, view.model)
        return (request.user and request.user.has_perms(perms))
