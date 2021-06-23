from django.db.utils import IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)

from .models import Group, Post
from .serializers import (
    FollowSerializer,
    PostSerializer,
    CommentSerializer,
    GroupSerializer
)
from .permissions import (
    IsAuthorOrReadOnly,
    FollowNotExistsAndCantFollowYourself
)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        group = self.request.query_params.get('group')
        if group is not None:
            queryset = queryset.filter(group=group)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post.objects.prefetch_related('comments'),
                                 id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user,
                            post_id=self.kwargs['post_id'])
        except IntegrityError:
            raise Http404(
                f"post whit id {self.kwargs['post_id']} doesn't exist"
            )


class FollowCreateOrListViewSet(viewsets.GenericViewSet,
                                mixins.CreateModelMixin,
                                mixins.ListModelMixin):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,
                          FollowNotExistsAndCantFollowYourself)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.following.all()


class GroupCreateOrListViewSet(viewsets.GenericViewSet,
                               mixins.CreateModelMixin,
                               mixins.ListModelMixin):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
