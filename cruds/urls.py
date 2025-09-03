from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('bechform/',views.becholerFormView,name='bechform'),   
    path('bechshow/', views.bechshow, name='bechshow'),
    path('bechdel/<int:f_oid>',views.bechDelete,name="bechdelete"),
    path('bechup/<int:f_oid>',views.bechUpdate,name="bechupdate"),
    path('bechpdf/<int:id>',views.bechpdf, name='bechpdf'),
    path('bechbulkupload/',views.bechbulkupload,name="bechbulkupload"),
    path('bechbulkuploadview/',views.bechbulkuploadview,name="bechbulkuploadview"),
    path('search-bech/', views.BechSearchView.as_view(), name='search_bech'),
    path('success/', views.success, name='success'),
    
    path('wedform/',views.weddingFormView,name='wedform'),   
    path('wedshow/', wedshow, name='wedshow'),
    path('weddel/<int:f_oid>',views.wedDelete,name="weddelete"),
    path('wedup/<int:f_oid>',views.wedUpdate,name="wedupdate"),
    path('wedpdf/<int:id>',views.wedpdf, name='wedpdf'),
    path('wedbulkupload/',views.wedbulkupload,name="wedbulkupload"),
    path('wedbulkuploadview/',views.wedbulkuploadview,name="wedbulkuploadview"),
    path('search-wed/', views.WedSearchView.as_view(), name='search_wed'),

    
    path('recform/',views.receptionFormView,name='recform'),   
    path('recshow/', recshow, name='recshow'),
    path('recdel/<int:f_oid>',views.recDelete,name="recdelete"),
    path('recup/<int:f_oid>',views.recUpdate,name="recupdate"),
    path('recpdf/<int:id>',views.recpdf, name='recpdf'),
    path('recbulkupload/',views.recbulkupload,name="recbulkupload"),
    path('recbulkuploadview/',views.recbulkuploadview,name="recbulkuploadview"),
    path('search-rec/', views.RecSearchView.as_view(), name='search_rec'),

    
]