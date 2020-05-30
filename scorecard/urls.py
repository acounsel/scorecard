from django.urls import include, path

from .views import Home, CommitmentList

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('commitments', CommitmentList.as_view(), 
        name='commitment-list')
]  
