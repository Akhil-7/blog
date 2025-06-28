from django.urls import path
from .views import BlogPostView, BlogPostDetailedView,CommentView
urlpatterns = [
    path("blogs/", BlogPostView.as_view()),
    path("blogs/<int:pk>/", BlogPostDetailedView.as_view()),
    path("blogs/<int:pk>/add_comment/", CommentView.as_view()),
]
