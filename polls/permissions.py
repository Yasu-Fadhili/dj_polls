from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # This method is called for all requests.
        # Here, we allow read-only access for everyone.
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # This method is called for individual objects (in this case, polls).
        # Here, we can check if the user is the author of the poll.
        return obj.author == request.user
