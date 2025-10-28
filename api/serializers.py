from rest_framework import serializers
from .models import Post, User


class PostSerializer(serializers.ModelSerializer):
    class Meta():
        model = Post
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user