from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


@api_view(['GET', 'POST'])
def api_posts(request):
    """Вью для постав."""
    if request.user.is_authenticated:
        if request.method == 'POST':
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    return Response(status=401)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_posts_detail(request, pk):
    """Вью для отдельного поста по pk."""
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)

        if request.method == 'GET':
            serializer = PostSerializer(post)
            return Response(serializer.data)

        if request.method == 'PUT' or request.method == 'PATCH':
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

        if request.method == 'DELETE':
            if request.user == post.author:
                post.delete()
                return Response(status=204)
            return Response(status=403)

    return Response(status=401)


@api_view(['GET', ])
def api_groups(request):
    """Вью для групп."""
    if request.user.is_authenticated:
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
    return Response(status=401)


@api_view(['GET', ])
def api_groups_detail(request, pk):
    """Вью для отдельной группы."""
    if request.user.is_authenticated:
        group = get_object_or_404(Group, id=pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)
    return Response(status=401)


@api_view(['GET', 'POST'])
def api_comments(request, post_pk):
    """Вью для коментов."""
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_pk)

        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    return Response(status=401)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_comments_detail(request, post_pk, comment_pk):
    """Вью для отдельного коммента."""
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_pk)

        if request.method == 'GET':
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

        if request.method == 'PUT' or request.method == 'PATCH':
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

        if request.method == 'DELETE':
            if request.user.is_authenticated:
                if request.user == comment.author:
                    comment.delete()
                    return Response(status=204)
                return Response(status=403)

    return Response(status=401)
