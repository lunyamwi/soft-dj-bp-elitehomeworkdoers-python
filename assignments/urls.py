from django.urls import path
from .views import (
    AssignmentCategoryView,
    AssignmentSearchView,
    AssignmentDetailView,
    assignment_upload,
    search_assignment,
    delete_assignment,
    assignment_detail
)

app_name='assignments'

urlpatterns = [
    path('list/',AssignmentCategoryView,name='category'),
    path('search/',search_assignment,name='search'),
    path('detail/',AssignmentDetailView,name='detail'),
    path('upload/',assignment_upload,name='upload'),
    path('delete/<int:pk>/',delete_assignment,name='delete_assignment'),
    path('edit/<int:pk>/',delete_assignment,name='edit_assignment'),
    path('detail/<int:pk>/',assignment_detail,name='assignment_detail'),
]
