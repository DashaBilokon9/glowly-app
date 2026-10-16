from django.urls import path

from salon import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('services/', views.service_list, name='service_list'),
    path('specialists/<int:pk>/', views.specialist_detail, name='specialist_detail'),
    path('book/', views.appointment_create, name='appointment_create'),
    path('book/done/', views.appointment_done, name='appointment_done'),
]
