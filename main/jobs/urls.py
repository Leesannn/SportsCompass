from django.urls import path

from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('postings/new/', views.job_create, name='job_create'),
    path('postings/new/reset/', views.job_manager_reset, name='job_manager_reset'),
    path('postings/<int:pk>/', views.job_detail, name='job_detail'),
    path('postings/<int:pk>/apply/', views.application_apply, name='application_apply'),
    path('postings/<int:pk>/delete/', views.job_delete_request, name='job_delete_request'),
    path('postings/<int:pk>/manage/<str:token>/', views.applicant_manage, name='applicant_manage'),
    path('postings/<int:pk>/manage/<str:token>/delete/', views.job_delete, name='job_delete'),
]
