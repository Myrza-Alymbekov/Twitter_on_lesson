from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet

from .models import Tweet, StatusTweet, Comment
from .serializers import TweetSerializer, StatusTweetSerializer, StatusCommentSerializer, \
                        CommentSerializer


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    @action(methods=['POST'], detail=True)
    def leave_status(self, request, pk=None):
        serializer = StatusTweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tweet=self.get_object(),
                            profile=request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True)
    def comment(self, request, pk=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tweet=self.get_object(),
                            profile=request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True)
    def view_comments(self, request, pk=None):
        queryset = Comment.objects.filter(tweet_id=self.get_object().id)
        serializer = CommentSerializer(queryset, many=True)

        return Response(serializer.data)


class CommentViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    @action(methods=['POST'], detail=True)
    def leave_status(self, request, pk=None):
        serializer = StatusCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(comment=self.get_object(),
                            profile=request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

