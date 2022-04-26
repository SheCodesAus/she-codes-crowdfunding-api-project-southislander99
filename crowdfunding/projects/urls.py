from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:pk>/', views.ProjectDetail.as_view()),
    path('category/', views.CategoryList.as_view()),
    path('category/<int:pk>', views.CategoryDetail.as_view()),
    path('pledges/', views.PledgeList.as_view()),
    path('comments/', views.CommentList.as_view()),
    path("comment/<int:pk>/", views.CommentDetailApi.as_view()),
    path('projects/comment/<int:pk>/', views.CommentDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)