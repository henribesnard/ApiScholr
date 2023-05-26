from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


def admin_check(user):
    return user.is_authenticated and user.is_staff

class IsAdminUser(permissions.BasePermission):
    message = 'Admin access is required.'

    def has_permission(self, request, view):
        return admin_check(request.user)

def head_or_staff_check(user):
    return user.is_authenticated and (user.roles.filter(name='HEAD').exists() or user.roles.filter(name='STAFF').exists())

class IsHeadOrStaffUser(permissions.BasePermission):
    message = 'Head or Staff access is required.'

class IsStaffOrTeacherCreating(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.roles.filter(name__in=['HEAD', 'STAFF']).exists():
            return True
        elif request.method in SAFE_METHODS + ['POST',] and request.user.roles.filter(name='TEACHER').exists():
            return True
        
        return False
    
def parent_check(user):
    return user.is_authenticated and user.roles.filter(name='PARENT').exists()

def student_check(user):
    return user.is_authenticated and user.roles.filter(name='STUDENT').exists()

class IsParentUser(permissions.BasePermission):
    message = 'Parent access is required.'

    def has_permission(self, request, view):
        return parent_check(request.user)

class IsStudentUser(permissions.BasePermission):
    message = 'Student access is required.'

    def has_permission(self, request, view):
        return student_check(request.user)
