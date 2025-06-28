from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BlogPostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import BlogPost, Comments
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
# Create your views here.
class BlogPostView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            blogs = BlogPost.objects.select_related("author").order_by("-create_at")
            if request.GET.get("search"):
                search = request.GET.get("search")
                blogs = BlogPost.objects.select_related("author").filter(Q(title__contains=search) | Q(description__contains=search)).order_by("-create_at")

            page_num = request.GET.get("page_num")
            paginator = Paginator(blogs,10)
            page_obj = paginator.get_page(page_num)
            serializer = BlogPostSerializer(page_obj, many=True)

            return Response(
                {
                    "data": serializer.data,
                    "message": "Blogs listed",
                    'next': page_obj.next_page_number() if page_obj.has_next() else None,
                    'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
                }, status = status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "data": {},
                    "message": "Error occured"
                }, status=status.HTTP_400_BAD_REQUEST
            )
    
    def post(self, request):
        try:
            data = request.data
            data['author'] = request.user.id
            serializer = BlogPostSerializer(data=data)

            if not serializer.is_valid():
                return Response(
                        {
                            "data" : serializer.errors,
                            "message": "Error occured"
                        }, status = status.HTTP_400_BAD_REQUEST
                    )
            serializer.save()

            return Response({
                    'data': serializer.data,
                    'message': "Blog created"
                }, status= status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                    {
                        "data" : {},
                        "message": "Error occured"
                    }, status = status.HTTP_400_BAD_REQUEST
                )

class BlogPostDetailedView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        try:
            blogs = get_object_or_404(BlogPost, pk=pk)
            serializer = BlogPostSerializer(blogs)

            comments = blogs.comments.all().order_by('-created_at')
            comment_paginator = Paginator(comments,10)
            comment_page_num = request.GET.get("comment_page_num")
            comment_page_obj = comment_paginator.get_page(comment_page_num)
            
            comment_serializer = CommentSerializer(comment_page_obj, many=True)

            return Response(
                {
                    "data": serializer.data,
                    "comments_data": {
                        "comments": comment_serializer.data,
                        'next_comment': comment_page_obj.next_page_number() if comment_page_obj.has_next() else None,
                        'previous_comment': comment_page_obj.previous_page_number() if comment_page_obj.has_previous() else None,
                    },
                    "message": "Blogs listed",
                }, status = status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "data": {},
                    "message": "Blog not found"
                }, status=status.HTTP_400_BAD_REQUEST
            )
        
    def delete(self,request,pk=None):
        if not pk:
            return Response(
                {
                    "date": {},
                    "message": "Blog ID is required"
                }, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            blog = get_object_or_404(BlogPost, pk=pk)
            if request.user != blog.author:
                return Response({
                    "data": {},
                    "message": "Blog can only be deleted by the posted author"
                }, status=status.HTTP_403_FORBIDDEN)
            
            blog.delete()
            return Response({
                "data": {},
                "message": "Blog deleted"
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
        
class CommentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, pk):
        try:
            blog = get_object_or_404(BlogPost, pk=pk)
            data = request.data
            data['author'] = request.user.id
            data['blog'] = blog.id
            serializer = CommentSerializer(data=data)
            if not serializer.is_valid():
                return Response(
                        {
                            "data" : serializer.errors,
                            "message": "Error occured"
                        }, status = status.HTTP_400_BAD_REQUEST
                    )
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': "Comment added"
            }, status= status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {
                    "data": {},
                    "message": "Error occured"
                }, status=status.HTTP_400_BAD_REQUEST
            )