from django.urls import path
from .views import Term, Session, TermDetail, SessionDetail
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'schoolManagement'

urlpatterns = [
    path('term/', Term.as_view(), name='term'),
    path('session/', Session.as_view(), name='session'),
    path('term/<int:pk>/', TermDetail.as_view(), name="term-detail"),
    path('session/<int:pk>/', SessionDetail.as_view(), name='session-detail'),
]
