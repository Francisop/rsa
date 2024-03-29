from django.urls import path
from .views import Term, Session, TermDetail, SessionDetail, Class, TeacherView, TeacherDetail, ClassDetail, \
    filter_student_by_class, Result, active, promote_student, filter_result_by_class
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'schoolManagement'

urlpatterns = [
    path('term/', Term.as_view(), name='term'),
    path('session/', Session.as_view(), name='session'),
    path('term/<int:pk>/', TermDetail.as_view(), name="term-detail"),
    path('session/<int:pk>/', SessionDetail.as_view(), name='session-detail'),
    path('class/', Class.as_view(), name='class'),
    path('class/<int:pk>/', ClassDetail.as_view(), name='class'),
    path('teacher/', TeacherView.as_view(), name='teacher'),
    path('teacher/<int:pk>/', TeacherDetail.as_view(), name='teacher-detail'),
    path('filter/<int:pk>/', filter_student_by_class, name='filter'),
    path('result/', Result.as_view(), name='result'),
    path('filter/result/<int:pk>/', filter_result_by_class, name='result-filter'),
    path('promote/<int:pk>/', promote_student, name='promote-student'),
    path('active/', active, name='active'),

]
