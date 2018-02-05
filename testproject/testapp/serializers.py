from rest_framework.serializers import ModelSerializer

from .models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'admin_only_field',
            'body',
            'created_at',
            'id',
            'title',
            'updated_at',
            'user',
        )
        read_only_fields = (
            'id',
            'user',
        )

    def validate(self, data):
        data['user'] = self.context['request'].user
        return data


class PostSerializerForUser(PostSerializer):
    class Meta:
        model = Post
        fields = (
            'body',
            'created_at',
            'id',
            'title',
            'updated_at',
            'user',
        )
        read_only_fields = (
            'id',
            'user',
        )
