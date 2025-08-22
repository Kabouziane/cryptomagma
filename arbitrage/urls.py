from django.urls import path
from . import views

app_name = 'arbitrage'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('update-prices/', views.update_prices, name='update_prices'),
    path('api/opportunities/', views.api_opportunities, name='api_opportunities'),
]