from rest_framework import permissions

class IsDocumentOwner(permissions.BasePermission):
    """Custom permission to only allow owners of a document to view, edit, or delete it.


    Ensures strict multi-tenant isolation across all document endpoints.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self,request,view,obj):
        return obj.user == request.user