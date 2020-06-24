from django.urls import path
from .views import ContactView

app_name="contacts"

urlpatterns = [
    path('',ContactView,name='home'),
]
