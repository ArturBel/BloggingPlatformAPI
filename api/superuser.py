from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.exceptions import PermissionDenied


User = get_user_model()


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]

    def perform_update(self, serializer):
        readonly_fields = [
        'first_name',
        'last_name',
        'date_joined',
        'username',
        'email',
        'password',
        ]

        for field in readonly_fields:
            if field in serializer.validated_data:
                raise PermissionDenied(
                    f"You are not allowed to modify the '{field}' field."
                )

        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user == instance:
            raise PermissionDenied("You cannot delete your own superuser account.")
        else:
            instance.delete()
    
