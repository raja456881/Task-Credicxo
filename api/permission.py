from rest_framework.permissions import BasePermission
from .models import User

# Permissions class for admin
class adminpermission(BasePermission):

	def has_permission(self, request, view):
		if request.user.is_superuser==True and request.user.is_authenticated:
			return True
		return False


#Permissions class for teacher
class teacherpermission(BasePermission):
	def has_permission(self, request, view):
		try:
			user=request.user
			user1=User.objects.get(email=user.email)
			if  user1.is_teacher==True and user1.is_authenticated:
				return True
		except :
			return False


# Permissions class for student
class studentpermission(BasePermission):
	def has_permission(self, request, view):
		try:
			user=request.user
			user1=User.objects.get(email=user.email)
			if user1.is_student==True and user1.is_authenticated:
				return True
		except :
			return False


