from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='datalabel-index'),
    path('projectRequestForm/', views.projectRequestForm,
         name='datalabel-projectRequestForm'),
    path('project/<int:id>/', views.projectDetail, name='datalabel-project'),
    path('getNextItem/', views.getNextItem, name='datalabel-getNextItem')
]
