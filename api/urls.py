from django.urls import path,include
from.import views
from rest_framework.routers import DefaultRouter


rounter=DefaultRouter()

rounter.register("student/register",views.studentresgister, basename="stundentregister")
rounter.register("teacher/register", views.teacheresgister, basename="teacherregister")
rounter.register("teacher/list", views.teacherlist, basename='teachlist')
rounter.register("student/list", views.studentlist, basename="studentlist")
rounter.register("user/list", views.UserList,basename="userlist")

urlpatterns = [
	path("", include(rounter.urls)),
    path('restpassword', views.Resetpasswordview.as_view()),
    path('password-rest/<uidb64>/<token>/', views.PasswordTokenCheckApi.as_view(), name='password-rest-confirm'),
    path('password-reset-complete', views.setnewpassword.as_view(), name='password-reset-complete'),

]
