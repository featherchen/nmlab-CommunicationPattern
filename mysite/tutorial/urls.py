from django.urls import path, re_path

from .views import EchoView1, EchoView2

urlpatterns = [
    re_path(r'^fibonacci/?$', EchoView1.as_view()),
    re_path(r'^logs/?$', EchoView2.as_view()),
]
