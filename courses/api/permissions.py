from rest_framework.permissions import BasePermission, exceptions

from utils.helper import get_user_uuid


class IsEnrolled(BasePermission):
    message = {'error': 'You are not enrolled!'}

    def has_object_permission(self, request, view, obj):
        token = request.headers.get('token')
        if not token:
            return False
        user_uuid = get_user_uuid(token)
        if not user_uuid:
            return False
        is_permitted = obj.students.filter(uuid=user_uuid).exists()
        if is_permitted:
            return is_permitted
        else:
            raise exceptions.PermissionDenied(detail=self.message)
