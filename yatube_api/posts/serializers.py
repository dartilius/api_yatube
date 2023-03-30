from rest_framework import serializers
from .models import Post, Comment, Group


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""
    author = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'text', 'author', 'image', 'pub_date')
        read_only_fields = ('author',)
        model = Post

    def get_author(self, obj):
        """Метод для получения имени автора."""
        return obj.author.username


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""
    author = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'post')
        model = Comment

    def get_author(self, obj):
        """Метод для получения имени автора."""
        return obj.author.username