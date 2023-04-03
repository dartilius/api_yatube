from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from posts.models import Post, Group, Comment


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request):
        """Метод для вывода всех постов."""
        if request.user.is_authenticated:
            queryset = Post.objects.all()
            serializer = PostSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(status=401)

    def create(self, request):
        """Метод для создания поста."""
        if request.user.is_authenticated:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        return Response(status=401)

    def update(self, request, pk=None):
        """Метод для обновления поста."""
        if request.user.is_authenticated:
            post = get_object_or_404(self.queryset, pk=pk)
            if request.user == post.author:
                serializer = PostSerializer(
                    post,
                    data=request.data,
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            return Response(status=403)
        return Response(status=401)

    def partial_update(self, request, pk=None):
        """Метод для частичного обновления поста."""
        if request.user.is_authenticated:
            post = get_object_or_404(self.queryset, pk=pk)
            if request.user == post.author:
                serializer = PostSerializer(
                    post,
                    data=request.data,
                    partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            return Response(status=403)
        return Response(status=401)

    def retrieve(self, request, pk=None):
        """Метод для получения поста по PK."""
        if request.user.is_authenticated:
            post = get_object_or_404(self.queryset, pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        return Response(status=401)

    def destroy(self, request, pk=None):
        """Метод для удаления поста по PK."""
        if request.user.is_authenticated:
            post = get_object_or_404(self.queryset, pk=pk)
            if request.user == post.author:
                post.delete()
                return Response(status=204)
            return Response(status=403)
        return Response(status=401)


class GroupViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Post."""

    queryset = Group.objects.all()
    serializer_class = PostSerializer

    def list(self, request):
        """Метод для вывода всех групп."""
        if request.user.is_authenticated:
            serializer = GroupSerializer(self.queryset, many=True)
            return Response(serializer.data)
        return Response(status=401)

    def retrieve(self, request, pk=None):
        """Метод для получения группы по PK."""
        if request.user.is_authenticated:
            post = get_object_or_404(self.queryset, pk=pk)
            serializer = GroupSerializer(post)
            return Response(serializer.data)
        return Response(status=401)

    def create(self, request):
        return Response(status=405)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, post_pk=None):
        """Метод для вывода всех комментариев."""
        if request.user.is_authenticated:
            post = get_object_or_404(Post, pk=post_pk)
            queryset = post.comments.all()
            serializer = CommentSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(status=401)

    def create(self, request, post_pk=None):
        """Метод для создания коментария."""
        post = get_object_or_404(Post, pk=post_pk)
        if request.user.is_authenticated:
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        return Response(status=401)

    def update(self, request, post_pk=None, pk=None):
        """Метод для обновления комментария."""
        post = get_object_or_404(Post, pk=post_pk)
        queryset = post.comments.all()
        if request.user.is_authenticated:
            comment = get_object_or_404(queryset, pk=pk)
            if request.user == comment.author:
                serializer = CommentSerializer(
                    comment,
                    data=request.data
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            return Response(status=403)
        return Response(status=401)

    def partial_update(self, request, post_pk=None, pk=None):
        """Метод для частичного обновления коментария."""
        if request.user.is_authenticated:
            post = get_object_or_404(Post, pk=post_pk)
            queryset = post.comments.all()
            comment = get_object_or_404(queryset, pk=pk)
            if request.user == comment.author:
                serializer = CommentSerializer(
                    comment,
                    data=request.data,
                    partial=True
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)
            return Response(status=403)
        return Response(status=401)

    def retrieve(self, request, post_pk=None, pk=None):
        """Метод для получения коментария по PK."""
        if request.user.is_authenticated:
            post = get_object_or_404(Post, pk=post_pk)
            queryset = post.comments.all()
            comment = get_object_or_404(queryset, pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        return Response(status=401)

    def destroy(self, request, post_pk=None, pk=None):
        """Метод для удаления коментария по PK."""
        if request.user.is_authenticated:
            post = get_object_or_404(Post, pk=post_pk)
            queryset = post.comments.all()
            comment = get_object_or_404(queryset, pk=pk)
            if request.user == comment.author:
                comment.delete()
                return Response(status=204)
            return Response(status=403)
        return Response(status=401)
