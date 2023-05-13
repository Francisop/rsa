from django.urls import path
from .views import Term, Session, TermDetail, SessionDetail,Class, Teacher, TeacherDetail
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'schoolManagement'

urlpatterns = [
    path('term/', Term.as_view(), name='term'),
    path('session/', Session.as_view(), name='session'),
    path('term/<int:pk>/', TermDetail.as_view(), name="term-detail"),
    path('session/<int:pk>/', SessionDetail.as_view(), name='session-detail'),
    path('class/', Class.as_view(), name='class'),
    path('teacher/', Teacher.as_view(), name='teacher'),
    path('teacher/<int:pk>/', TeacherDetail.as_view(), name='teacher-detail'),

]
