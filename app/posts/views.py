from django.shortcuts import render
from django_filters import filters
from rest_framework import viewsets, mixins
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import PostPermission
from rest_framework.permissions import IsAuthenticated
from .models import Tweet, StatusTweet, Comment, StatusType
from .serializers import TweetSerializer, StatusTweetSerializer, StatusCommentSerializer, \
    CommentSerializer


class PostPagePagination(PageNumberPagination):
    page_size = 3


class TweetViewSet(viewsets.ModelViewSet):
    """
    API для создания, получения, изменения и удаления твитов
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [PostPermission, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['text', ]
    search_fields = ['text', ]
    ordering_fields = ['text', ]
    pagination_class = PostPagePagination

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     text = self.request.query_params.get('text')
    #     if text:
    #         queryset = queryset.filter(text__icontains=text)
    #     return queryset

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated, ])
    def leave_status(self, request, pk=None):
        serializer = StatusTweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                profile=request.user.profile,
                tweet=self.get_object()
            )
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


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return super().get_queryset().filter(tweet_id=self.kwargs.get('tweet_id'))

    def perform_create(self, serializer):
        serializer.save(
            profile=self.request.user.profile,
            tweet_id=self.kwargs.get('tweet_id')
        )

# class CommentViewSet(mixins.RetrieveModelMixin,
#                      mixins.UpdateModelMixin,
#                      mixins.DestroyModelMixin,
#                      mixins.ListModelMixin,
#                      GenericViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(profile=self.request.user.profile)
#
#     @action(methods=['POST'], detail=True)
#     def leave_status(self, request, pk=None):
#         serializer = StatusCommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(comment=self.get_object(),
#                             profile=request.user.profile)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class StatusTypeViewSet(viewsets.ModelViewSet):
#     queryset = StatusType.objects.all()
#     serializer_class = StatusTypeSerializer
