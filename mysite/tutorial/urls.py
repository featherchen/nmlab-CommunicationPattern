from django.urls import path, re_path

from .views import EchoView1, EchoView2, Fibonacci, Logging

urlpatterns = [
    re_path(r'^fibonacci/?$', Fibonacci().as_view()),
    re_path(r'^logs/?$', Logging.as_view()),
]
