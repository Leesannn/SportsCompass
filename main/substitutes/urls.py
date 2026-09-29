from django.urls import path

from . import views

app_name = 'substitutes'

urlpatterns = [
    path('', views.posting_list, name='posting_list'),
    path('postings/new/', views.posting_create, name='posting_create'),
    path('postings/new/reset/', views.posting_manager_reset, name='posting_manager_reset'),
    path('postings/<int:pk>/', views.posting_detail, name='posting_detail'),
    path('postings/<int:pk>/apply/', views.application_apply, name='application_apply'),
    path('postings/<int:pk>/edit/', views.posting_edit_request, name='posting_edit_request'),
    path('postings/<int:pk>/delete/', views.posting_delete_request, name='posting_delete_request'),
    path('postings/<int:pk>/manage/<str:token>/', views.applicant_manage, name='applicant_manage'),
    path('postings/<int:pk>/manage/<str:token>/delete/', views.posting_delete, name='posting_delete'),
    path(
        'postings/<int:pk>/manage/<str:token>/applications/<int:application_id>/evaluate/',
        views.application_evaluate, name='application_evaluate',
    ),
]
