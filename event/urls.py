from django.urls import path
from . import views
from .forms import *
from django.urls import path
from .views import user_login, password_reset
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.index,name="index"),
    path('register',views.register,name="register"),
    path('login',views.user_login,name="login"),
    # path('contact',views.contact,name="contact"),
    path('addmin',views.admin_login,name="addmin"),
    path('logout', views.user_logout, name="logout"),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('Contactview/', views.contact_view, name='Contactview'),

    path('usershow/', views.usershow, name='usershow'),
    path('userdelete/<str:f_username>',views.userDelete,name="userdelete"),

    path('gallery', views.gallery, name='gallery'),
    # path('photo/', views.viewPhoto, name='photo'),
    path('delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add/', views.addPhoto, name='add'), 
    path('change_password/', views.change_password, name='change_password'),
    
    path('login/', user_login, name='login'),
    path('password_reset/', password_reset, name='password_reset'),

    path('wedviewplot',views.viewplotw,name="wedviewplot"),
    path('becholertheme',views.becholertheme,name="becholertheme"),
    path('receptiondest',views.receptiondest,name="receptiondest"),
    
    path('userprofile',views.userprofile,name="userprofile"),
    path('profile', views.profile_view, name='profile'),

    path('pdf_view/<str:order_type>/<int:order_id>/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/<str:order_type>/<int:order_id>/', views.DownloadPDF.as_view(), name="pdf_download"),

    
    path('complete_order/<str:order_type>/<int:order_id>/', views.complete_order, name='complete_order'),

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('send-feedback/', views.send_feedback, name='send_feedback'),

    path('showcall/', views.showcall, name='showcall'),
    path('search_call/', views.CallSearchView.as_view(), name='search_call'),

    path('sendmail/<str:email>', views.sendmail, name='sendmail'),
    path('senddelete/<str:email>', views.senddelete, name='senddelete'),






]