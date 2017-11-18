from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):

    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Book
        fields = '__all__'
