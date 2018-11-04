from django.conf.urls import include, url
from driver import views

urlpatterns = [
    url(r'^ride/', views.Rides.as_view())
]
