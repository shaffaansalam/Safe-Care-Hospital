from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from authentication.views import DoctorDashboardTemplateView

urlpatterns = [

    # =========================
    # ADMIN
    # =========================

    path('admin/', admin.site.urls),

    # =========================
    # API ROUTES
    # =========================

    path('auth/', include('authentication.urls')),

    # =========================
    # FRONTEND PAGES
    # =========================

    path(
        '',
        TemplateView.as_view(
            template_name='home.html'
        ),
        name='home'
    ),

    path(
        'about/',
        TemplateView.as_view(
            template_name='about.html'
        ),
        name='about'
    ),

    path(
        'departments/',
        TemplateView.as_view(
            template_name='departments.html'
        ),
        name='departments'
    ),

    path(
        'contact/',
        TemplateView.as_view(
            template_name='contact.html'
        ),
        name='contact'
    ),

    path(
        'login/',
        TemplateView.as_view(
            template_name='login.html'
        ),
        name='login-page'
    ),

    path(
        'patient-dashboard/',
        TemplateView.as_view(
            template_name='patient-dashboard.html'
        ),
        name='patient-dashboard'
    ),

    path(
        'doctor-dashboard/',
        DoctorDashboardTemplateView.as_view(),
        name='doctor-dashboard'
    ),

    path(
        'admin-dashboard/',
        TemplateView.as_view(
            template_name='admin-dashboard.html'
        ),
        name='admin-dashboard'
    ),

    path(
        'patient-booking/',
        TemplateView.as_view(
            template_name='patient-booking.html'
        ),
        name='patient-booking'
    ),
]

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    