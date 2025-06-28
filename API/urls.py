from django.urls import path, include

urlpatterns = [
    path("user/", include("user_management.urls")),
    path("blog/", include("blog_management.urls")),
]
