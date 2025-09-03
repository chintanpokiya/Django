from django.urls import path
from . import views
from .views import order_stats,chart_order

urlpatterns = [
    path('addmin',views.index,name="add-index"),
    path('api/order-stats/', order_stats, name='order_stats'),
    path('api/complete-order/<int:order_id>/', chart_order, name='complete_order'),
    path('uploadoption',views.uploadoption,name="uploadoption"),

]