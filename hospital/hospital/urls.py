from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),

    path('login/', TemplateView.as_view(template_name="login.html"), name="login-page"),

    path('patient-dashboard/',TemplateView.as_view(template_name="patient-dashboard.html")),

    path('doctor-dashboard/',TemplateView.as_view(template_name="doctor-dashboard.html")),

    path('admin-dashboard/', TemplateView.as_view(template_name="admin-dashboard.html")),

    path('patient-booking/',TemplateView.as_view(template_name="patient-booking.html")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
