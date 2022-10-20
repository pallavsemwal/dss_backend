from django.urls import path
from . import views

 
urlpatterns = [ 
    path('createDoable', views.create_doable),
    #path('compliancePage',views.compliancePage)
    path('getAllCompliance',views.allCompliancePage),
    path('getComplianceDetail',views.getComplianceDetail),
    path('updateDoable',views.updateDoable),
    path('deleteDoable',views.deleteDoable)
]