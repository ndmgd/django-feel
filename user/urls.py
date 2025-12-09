from django.urls import path

from user.views import TestView, JwtTestView

urlpatterns = [
    path("test", TestView.as_view(), name="test"),
    path("jwt_test", JwtTestView.as_view(), name="jwt_test"),
]
