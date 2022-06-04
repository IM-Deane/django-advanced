from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('hello/', views.say_hello),
    path('hey/', views.cached_view),
    path('class/', views.CachedClassView.as_view()),
]
