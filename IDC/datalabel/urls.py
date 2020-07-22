from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='datalabel-index'),
    path('projectRequestForm/', views.projectRequestForm,
         name='datalabel-projectRequestForm'),
    path('project/<int:id>/', views.projectDetail, name='datalabel-project'),
    path('labelingProject/<str:projectName>', views.labelingProject, name='datalabel-labelingProject'),
    path('labelItem/<str:pname>/<str:fname>', views.labelItem, name='datalabel-labelItem'),
    # path('labelCorrection/', views.labelCorrection, name='datalabel-labelCorrection'),
    # path('addToProcessQueue/<str: tableName>', views.addToProcessQueue, name='datalabel-addToProcessQueue')
]
