from django.conf.urls import url
from .views import test, initdb, generatexls

urlpatterns = [
    url(r'^new/', test),
    url(r'^initdb/', initdb),
    url(r'^genxl/', generatexls),
]