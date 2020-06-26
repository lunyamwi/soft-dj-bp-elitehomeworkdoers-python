from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('payments/',include('payments.urls')),
    path('',views.IndexView,name='index'),
    path('about/',views.AboutView,name='about'),
    path('assignments/',include('assignments.urls')),
    path('authentication/',include('authentication.urls')),
    path('user/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
