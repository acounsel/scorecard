from django.urls import include, path

from .views import Home, CommitmentList, CommitmentExport
from .views import DocumentList

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('commitments', CommitmentList.as_view(), 
        name='commitment-list'),
    path('documents', DocumentList.as_view(), 
        name='document-list'),
    path('export', CommitmentExport.as_view(), 
        name='export'),
]  
