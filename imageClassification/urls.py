from django.urls import path
from . import views

urlpatterns=[
    path('', views.Landing, name='Landing'),
    path('index/', views.Index, name='Index'),
    path('createNew/', views.createNew, name='createNew'),
    path('uploadFile/', views.uploadFile, name='uploadFile'),
    path('SignupOrLogin/',views.SignupOrLogin, name="SignupOrLogin"),
    path('processSignup/',views.processSignup, name="processSignup"),
    path('processLogin/',views.processLogin, name="processLogin"),
    path('processPrediction/',views.processPrediction, name="processPrediction"),
    path('logout/',views.logout, name="logout"),
]