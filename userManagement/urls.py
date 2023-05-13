from django.urls import path
from .views import Register, signin,StudentList, StudentDetails
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'userManagement'

urlpatterns = [
    path('signin/', signin, name='login'),
    path('register/', Register.as_view(), name='register'),
    path('students/', StudentList.as_view(), name='student-list'),
    path('students/<int:pk>', StudentDetails.as_view(), name='student-details'),

]
