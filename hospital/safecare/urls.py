from django.urls import path
from .import views

# from .views import UserRegistrationAPI,LoginAPI


#Template URLS

urlpatterns=[
    #homepage
    path('', views.home, name='home'),

    #aboutus page
    path('about', views.about, name='about'),

    #departments page
    path('departments', views.departments, name='departments'),

    #contact page
    path('contact', views.contact, name='contact'),

    #login page
    path('login', views.login, name='login'),
    

    #register page
    # path('register', views.register, name='register'),



    # API URLS

    # User
#    path('user/', UserRegistrationAPI.as_view(), name="add_user"),

   #login
    # path('loginpage/', LoginAPI.as_view(), name="loginpage"),

    # path('api/auth/login/', TokenObtainPairView.as_view()),

    # path('api/auth/refresh/', TokenRefreshView.as_view()),


    # # Patient
#    path('user/<int:id>', PatientViewSet.as_view(), name="user"),

]