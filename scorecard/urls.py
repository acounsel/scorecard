from django.urls import include, path

from .views import Home, CommitmentList, CommitmentExport
from .views import DocumentList, Methodology, CommitmentPDFExport

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('commitments/', CommitmentList.as_view(), 
        name='commitment-list'),
    path('documents/', DocumentList.as_view(), 
        name='document-list'),
    path('export/', CommitmentExport.as_view(), 
        name='export'),
    path('export-pdf/', CommitmentPDFExport.as_view(), 
        name='export-pdf'),
    path('methodology/', Methodology.as_view(), 
        name='methodology')
]  
