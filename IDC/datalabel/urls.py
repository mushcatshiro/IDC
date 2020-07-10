from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='datalabel-index'),
    path('projectRequestForm/', views.projectRequestForm,
         name='datalabel-projectRequestForm'),
    path('project/<int:id>/', views.projectDetail, name='datalabel-project'),
    path('labelNextItem/', views.labelNextItem, name='datalabel-labelNextItem')
    path('labelCorrection/', views.labelCorrection, name='datalabel-labelCorrection'),
    path('addToProcessQueue/<str: tableName>', views.addToProcessQueue, name='datalabel-addToProcessQueue')
]
